from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Tag, Post, Comment, PostLike, PostView


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'posts_count', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at']
    
    def posts_count(self, obj):
        return obj.posts.count()
    posts_count.short_description = 'Posts Count'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'posts_count', 'created_at']
    search_fields = ['name']
    readonly_fields = ['created_at']
    
    def posts_count(self, obj):
        return obj.posts.count()
    posts_count.short_description = 'Posts Count'


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'status', 'is_featured', 'views_count', 'likes_count', 'created_at']
    list_filter = ['status', 'is_featured', 'category', 'created_at']
    search_fields = ['title', 'content', 'excerpt']
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ['tags']
    readonly_fields = ['views_count', 'likes_count', 'created_at', 'updated_at', 'reading_time']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'author', 'excerpt')
        }),
        ('Content', {
            'fields': ('content', 'featured_image')
        }),
        ('Categorization', {
            'fields': ('category', 'tags')
        }),
        ('Status', {
            'fields': ('status', 'is_featured')
        }),
        ('Statistics', {
            'fields': ('views_count', 'likes_count', 'reading_time'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'published_at'),
            'classes': ('collapse',)
        })
    )
    
    def save_model(self, request, obj, form, change):
        if not change:  # If creating new post
            obj.author = request.user
        super().save_model(request, obj, form, change)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['post', 'author', 'content_preview', 'is_approved', 'is_reply', 'created_at']
    list_filter = ['is_approved', 'created_at', 'post']
    search_fields = ['content', 'author__username', 'post__title']
    readonly_fields = ['created_at', 'updated_at']
    
    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content Preview'
    
    def is_reply(self, obj):
        return obj.parent is not None
    is_reply.boolean = True
    is_reply.short_description = 'Is Reply'


@admin.register(PostLike)
class PostLikeAdmin(admin.ModelAdmin):
    list_display = ['post', 'user', 'created_at']
    list_filter = ['created_at']
    search_fields = ['post__title', 'user__username']
    readonly_fields = ['created_at']


@admin.register(PostView)
class PostViewAdmin(admin.ModelAdmin):
    list_display = ['post', 'user', 'ip_address', 'created_at']
    list_filter = ['created_at']
    search_fields = ['post__title', 'user__username', 'ip_address']
    readonly_fields = ['created_at']
