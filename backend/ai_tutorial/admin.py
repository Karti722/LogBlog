from django.contrib import admin
from django.utils.html import format_html
from .models import TutorialCategory, Tutorial, TutorialStep, AITutorialRequest, UserTutorialProgress, TutorialRating


@admin.register(TutorialCategory)
class TutorialCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon', 'tutorials_count', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at']
    
    def tutorials_count(self, obj):
        return obj.tutorials.count()
    tutorials_count.short_description = 'Tutorials Count'


class TutorialStepInline(admin.TabularInline):
    model = TutorialStep
    extra = 1
    fields = ['step_number', 'title', 'content', 'code_example']
    ordering = ['step_number']


@admin.register(Tutorial)
class TutorialAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'difficulty', 'estimated_duration', 'steps_count', 'is_ai_generated', 'created_at']
    list_filter = ['difficulty', 'is_ai_generated', 'category', 'created_at']
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [TutorialStepInline]
    readonly_fields = ['created_at', 'updated_at']
    
    def steps_count(self, obj):
        return obj.steps.count()
    steps_count.short_description = 'Steps Count'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'category', 'description')
        }),
        ('Details', {
            'fields': ('difficulty', 'estimated_duration', 'is_ai_generated')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )


@admin.register(TutorialStep)
class TutorialStepAdmin(admin.ModelAdmin):
    list_display = ['tutorial', 'step_number', 'title', 'is_completed']
    list_filter = ['tutorial', 'is_completed']
    search_fields = ['title', 'content', 'tutorial__title']
    readonly_fields = ['created_at']


@admin.register(AITutorialRequest)
class AITutorialRequestAdmin(admin.ModelAdmin):
    list_display = ['topic', 'user', 'difficulty', 'status', 'created_at', 'completed_at']
    list_filter = ['status', 'difficulty', 'created_at']
    search_fields = ['topic', 'description', 'user__username']
    readonly_fields = ['created_at', 'completed_at']
    
    fieldsets = (
        ('Request Information', {
            'fields': ('user', 'topic', 'description', 'difficulty')
        }),
        ('Status', {
            'fields': ('status', 'generated_tutorial', 'error_message')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'completed_at'),
            'classes': ('collapse',)
        })
    )


@admin.register(UserTutorialProgress)
class UserTutorialProgressAdmin(admin.ModelAdmin):
    list_display = ['user', 'tutorial', 'progress_percentage', 'started_at', 'completed_at']
    list_filter = ['progress_percentage', 'started_at', 'completed_at']
    search_fields = ['user__username', 'tutorial__title']
    readonly_fields = ['started_at', 'last_accessed', 'completed_at']
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            return self.readonly_fields + ['user', 'tutorial']
        return self.readonly_fields


@admin.register(TutorialRating)
class TutorialRatingAdmin(admin.ModelAdmin):
    list_display = ['tutorial', 'user', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['tutorial__title', 'user__username', 'review']
    readonly_fields = ['created_at']
