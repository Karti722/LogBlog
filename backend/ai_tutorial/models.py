from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class TutorialCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True, help_text="Font Awesome icon class")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Tutorial Categories"
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Tutorial(models.Model):
    DIFFICULTY_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    category = models.ForeignKey(TutorialCategory, on_delete=models.CASCADE, related_name='tutorials')
    description = models.TextField(max_length=500)
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='beginner')
    estimated_duration = models.PositiveIntegerField(help_text="Estimated time in minutes")
    is_ai_generated = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title


class TutorialStep(models.Model):
    tutorial = models.ForeignKey(Tutorial, on_delete=models.CASCADE, related_name='steps')
    title = models.CharField(max_length=200)
    content = models.TextField()
    code_example = models.TextField(blank=True, help_text="Code example for this step")
    step_number = models.PositiveIntegerField()
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['step_number']
        unique_together = ('tutorial', 'step_number')
    
    def __str__(self):
        return f"{self.tutorial.title} - Step {self.step_number}: {self.title}"


class AITutorialRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tutorial_requests')
    topic = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    difficulty = models.CharField(max_length=20, choices=Tutorial.DIFFICULTY_CHOICES, default='beginner')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    generated_tutorial = models.ForeignKey(Tutorial, on_delete=models.SET_NULL, null=True, blank=True)
    error_message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Tutorial request: {self.topic} by {self.user.username}"


class UserTutorialProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tutorial_progress')
    tutorial = models.ForeignKey(Tutorial, on_delete=models.CASCADE, related_name='user_progress')
    completed_steps = models.JSONField(default=list, help_text="List of completed step IDs")
    progress_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    started_at = models.DateTimeField(auto_now_add=True)
    last_accessed = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        unique_together = ('user', 'tutorial')
    
    def __str__(self):
        return f"{self.user.username} - {self.tutorial.title} ({self.progress_percentage}%)"
    
    def update_progress(self):
        total_steps = self.tutorial.steps.count()
        if total_steps > 0:
            self.progress_percentage = (len(self.completed_steps) / total_steps) * 100
            if self.progress_percentage >= 100 and not self.completed_at:
                self.completed_at = timezone.now()
        self.save()


class TutorialRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tutorial = models.ForeignKey(Tutorial, on_delete=models.CASCADE, related_name='ratings')
    rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)])
    review = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'tutorial')
    
    def __str__(self):
        return f"{self.user.username} rated {self.tutorial.title}: {self.rating}/5"
