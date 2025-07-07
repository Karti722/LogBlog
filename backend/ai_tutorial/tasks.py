from celery import shared_task
from django.utils import timezone
import logging
from .models import AITutorialRequest, Tutorial
from .services import AITutorialGenerator

logger = logging.getLogger(__name__)

@shared_task(bind=True, max_retries=3)
def generate_tutorial_task(self, request_id):
    """
    Celery task to generate tutorial asynchronously
    """
    try:
        # Get the tutorial request
        tutorial_request = AITutorialRequest.objects.get(id=request_id)
        
        # Update status to processing
        tutorial_request.status = 'processing'
        tutorial_request.save()
        
        # Generate tutorial
        generator = AITutorialGenerator()
        tutorial = generator.generate_tutorial(tutorial_request)
        
        logger.info(f"Successfully generated tutorial: {tutorial.title}")
        return {
            'status': 'success',
            'tutorial_id': tutorial.id,
            'tutorial_title': tutorial.title
        }
        
    except AITutorialRequest.DoesNotExist:
        logger.error(f"Tutorial request with ID {request_id} not found")
        return {'status': 'error', 'message': 'Tutorial request not found'}
        
    except Exception as e:
        logger.error(f"Error generating tutorial: {str(e)}")
        
        # Update request status on failure
        try:
            tutorial_request = AITutorialRequest.objects.get(id=request_id)
            tutorial_request.status = 'failed'
            tutorial_request.error_message = str(e)
            tutorial_request.save()
        except AITutorialRequest.DoesNotExist:
            pass
        
        # Retry the task
        if self.request.retries < self.max_retries:
            logger.info(f"Retrying tutorial generation (attempt {self.request.retries + 1})")
            raise self.retry(countdown=60, exc=e)
        
        return {'status': 'error', 'message': str(e)}

@shared_task
def get_tutorial_suggestions_task(topic):
    """
    Celery task to get tutorial suggestions asynchronously
    """
    try:
        generator = AITutorialGenerator()
        suggestions = generator.get_tutorial_suggestions(topic)
        return {
            'status': 'success',
            'suggestions': suggestions
        }
    except Exception as e:
        logger.error(f"Error getting tutorial suggestions: {str(e)}")
        return {
            'status': 'error',
            'message': str(e)
        }
