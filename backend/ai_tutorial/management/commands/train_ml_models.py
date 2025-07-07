from django.core.management.base import BaseCommand
from ai_tutorial.ml_models import MLTutorialGenerator
import os


class Command(BaseCommand):
    help = 'Train the ML-based tutorial generator'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force retrain even if models exist',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting ML model training...'))
        
        try:
            # Initialize the ML generator
            ml_generator = MLTutorialGenerator()
            
            # Check if models exist
            model_path = ml_generator.model_path
            if os.path.exists(model_path) and not options['force']:
                self.stdout.write(
                    self.style.WARNING(
                        f'Models already exist at {model_path}. Use --force to retrain.'
                    )
                )
                return
            
            # Train the models
            self.stdout.write('Training ML models with sample data...')
            ml_generator._create_and_train_models()
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'ML models trained successfully and saved to {model_path}'
                )
            )
            
            # Test the model
            self.stdout.write('Testing the trained model...')
            test_tutorial = ml_generator.generate_tutorial(
                topic='Python Testing',
                description='Learn how to test Python applications',
                difficulty='intermediate'
            )
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'Test tutorial generated: "{test_tutorial["title"]}"'
                )
            )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error training ML models: {str(e)}')
            )
            raise
