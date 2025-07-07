from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Q, Count, F
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.contrib.auth.models import User
from django.utils import timezone
import logging

from .models import Post, Category, Tag, Comment, PostLike, PostView
from .serializers import (
    PostListSerializer, PostDetailSerializer, PostCreateUpdateSerializer,
    CategorySerializer, TagSerializer, CommentSerializer, PostLikeSerializer
)

logger = logging.getLogger(__name__)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.select_related('author', 'category').prefetch_related('tags', 'comments')
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category', 'tags', 'status', 'is_featured']
    search_fields = ['title', 'content', 'excerpt']
    ordering_fields = ['created_at', 'updated_at', 'published_at', 'views_count', 'likes_count']
    ordering = ['-created_at']
    lookup_field = 'slug'
    
    def get_serializer_class(self):
        if self.action == 'list':
            return PostListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return PostCreateUpdateSerializer
        return PostDetailSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter published posts for non-owners
        if self.request.user.is_anonymous:
            queryset = queryset.filter(status='published')
        elif not self.request.user.is_staff:
            queryset = queryset.filter(
                Q(status='published') | Q(author=self.request.user)
            )
        
        return queryset
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        
        # Record view if not the author
        if request.user != instance.author:
            self._record_view(instance, request)
        
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    def _record_view(self, post, request):
        """Record a view for the post"""
        try:
            # Get IP address
            ip_address = self._get_client_ip(request)
            
            # Create or get view record
            view, created = PostView.objects.get_or_create(
                post=post,
                ip_address=ip_address,
                defaults={'user': request.user if request.user.is_authenticated else None}
            )
            
            if created:
                # Increment view count
                Post.objects.filter(id=post.id).update(views_count=F('views_count') + 1)
                
        except Exception as e:
            logger.error(f"Error recording view: {str(e)}")
    
    def _get_client_ip(self, request):
        """Get client IP address"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def like(self, request, pk=None):
        """Like or unlike a post"""
        post = self.get_object()
        
        try:
            like = PostLike.objects.get(post=post, user=request.user)
            like.delete()
            # Decrement like count
            Post.objects.filter(id=post.id).update(likes_count=F('likes_count') - 1)
            return Response({'liked': False, 'message': 'Post unliked'})
        except PostLike.DoesNotExist:
            PostLike.objects.create(post=post, user=request.user)
            # Increment like count
            Post.objects.filter(id=post.id).update(likes_count=F('likes_count') + 1)
            return Response({'liked': True, 'message': 'Post liked'})
    
    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Get featured posts"""
        posts = self.get_queryset().filter(is_featured=True)[:5]
        serializer = PostListSerializer(posts, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def popular(self, request):
        """Get popular posts based on views and likes"""
        posts = self.get_queryset().annotate(
            popularity_score=F('views_count') + F('likes_count') * 2
        ).order_by('-popularity_score')[:10]
        serializer = PostListSerializer(posts, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def recent(self, request):
        """Get recent posts"""
        posts = self.get_queryset().filter(status='published').order_by('-published_at')[:10]
        serializer = PostListSerializer(posts, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def ai_title_suggestions(self, request):
        """Generate AI-powered title suggestions for a blog post"""
        try:
            from ai_tutorial.services import OpenAIService
            
            topic = request.data.get('topic', '')
            keywords = request.data.get('keywords', [])
            
            if not topic:
                return Response({'error': 'Topic is required'}, status=status.HTTP_400_BAD_REQUEST)
            
            ai_service = OpenAIService()
            prompt = f"""
            Generate 5 compelling blog post titles for the following topic: {topic}
            Keywords to include: {', '.join(keywords) if keywords else 'None'}
            
            Requirements:
            - Titles should be engaging and clickable
            - Include relevant keywords naturally
            - Vary in style (how-to, listicle, guide, etc.)
            - Keep titles under 60 characters for SEO
            
            Return only the titles, one per line.
            """
            
            suggestions = ai_service.generate_content(prompt)
            titles = [title.strip() for title in suggestions.split('\n') if title.strip()]
            
            return Response({'suggestions': titles})
            
        except Exception as e:
            logger.error(f"Error generating title suggestions: {str(e)}")
            return Response({'error': 'Failed to generate suggestions'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def ai_content_outline(self, request):
        """Generate AI-powered content outline for a blog post"""
        try:
            from ai_tutorial.services import OpenAIService
            
            title = request.data.get('title', '')
            target_audience = request.data.get('target_audience', 'general')
            content_type = request.data.get('content_type', 'tutorial')
            
            if not title:
                return Response({'error': 'Title is required'}, status=status.HTTP_400_BAD_REQUEST)
            
            ai_service = OpenAIService()
            prompt = f"""
            Create a detailed outline for a blog post with the title: "{title}"
            Target audience: {target_audience}
            Content type: {content_type}
            
            Requirements:
            - Create a logical structure with main sections and subsections
            - Include introduction and conclusion
            - Suggest key points to cover in each section
            - Add suggestions for examples, code snippets, or visuals where appropriate
            - Ensure the outline flows logically from beginner to advanced concepts
            
            Format the outline with clear headers and bullet points.
            """
            
            outline = ai_service.generate_content(prompt)
            
            return Response({'outline': outline})
            
        except Exception as e:
            logger.error(f"Error generating content outline: {str(e)}")
            return Response({'error': 'Failed to generate outline'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def ai_writing_tips(self, request):
        """Get AI-powered writing tips based on current content"""
        try:
            from ai_tutorial.services import OpenAIService
            
            content = request.data.get('content', '')
            title = request.data.get('title', '')
            improvement_focus = request.data.get('focus', 'general')
            
            if not content:
                return Response({'error': 'Content is required'}, status=status.HTTP_400_BAD_REQUEST)
            
            ai_service = OpenAIService()
            prompt = f"""
            Analyze the following blog post content and provide specific writing improvement suggestions:
            
            Title: {title}
            Content: {content[:2000]}...
            
            Focus on: {improvement_focus}
            
            Provide feedback on:
            1. Content structure and flow
            2. Readability and clarity
            3. Engagement and tone
            4. SEO optimization
            5. Technical accuracy (if applicable)
            
            Give 3-5 specific, actionable suggestions for improvement.
            """
            
            tips = ai_service.generate_content(prompt)
            
            return Response({'tips': tips})
            
        except Exception as e:
            logger.error(f"Error generating writing tips: {str(e)}")
            return Response({'error': 'Failed to generate tips'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def perform_create(self, request, *args, **kwargs):
        """Override to set the author when creating a post"""
        return super().perform_create(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        """Override create to handle blog post creation with AI assistance tracking"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Set the author to the current user
        serializer.save(author=request.user)
        
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=False, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def track_ai_assistance(self, request):
        """Track AI assistance usage for a user"""
        try:
            from ai_tutorial.models import AIUsage
            
            # Log the AI assistance usage
            AIUsage.objects.create(
                user=request.user,
                endpoint='blog_post_creation',  # or other relevant endpoint
                timestamp=timezone.now()
            )
            
            return Response({'message': 'AI assistance usage tracked'})
        
        except Exception as e:
            logger.error(f"Error tracking AI assistance: {str(e)}")
            return Response({'error': 'Failed to track usage'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def ai_usage_stats(self, request):
        """Get AI usage statistics for the authenticated user"""
        try:
            from ai_tutorial.models import AIUsage
            
            # Get usage stats for the user
            stats = AIUsage.objects.filter(user=request.user).values(
                'endpoint'
            ).annotate(
                total_usage=Count('id')
            ).order_by('-total_usage')
            
            return Response({'usage_stats': list(stats)})
        
        except Exception as e:
            logger.error(f"Error fetching AI usage stats: {str(e)}")
            return Response({'error': 'Failed to fetch stats'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for Category model - read-only for now"""
    queryset = Category.objects.annotate(post_count=Count('posts')).order_by('name')
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for Tag model - read-only for now"""
    queryset = Tag.objects.annotate(post_count=Count('posts')).order_by('name')
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class CommentViewSet(viewsets.ModelViewSet):
    """ViewSet for Comment model"""
    queryset = Comment.objects.select_related('author', 'post').order_by('-created_at')
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        """Filter comments by post if post_id is provided"""
        queryset = super().get_queryset()
        post_id = self.request.query_params.get('post_id')
        if post_id:
            queryset = queryset.filter(post_id=post_id)
        return queryset
    
    def perform_create(self, serializer):
        """Set the author when creating a comment"""
        serializer.save(author=self.request.user)
