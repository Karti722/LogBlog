import openai
from django.conf import settings
from .models import Tutorial, TutorialStep, TutorialCategory, AITutorialRequest
from django.utils.text import slugify
import json
import logging

logger = logging.getLogger(__name__)


class AITutorialGenerator:
    def __init__(self):
        self.client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
    
    def generate_tutorial(self, request_obj):
        """Generate a complete tutorial using OpenAI GPT"""
        try:
            # Update request status
            request_obj.status = 'processing'
            request_obj.save()
            
            # Create the prompt for OpenAI
            prompt = self._create_tutorial_prompt(
                request_obj.topic,
                request_obj.description,
                request_obj.difficulty
            )
            
            # Call OpenAI API
            response = self.client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {"role": "system", "content": "You are an expert technical writer and educator who creates comprehensive, step-by-step tutorials for building blogs and web applications."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=4000,
                temperature=0.7
            )
            
            # Parse the response
            tutorial_data = self._parse_tutorial_response(response.choices[0].message.content)
            
            # Create tutorial in database
            tutorial = self._create_tutorial_from_data(tutorial_data, request_obj)
            
            # Update request status
            request_obj.status = 'completed'
            request_obj.generated_tutorial = tutorial
            request_obj.save()
            
            return tutorial
            
        except Exception as e:
            logger.error(f"Error generating tutorial: {str(e)}")
            request_obj.status = 'failed'
            request_obj.error_message = str(e)
            request_obj.save()
            raise
    
    def _create_tutorial_prompt(self, topic, description, difficulty):
        """Create a detailed prompt for OpenAI"""
        prompt = f"""
        Create a comprehensive tutorial on "{topic}" for {difficulty} level developers.
        
        {f"Additional context: {description}" if description else ""}
        
        Please provide a detailed tutorial with the following structure:
        
        1. Tutorial Title
        2. Brief Description (2-3 sentences)
        3. Estimated Duration (in minutes)
        4. Prerequisites (if any)
        5. Step-by-step instructions (minimum 5 steps, maximum 15 steps)
        
        For each step, include:
        - Step title
        - Detailed explanation
        - Code examples (if applicable)
        - Best practices or tips
        
        Focus on practical, hands-on learning with real-world examples.
        Make sure the tutorial is actionable and includes all necessary code snippets.
        
        Format your response as a JSON object with this structure:
        {{
            "title": "Tutorial Title",
            "description": "Brief description",
            "estimated_duration": 30,
            "prerequisites": ["prerequisite1", "prerequisite2"],
            "steps": [
                {{
                    "title": "Step Title",
                    "content": "Detailed explanation",
                    "code_example": "Optional code example"
                }}
            ]
        }}
        
        Topic: {topic}
        Difficulty: {difficulty}
        """
        return prompt
    
    def _parse_tutorial_response(self, response_text):
        """Parse OpenAI response and extract tutorial data"""
        try:
            # Try to find JSON in the response
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1
            
            if start_idx != -1 and end_idx != -1:
                json_str = response_text[start_idx:end_idx]
                return json.loads(json_str)
            else:
                # If no JSON found, create a basic structure
                return self._create_fallback_tutorial_data(response_text)
                
        except json.JSONDecodeError:
            # Fallback to parsing text manually
            return self._create_fallback_tutorial_data(response_text)
    
    def _create_fallback_tutorial_data(self, text):
        """Create tutorial data from plain text response"""
        lines = text.split('\n')
        title = lines[0].strip() if lines else "Generated Tutorial"
        
        return {
            "title": title,
            "description": "AI-generated tutorial created from your request.",
            "estimated_duration": 30,
            "prerequisites": [],
            "steps": [
                {
                    "title": "Getting Started",
                    "content": text,
                    "code_example": ""
                }
            ]
        }
    
    def _create_tutorial_from_data(self, data, request_obj):
        """Create Tutorial and TutorialStep objects from parsed data"""
        # Get or create category
        category, created = TutorialCategory.objects.get_or_create(
            name="AI Generated Tutorials",
            defaults={
                "description": "Tutorials automatically generated by AI",
                "icon": "fas fa-robot"
            }
        )
        
        # Create tutorial
        tutorial = Tutorial.objects.create(
            title=data['title'],
            slug=slugify(data['title']),
            category=category,
            description=data.get('description', ''),
            difficulty=request_obj.difficulty,
            estimated_duration=data.get('estimated_duration', 30),
            is_ai_generated=True
        )
        
        # Create tutorial steps
        for idx, step_data in enumerate(data.get('steps', []), 1):
            TutorialStep.objects.create(
                tutorial=tutorial,
                title=step_data.get('title', f'Step {idx}'),
                content=step_data.get('content', ''),
                code_example=step_data.get('code_example', ''),
                step_number=idx
            )
        
        return tutorial
    
    def get_tutorial_suggestions(self, topic):
        """Get AI-powered tutorial suggestions based on a topic"""
        try:
            prompt = f"""
            Based on the topic "{topic}", suggest 5 related tutorial topics that would be helpful for someone learning about blog development and web applications.
            
            Provide suggestions in JSON format:
            {{
                "suggestions": [
                    {{
                        "title": "Tutorial Title",
                        "description": "Brief description",
                        "difficulty": "beginner|intermediate|advanced",
                        "estimated_duration": 30
                    }}
                ]
            }}
            """
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that suggests relevant tutorials."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000,
                temperature=0.5
            )
            
            suggestions_text = response.choices[0].message.content
            start_idx = suggestions_text.find('{')
            end_idx = suggestions_text.rfind('}') + 1
            
            if start_idx != -1 and end_idx != -1:
                json_str = suggestions_text[start_idx:end_idx]
                return json.loads(json_str)
            
            return {"suggestions": []}
            
        except Exception as e:
            logger.error(f"Error getting tutorial suggestions: {str(e)}")
            return {"suggestions": []}
