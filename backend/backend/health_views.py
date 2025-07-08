from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import os
import json
from datetime import datetime
from django.db import connection
from django.core.cache import cache
import logging

logger = logging.getLogger(__name__)

@csrf_exempt
@require_http_methods(["GET"])
def health_check(request):
    """
    Health check endpoint for monitoring the application status
    Returns JSON response with system health information
    """
    health_data = {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0",
        "services": {},
        "ml_system": {
            "enabled": getattr(settings, 'USE_ML_GENERATOR', False),
            "model_path": getattr(settings, 'ML_MODEL_PATH', ''),
            "device": getattr(settings, 'ML_DEVICE', 'auto')
        }
    }
    
    # Check database connection
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        health_data["services"]["database"] = "healthy"
    except Exception as e:
        health_data["services"]["database"] = "unhealthy"
        health_data["status"] = "degraded"
        logger.error(f"Database health check failed: {e}")
    
    # Check ML models availability
    try:
        model_path = getattr(settings, 'ML_MODEL_PATH', '')
        if model_path:
            # Check if model files exist
            encoder_path = os.path.join(model_path, 'encoder.pth')
            decoder_path = os.path.join(model_path, 'decoder.pth')
            vectorizer_path = os.path.join(model_path, 'vectorizer.pkl')
            templates_path = os.path.join(model_path, 'tutorial_templates.json')
            
            if all(os.path.exists(path) for path in [encoder_path, decoder_path, vectorizer_path, templates_path]):
                health_data["services"]["ml_models"] = "healthy"
                health_data["ml_system"]["models_loaded"] = True
            else:
                health_data["services"]["ml_models"] = "models_missing"
                health_data["ml_system"]["models_loaded"] = False
                health_data["status"] = "degraded"
        else:
            health_data["services"]["ml_models"] = "path_not_configured"
            health_data["ml_system"]["models_loaded"] = False
    except Exception as e:
        health_data["services"]["ml_models"] = "unhealthy"
        health_data["ml_system"]["models_loaded"] = False
        health_data["status"] = "degraded"
        logger.error(f"ML models health check failed: {e}")
    
    # Check static files
    try:
        static_root = getattr(settings, 'STATIC_ROOT', '')
        if static_root and os.path.exists(static_root):
            health_data["services"]["static_files"] = "healthy"
        else:
            health_data["services"]["static_files"] = "not_configured"
    except Exception as e:
        health_data["services"]["static_files"] = "unhealthy"
        logger.error(f"Static files health check failed: {e}")
    
    # Overall status
    if health_data["status"] == "healthy":
        status_code = 200
    else:
        status_code = 503
    
    return JsonResponse(health_data, status=status_code)

@csrf_exempt
@require_http_methods(["GET"])
def readiness_check(request):
    """
    Readiness check endpoint for Kubernetes/container orchestration
    Returns 200 if the application is ready to serve requests
    """
    try:
        # Check database connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        
        # Check if ML models are available (if enabled)
        if getattr(settings, 'USE_ML_GENERATOR', False):
            model_path = getattr(settings, 'ML_MODEL_PATH', '')
            if model_path:
                required_files = [
                    'encoder.pth', 'decoder.pth', 
                    'vectorizer.pkl', 'tutorial_templates.json'
                ]
                
                for file_name in required_files:
                    file_path = os.path.join(model_path, file_name)
                    if not os.path.exists(file_path):
                        return JsonResponse(
                            {"status": "not_ready", "reason": f"ML model file missing: {file_name}"},
                            status=503
                        )
        
        return JsonResponse({"status": "ready"}, status=200)
    
    except Exception as e:
        logger.error(f"Readiness check failed: {e}")
        return JsonResponse(
            {"status": "not_ready", "reason": str(e)},
            status=503
        )

@csrf_exempt
@require_http_methods(["GET"])
def liveness_check(request):
    """
    Liveness check endpoint for Kubernetes/container orchestration
    Returns 200 if the application is alive (basic functionality)
    """
    return JsonResponse({
        "status": "alive",
        "timestamp": datetime.now().isoformat()
    }, status=200)
