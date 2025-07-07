from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Q, Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.utils import timezone
import logging

from .models import Tutorial, TutorialCategory, TutorialStep, AITutorialRequest, UserTutorialProgress, TutorialRating
from .serializers import (
    TutorialListSerializer, TutorialDetailSerializer, TutorialCategorySerializer,
    AITutorialRequestSerializer, TutorialProgressUpdateSerializer, TutorialRatingSerializer
)
from .services import AITutorialGenerator

logger = logging.getLogger(__name__)


class TutorialViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tutorial.objects.select_related('category').prefetch_related('steps', 'ratings')
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category', 'difficulty', 'is_ai_generated']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'estimated_duration']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return TutorialListSerializer
        return TutorialDetailSerializer
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def start(self, request, pk=None):
        """Start a tutorial (create progress record)"""
        tutorial = self.get_object()
        
        progress, created = UserTutorialProgress.objects.get_or_create(
            user=request.user,
            tutorial=tutorial,
            defaults={'started_at': timezone.now()}
        )
        
        if not created:
            progress.last_accessed = timezone.now()
            progress.save()
        
        return Response({
            'message': 'Tutorial started' if created else 'Tutorial resumed',
            'progress': {
                'progress_percentage': float(progress.progress_percentage),
                'completed_steps': progress.completed_steps,
                'started_at': progress.started_at,
                'last_accessed': progress.last_accessed
            }
        })
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def update_progress(self, request, pk=None):
        """Update tutorial progress"""
        tutorial = self.get_object()
        
        try:
            progress = UserTutorialProgress.objects.get(user=request.user, tutorial=tutorial)
        except UserTutorialProgress.DoesNotExist:
            return Response(
                {'error': 'Tutorial not started yet'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = TutorialProgressUpdateSerializer(progress, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Progress updated',
                'progress': {
                    'progress_percentage': float(progress.progress_percentage),
                    'completed_steps': progress.completed_steps,
                    'completed_at': progress.completed_at
                }
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def rate(self, request, pk=None):
        """Rate a tutorial"""
        tutorial = self.get_object()
        
        serializer = TutorialRatingSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            # Check if user already rated this tutorial
            existing_rating = TutorialRating.objects.filter(
                user=request.user, tutorial=tutorial
            ).first()
            
            if existing_rating:
                # Update existing rating
                serializer = TutorialRatingSerializer(
                    existing_rating, data=request.data, partial=True, context={'request': request}
                )
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response({'message': 'Rating updated', 'rating': serializer.data})
            else:
                # Create new rating
                serializer.save(tutorial=tutorial)
                return Response({'message': 'Rating added', 'rating': serializer.data})
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def popular(self, request):
        """Get popular tutorials based on ratings and completion rates"""
        tutorials = self.get_queryset().annotate(
            avg_rating=Avg('ratings__rating')
        ).filter(avg_rating__gte=4.0).order_by('-avg_rating')[:10]
        
        serializer = TutorialListSerializer(tutorials, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def recommended(self, request):
        """Get recommended tutorials for the user"""
        if not request.user.is_authenticated:
            # Return popular tutorials for anonymous users
            return self.popular(request)
        
        # Get user's completed tutorials to find similar ones
        completed_tutorials = UserTutorialProgress.objects.filter(
            user=request.user, progress_percentage=100
        ).values_list('tutorial__category', flat=True)
        
        if completed_tutorials:
            # Recommend tutorials from similar categories
            tutorials = self.get_queryset().filter(
                category__in=completed_tutorials
            ).exclude(
                user_progress__user=request.user
            )[:10]
        else:
            # Recommend beginner tutorials
            tutorials = self.get_queryset().filter(difficulty='beginner')[:10]
        
        serializer = TutorialListSerializer(tutorials, many=True, context={'request': request})
        return Response(serializer.data)


class TutorialCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TutorialCategory.objects.prefetch_related('tutorials')
    serializer_class = TutorialCategorySerializer
    permission_classes = [permissions.AllowAny]


class AITutorialRequestViewSet(viewsets.ModelViewSet):
    serializer_class = AITutorialRequestSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return AITutorialRequest.objects.filter(user=self.request.user).order_by('-created_at')
    
    def create(self, request, *args, **kwargs):
        """Create a new AI tutorial request"""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            tutorial_request = serializer.save()
            
            # Start generating tutorial in the background
            try:
                generator = AITutorialGenerator()
                tutorial = generator.generate_tutorial(tutorial_request)
                
                # Return the created tutorial
                tutorial_serializer = TutorialDetailSerializer(
                    tutorial, context={'request': request}
                )
                return Response({
                    'message': 'Tutorial generated successfully',
                    'request': serializer.data,
                    'tutorial': tutorial_serializer.data
                }, status=status.HTTP_201_CREATED)
                
            except Exception as e:
                logger.error(f"Error generating tutorial: {str(e)}")
                return Response({
                    'message': 'Tutorial request created but generation failed',
                    'request': serializer.data,
                    'error': str(e)
                }, status=status.HTTP_202_ACCEPTED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'])
    def suggestions(self, request):
        """Get AI-powered tutorial suggestions"""
        topic = request.data.get('topic', '')
        if not topic:
            return Response(
                {'error': 'Topic is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            generator = AITutorialGenerator()
            suggestions = generator.get_tutorial_suggestions(topic)
            return Response(suggestions)
        except Exception as e:
            logger.error(f"Error getting suggestions: {str(e)}")
            return Response(
                {'error': 'Failed to get suggestions'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=True, methods=['post'])
    def regenerate(self, request, pk=None):
        """Regenerate a failed tutorial"""
        tutorial_request = self.get_object()
        
        if tutorial_request.status != 'failed':
            return Response(
                {'error': 'Can only regenerate failed tutorials'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            generator = AITutorialGenerator()
            tutorial = generator.generate_tutorial(tutorial_request)
            
            tutorial_serializer = TutorialDetailSerializer(
                tutorial, context={'request': request}
            )
            return Response({
                'message': 'Tutorial regenerated successfully',
                'tutorial': tutorial_serializer.data
            })
            
        except Exception as e:
            logger.error(f"Error regenerating tutorial: {str(e)}")
            return Response(
                {'error': f'Failed to regenerate tutorial: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
