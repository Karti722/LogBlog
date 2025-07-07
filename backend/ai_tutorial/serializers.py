from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Tutorial, TutorialCategory, TutorialStep, AITutorialRequest, UserTutorialProgress, TutorialRating


class TutorialCategorySerializer(serializers.ModelSerializer):
    tutorials_count = serializers.SerializerMethodField()
    
    class Meta:
        model = TutorialCategory
        fields = ['id', 'name', 'description', 'icon', 'tutorials_count', 'created_at']
    
    def get_tutorials_count(self, obj):
        return obj.tutorials.count()


class TutorialStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = TutorialStep
        fields = ['id', 'title', 'content', 'code_example', 'step_number', 'is_completed']


class TutorialListSerializer(serializers.ModelSerializer):
    category = TutorialCategorySerializer(read_only=True)
    steps_count = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()
    user_progress = serializers.SerializerMethodField()
    
    class Meta:
        model = Tutorial
        fields = [
            'id', 'title', 'slug', 'category', 'description', 'difficulty',
            'estimated_duration', 'steps_count', 'average_rating', 'user_progress',
            'is_ai_generated', 'created_at', 'updated_at'
        ]
    
    def get_steps_count(self, obj):
        return obj.steps.count()
    
    def get_average_rating(self, obj):
        ratings = obj.ratings.all()
        if ratings:
            return sum(r.rating for r in ratings) / len(ratings)
        return 0.0
    
    def get_user_progress(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            try:
                progress = obj.user_progress.get(user=request.user)
                return {
                    'progress_percentage': float(progress.progress_percentage),
                    'completed_steps': progress.completed_steps,
                    'started_at': progress.started_at,
                    'last_accessed': progress.last_accessed,
                    'completed_at': progress.completed_at
                }
            except UserTutorialProgress.DoesNotExist:
                return None
        return None


class TutorialDetailSerializer(serializers.ModelSerializer):
    category = TutorialCategorySerializer(read_only=True)
    steps = TutorialStepSerializer(many=True, read_only=True)
    average_rating = serializers.SerializerMethodField()
    ratings_count = serializers.SerializerMethodField()
    user_progress = serializers.SerializerMethodField()
    user_rating = serializers.SerializerMethodField()
    
    class Meta:
        model = Tutorial
        fields = [
            'id', 'title', 'slug', 'category', 'description', 'difficulty',
            'estimated_duration', 'steps', 'average_rating', 'ratings_count',
            'user_progress', 'user_rating', 'is_ai_generated', 'created_at', 'updated_at'
        ]
    
    def get_average_rating(self, obj):
        ratings = obj.ratings.all()
        if ratings:
            return round(sum(r.rating for r in ratings) / len(ratings), 1)
        return 0.0
    
    def get_ratings_count(self, obj):
        return obj.ratings.count()
    
    def get_user_progress(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            try:
                progress = obj.user_progress.get(user=request.user)
                return {
                    'progress_percentage': float(progress.progress_percentage),
                    'completed_steps': progress.completed_steps,
                    'started_at': progress.started_at,
                    'last_accessed': progress.last_accessed,
                    'completed_at': progress.completed_at
                }
            except UserTutorialProgress.DoesNotExist:
                return None
        return None
    
    def get_user_rating(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            try:
                rating = obj.ratings.get(user=request.user)
                return {
                    'rating': rating.rating,
                    'review': rating.review,
                    'created_at': rating.created_at
                }
            except TutorialRating.DoesNotExist:
                return None
        return None


class AITutorialRequestSerializer(serializers.ModelSerializer):
    generated_tutorial = TutorialListSerializer(read_only=True)
    
    class Meta:
        model = AITutorialRequest
        fields = [
            'id', 'topic', 'description', 'difficulty', 'status',
            'generated_tutorial', 'error_message', 'created_at', 'completed_at'
        ]
        read_only_fields = ['status', 'generated_tutorial', 'error_message', 'completed_at']
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class TutorialProgressUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTutorialProgress
        fields = ['completed_steps']
    
    def update(self, instance, validated_data):
        instance.completed_steps = validated_data.get('completed_steps', instance.completed_steps)
        instance.update_progress()
        return instance


class TutorialRatingSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = TutorialRating
        fields = ['id', 'user', 'rating', 'review', 'created_at']
        read_only_fields = ['user']
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
