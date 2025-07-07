from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'tutorials', views.TutorialViewSet)
router.register(r'categories', views.TutorialCategoryViewSet)
router.register(r'requests', views.AITutorialRequestViewSet, basename='tutorial-request')

app_name = 'ai_tutorial'

urlpatterns = [
    path('api/', include(router.urls)),
]
