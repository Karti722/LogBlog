from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Q, Count, F
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.contrib.auth.models import User
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


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.annotate(posts_count=Count('posts'))
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.annotate(posts_count=Count('posts'))
    serializer_class = TagSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [SearchFilter]
    search_fields = ['name']


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.select_related('author', 'post').prefetch_related('replies')
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['post', 'is_approved']
    ordering = ['created_at']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter approved comments for non-staff users
        if not self.request.user.is_staff:
            queryset = queryset.filter(is_approved=True)
        
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    
    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAuthenticatedOrReadOnly]
        
        return [permission() for permission in permission_classes]
    
    def update(self, request, *args, **kwargs):
        comment = self.get_object()
        
        # Only allow author or staff to update
        if comment.author != request.user and not request.user.is_staff:
            return Response(
                {'error': 'You can only edit your own comments'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        return super().update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        comment = self.get_object()
        
        # Only allow author or staff to delete
        if comment.author != request.user and not request.user.is_staff:
            return Response(
                {'error': 'You can only delete your own comments'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        return super().destroy(request, *args, **kwargs)
