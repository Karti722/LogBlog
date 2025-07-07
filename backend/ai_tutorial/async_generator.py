import threading
import time
import logging
from django.utils import timezone
from .models import AITutorialRequest
from .services import AITutorialGenerator

logger = logging.getLogger(__name__)

class ThreadedTutorialGenerator:
    """
    A simple threaded approach to generate tutorials without requiring Celery/Redis
    """
    
    def __init__(self):
        self.active_tasks = {}
    
    def generate_tutorial_async(self, request_id):
        """Generate tutorial in a separate thread"""
        def _generate():
            try:
                # Get the tutorial request
                tutorial_request = AITutorialRequest.objects.get(id=request_id)
                
                # Update status to processing
                tutorial_request.status = 'processing'
                tutorial_request.save()
                
                # Generate tutorial
                generator = AITutorialGenerator()
                tutorial = generator.generate_tutorial(tutorial_request)
                
                # Remove from active tasks
                if request_id in self.active_tasks:
                    del self.active_tasks[request_id]
                
                logger.info(f"Successfully generated tutorial: {tutorial.title}")
                
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
                
                # Remove from active tasks
                if request_id in self.active_tasks:
                    del self.active_tasks[request_id]
        
        # Start the thread
        thread = threading.Thread(target=_generate)
        thread.daemon = True
        thread.start()
        
        # Store the thread reference
        self.active_tasks[request_id] = {
            'thread': thread,
            'started_at': timezone.now()
        }
        
        return thread
    
    def is_task_active(self, request_id):
        """Check if a task is still active"""
        if request_id in self.active_tasks:
            thread = self.active_tasks[request_id]['thread']
            return thread.is_alive()
        return False
    
    def get_active_tasks(self):
        """Get list of active task IDs"""
        # Clean up finished tasks
        finished_tasks = []
        for request_id, task_info in self.active_tasks.items():
            if not task_info['thread'].is_alive():
                finished_tasks.append(request_id)
        
        for request_id in finished_tasks:
            del self.active_tasks[request_id]
        
        return list(self.active_tasks.keys())

# Global instance
threaded_generator = ThreadedTutorialGenerator()
