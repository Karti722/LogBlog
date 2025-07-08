from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import os
import json
from datetime import datetime

@require_http_methods(["GET"])
@csrf_exempt
def health_check(request):
    """
    Health check endpoint for monitoring and deployment verification
    """
    try:
        # Check database connection
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            db_status = "healthy"
    except Exception as e:
        db_status = f"unhealthy: {str(e)}"
    
    # Check ML models
    try:
        ml_model_path = getattr(settings, 'ML_MODEL_PATH', 'ai_tutorial/models/')
        if not os.path.isabs(ml_model_path):
            ml_model_path = os.path.join(settings.BASE_DIR, ml_model_path)
        
        required_files = ['encoder.pth', 'decoder.pth', 'vectorizer.pkl', 'tutorial_templates.json']
        missing_files = []
        
        for file_name in required_files:
            file_path = os.path.join(ml_model_path, file_name)
            if not os.path.exists(file_path):
                missing_files.append(file_name)
        
        if missing_files:
            ml_status = f"missing files: {', '.join(missing_files)}"
        else:
            ml_status = "healthy"
    except Exception as e:
        ml_status = f"error: {str(e)}"
    
    # System info
    health_data = {
        "status": "healthy" if db_status == "healthy" and "healthy" in ml_status else "unhealthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0",
        "components": {
            "database": db_status,
            "ml_models": ml_status,
            "ml_generator_enabled": getattr(settings, 'USE_ML_GENERATOR', False),
        },
        "environment": {
            "debug": settings.DEBUG,
            "ml_device": getattr(settings, 'ML_DEVICE', 'auto'),
        }
    }
    
    status_code = 200 if health_data["status"] == "healthy" else 503
    return JsonResponse(health_data, status=status_code)


@require_http_methods(["GET"])
@csrf_exempt
def readiness_check(request):
    """
    Readiness check endpoint for deployment verification
    """
    try:
        # Quick database test
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        
        # Check if ML models are available
        ml_model_path = getattr(settings, 'ML_MODEL_PATH', 'ai_tutorial/models/')
        if not os.path.isabs(ml_model_path):
            ml_model_path = os.path.join(settings.BASE_DIR, ml_model_path)
        
        encoder_path = os.path.join(ml_model_path, 'encoder.pth')
        ready = os.path.exists(encoder_path)
        
        return JsonResponse({
            "ready": ready,
            "timestamp": datetime.now().isoformat(),
            "ml_models_available": ready
        }, status=200 if ready else 503)
        
    except Exception as e:
        return JsonResponse({
            "ready": False,
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }, status=503)
