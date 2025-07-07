from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Post, Category, Tag, Comment, PostLike, PostView


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']


class CategorySerializer(serializers.ModelSerializer):
    posts_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'posts_count', 'created_at']
    
    def get_posts_count(self, obj):
        return obj.posts.filter(status='published').count()


class TagSerializer(serializers.ModelSerializer):
    posts_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Tag
        fields = ['id', 'name', 'posts_count', 'created_at']
    
    def get_posts_count(self, obj):
        return obj.posts.filter(status='published').count()


class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    replies = serializers.SerializerMethodField()
    
    class Meta:
        model = Comment
        fields = ['id', 'content', 'author', 'parent', 'replies', 'is_approved', 'created_at', 'updated_at']
        read_only_fields = ['author', 'is_approved']
    
    def get_replies(self, obj):
        if obj.replies.exists():
            return CommentSerializer(obj.replies.filter(is_approved=True), many=True).data
        return []
    
    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)


class PostListSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    comments_count = serializers.SerializerMethodField()
    reading_time = serializers.ReadOnlyField()
    
    class Meta:
        model = Post
        fields = [
            'id', 'title', 'slug', 'author', 'excerpt', 'featured_image',
            'category', 'tags', 'status', 'is_featured', 'views_count',
            'likes_count', 'comments_count', 'reading_time', 'created_at',
            'updated_at', 'published_at'
        ]
    
    def get_comments_count(self, obj):
        return obj.comments.filter(is_approved=True).count()


class PostDetailSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    comments = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    reading_time = serializers.ReadOnlyField()
    is_liked_by_user = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = [
            'id', 'title', 'slug', 'author', 'content', 'excerpt',
            'featured_image', 'category', 'tags', 'status', 'is_featured',
            'views_count', 'likes_count', 'comments', 'comments_count',
            'reading_time', 'is_liked_by_user', 'created_at', 'updated_at',
            'published_at'
        ]
    
    def get_comments(self, obj):
        # Get top-level comments (no parent)
        top_comments = obj.comments.filter(parent=None, is_approved=True).order_by('created_at')
        return CommentSerializer(top_comments, many=True).data
    
    def get_comments_count(self, obj):
        return obj.comments.filter(is_approved=True).count()
    
    def get_is_liked_by_user(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.likes.filter(user=request.user).exists()
        return False


class PostCreateUpdateSerializer(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(many=True, queryset=Tag.objects.all(), required=False)
    
    class Meta:
        model = Post
        fields = [
            'title', 'slug', 'content', 'excerpt', 'featured_image',
            'category', 'tags', 'status', 'is_featured'
        ]
    
    def create(self, validated_data):
        tags_data = validated_data.pop('tags', [])
        validated_data['author'] = self.context['request'].user
        post = Post.objects.create(**validated_data)
        post.tags.set(tags_data)
        return post
    
    def update(self, instance, validated_data):
        tags_data = validated_data.pop('tags', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        if tags_data is not None:
            instance.tags.set(tags_data)
        
        return instance


class PostLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostLike
        fields = ['id', 'created_at']
        read_only_fields = ['id', 'created_at']
