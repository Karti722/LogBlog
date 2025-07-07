import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import json
import pickle
import os
from sentence_transformers import SentenceTransformer
import logging

logger = logging.getLogger(__name__)


class TutorialDataset(Dataset):
    """Custom Dataset for tutorial generation"""
    
    def __init__(self, topics, descriptions, difficulties, tutorials):
        self.topics = topics
        self.descriptions = descriptions
        self.difficulties = difficulties
        self.tutorials = tutorials
    
    def __len__(self):
        return len(self.topics)
    
    def __getitem__(self, idx):
        return {
            'topic': self.topics[idx],
            'description': self.descriptions[idx],
            'difficulty': self.difficulties[idx],
            'tutorial': self.tutorials[idx]
        }


class TutorialEncoder(nn.Module):
    """Neural network for encoding tutorial requests"""
    
    def __init__(self, input_size=768, hidden_size=512, output_size=256):
        super(TutorialEncoder, self).__init__()
        self.encoder = nn.Sequential(
            nn.Linear(input_size, hidden_size),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(hidden_size, hidden_size),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(hidden_size, output_size),
            nn.Tanh()
        )
    
    def forward(self, x):
        return self.encoder(x)


class TutorialDecoder(nn.Module):
    """Neural network for decoding tutorial content"""
    
    def __init__(self, input_size=256, hidden_size=512, vocab_size=10000):
        super(TutorialDecoder, self).__init__()
        self.hidden_size = hidden_size
        self.embedding = nn.Embedding(vocab_size, hidden_size)
        self.lstm = nn.LSTM(hidden_size, hidden_size, batch_first=True)
        self.attention = nn.Linear(hidden_size + input_size, hidden_size)
        self.output_projection = nn.Linear(hidden_size, vocab_size)
        self.dropout = nn.Dropout(0.3)
    
    def forward(self, context, target_seq=None):
        if target_seq is not None:
            embedded = self.embedding(target_seq)
            lstm_out, _ = self.lstm(embedded)
            
            # Expand context to match sequence length
            context_expanded = context.unsqueeze(1).expand(-1, lstm_out.size(1), -1)
            
            # Attention mechanism
            attention_input = torch.cat([lstm_out, context_expanded], dim=2)
            attention_weights = torch.softmax(self.attention(attention_input), dim=2)
            
            output = self.output_projection(self.dropout(attention_weights))
            return output
        else:
            # Generation mode
            batch_size = context.size(0)
            hidden = (torch.zeros(1, batch_size, self.hidden_size),
                     torch.zeros(1, batch_size, self.hidden_size))
            
            outputs = []
            input_token = torch.zeros(batch_size, 1, dtype=torch.long)
            
            for _ in range(200):  # Maximum sequence length
                embedded = self.embedding(input_token)
                lstm_out, hidden = self.lstm(embedded, hidden)
                
                # Apply attention
                context_expanded = context.unsqueeze(1)
                attention_input = torch.cat([lstm_out, context_expanded], dim=2)
                attention_weights = torch.softmax(self.attention(attention_input), dim=2)
                
                output = self.output_projection(self.dropout(attention_weights))
                outputs.append(output)
                
                input_token = torch.argmax(output, dim=2)
            
            return torch.cat(outputs, dim=1)


class MLTutorialGenerator:
    """Main ML-based tutorial generator"""
    
    def __init__(self, model_path='backend/ai_tutorial/models/'):
        self.model_path = model_path
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        
        # Initialize components
        self.sentence_transformer = SentenceTransformer('all-MiniLM-L6-v2')
        self.vectorizer = None
        self.encoder = None
        self.decoder = None
        self.tutorial_templates = None
        
        # Load or create models
        self._load_or_create_models()
    
    def _load_or_create_models(self):
        """Load existing models or create new ones"""
        try:
            self._load_models()
            logger.info("ML models loaded successfully")
        except (FileNotFoundError, Exception) as e:
            logger.warning(f"Could not load models: {e}")
            logger.info("Creating new ML models with sample data")
            self._create_and_train_models()
    
    def _load_models(self):
        """Load pre-trained models"""
        if not os.path.exists(self.model_path):
            raise FileNotFoundError("Model directory not found")
        
        # Load vectorizer
        with open(os.path.join(self.model_path, 'vectorizer.pkl'), 'rb') as f:
            self.vectorizer = pickle.load(f)
        
        # Load neural networks
        self.encoder = TutorialEncoder().to(self.device)
        self.decoder = TutorialDecoder().to(self.device)
        
        encoder_path = os.path.join(self.model_path, 'encoder.pth')
        decoder_path = os.path.join(self.model_path, 'decoder.pth')
        
        if os.path.exists(encoder_path) and os.path.exists(decoder_path):
            self.encoder.load_state_dict(torch.load(encoder_path, map_location=self.device))
            self.decoder.load_state_dict(torch.load(decoder_path, map_location=self.device))
        
        # Load tutorial templates
        with open(os.path.join(self.model_path, 'tutorial_templates.json'), 'r') as f:
            self.tutorial_templates = json.load(f)
    
    def _create_and_train_models(self):
        """Create and train models with sample data"""
        # Create sample training data
        sample_data = self._create_sample_data()
        
        # Create directories
        os.makedirs(self.model_path, exist_ok=True)
        
        # Train vectorizer
        self._train_vectorizer(sample_data)
        
        # Train neural networks
        self._train_neural_networks(sample_data)
        
        # Save models
        self._save_models()
    
    def _create_sample_data(self):
        """Create comprehensive sample training data"""
        sample_tutorials = [
            {
                'topic': 'Django REST API',
                'description': 'Build a RESTful API with Django',
                'difficulty': 'intermediate',
                'tutorial': {
                    'title': 'Building a Django REST API',
                    'description': 'Learn to create a robust RESTful API using Django REST Framework',
                    'duration': 45,
                    'prerequisites': ['Python basics', 'Django fundamentals'],
                    'steps': [
                        {
                            'title': 'Set up Django project',
                            'content': 'Create a new Django project and install Django REST Framework',
                            'code': 'django-admin startproject myapi\ncd myapi\npip install djangorestframework'
                        },
                        {
                            'title': 'Create API models',
                            'content': 'Define your data models for the API',
                            'code': 'from django.db import models\n\nclass Post(models.Model):\n    title = models.CharField(max_length=200)\n    content = models.TextField()'
                        },
                        {
                            'title': 'Create serializers',
                            'content': 'Create serializers to convert model instances to JSON',
                            'code': 'from rest_framework import serializers\nfrom .models import Post\n\nclass PostSerializer(serializers.ModelSerializer):\n    class Meta:\n        model = Post\n        fields = "__all__"'
                        },
                        {
                            'title': 'Create API views',
                            'content': 'Build views to handle HTTP requests',
                            'code': 'from rest_framework import viewsets\nfrom .models import Post\nfrom .serializers import PostSerializer\n\nclass PostViewSet(viewsets.ModelViewSet):\n    queryset = Post.objects.all()\n    serializer_class = PostSerializer'
                        },
                        {
                            'title': 'Configure URLs',
                            'content': 'Set up URL routing for your API endpoints',
                            'code': 'from django.urls import path, include\nfrom rest_framework.routers import DefaultRouter\nfrom . import views\n\nrouter = DefaultRouter()\nrouter.register(r"posts", views.PostViewSet)\n\nurlpatterns = [\n    path("api/", include(router.urls)),\n]'
                        }
                    ]
                }
            },
            {
                'topic': 'React Components',
                'description': 'Create reusable React components',
                'difficulty': 'beginner',
                'tutorial': {
                    'title': 'Building Reusable React Components',
                    'description': 'Learn to create modular and reusable React components',
                    'duration': 30,
                    'prerequisites': ['JavaScript basics', 'React fundamentals'],
                    'steps': [
                        {
                            'title': 'Create functional component',
                            'content': 'Start with a simple functional component',
                            'code': 'import React from "react";\n\nfunction Button({ text, onClick }) {\n  return (\n    <button onClick={onClick}>\n      {text}\n    </button>\n  );\n}\n\nexport default Button;'
                        },
                        {
                            'title': 'Add PropTypes',
                            'content': 'Define prop types for better development experience',
                            'code': 'import PropTypes from "prop-types";\n\nButton.propTypes = {\n  text: PropTypes.string.isRequired,\n  onClick: PropTypes.func.isRequired,\n};'
                        },
                        {
                            'title': 'Add styling',
                            'content': 'Style your component with CSS modules or styled-components',
                            'code': 'import styles from "./Button.module.css";\n\nfunction Button({ text, onClick, variant = "primary" }) {\n  return (\n    <button \n      className={`${styles.button} ${styles[variant]}`}\n      onClick={onClick}\n    >\n      {text}\n    </button>\n  );\n}'
                        }
                    ]
                }
            },
            {
                'topic': 'Python Data Analysis',
                'description': 'Analyze data with pandas and matplotlib',
                'difficulty': 'intermediate',
                'tutorial': {
                    'title': 'Python Data Analysis with Pandas',
                    'description': 'Learn to analyze and visualize data using pandas and matplotlib',
                    'duration': 60,
                    'prerequisites': ['Python basics', 'NumPy knowledge'],
                    'steps': [
                        {
                            'title': 'Import libraries',
                            'content': 'Import necessary libraries for data analysis',
                            'code': 'import pandas as pd\nimport numpy as np\nimport matplotlib.pyplot as plt\nimport seaborn as sns'
                        },
                        {
                            'title': 'Load data',
                            'content': 'Load your dataset into a pandas DataFrame',
                            'code': 'df = pd.read_csv("data.csv")\nprint(df.head())\nprint(df.info())'
                        },
                        {
                            'title': 'Clean data',
                            'content': 'Handle missing values and clean your dataset',
                            'code': '# Check for missing values\nprint(df.isnull().sum())\n\n# Fill missing values\ndf.fillna(df.mean(), inplace=True)\n\n# Remove duplicates\ndf.drop_duplicates(inplace=True)'
                        },
                        {
                            'title': 'Analyze data',
                            'content': 'Perform basic statistical analysis',
                            'code': '# Basic statistics\nprint(df.describe())\n\n# Correlation matrix\ncorr_matrix = df.corr()\nprint(corr_matrix)'
                        },
                        {
                            'title': 'Visualize data',
                            'content': 'Create visualizations to understand your data',
                            'code': '# Create plots\nplt.figure(figsize=(10, 6))\nplt.subplot(1, 2, 1)\nplt.hist(df["column1"], bins=30)\nplt.title("Distribution of Column1")\n\nplt.subplot(1, 2, 2)\nplt.scatter(df["column1"], df["column2"])\nplt.title("Column1 vs Column2")\n\nplt.tight_layout()\nplt.show()'
                        }
                    ]
                }
            },
            {
                'topic': 'Machine Learning',
                'description': 'Build a machine learning model',
                'difficulty': 'advanced',
                'tutorial': {
                    'title': 'Building Your First Machine Learning Model',
                    'description': 'Create a machine learning model using scikit-learn',
                    'duration': 90,
                    'prerequisites': ['Python', 'NumPy', 'Pandas', 'Statistics'],
                    'steps': [
                        {
                            'title': 'Import libraries',
                            'content': 'Import necessary machine learning libraries',
                            'code': 'import pandas as pd\nimport numpy as np\nfrom sklearn.model_selection import train_test_split\nfrom sklearn.linear_model import LinearRegression\nfrom sklearn.metrics import mean_squared_error, r2_score\nimport matplotlib.pyplot as plt'
                        },
                        {
                            'title': 'Prepare data',
                            'content': 'Load and prepare your dataset for training',
                            'code': '# Load data\ndf = pd.read_csv("dataset.csv")\n\n# Define features and target\nX = df.drop("target", axis=1)\ny = df["target"]\n\n# Split data\nX_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)'
                        },
                        {
                            'title': 'Train model',
                            'content': 'Create and train your machine learning model',
                            'code': '# Create model\nmodel = LinearRegression()\n\n# Train model\nmodel.fit(X_train, y_train)\n\n# Make predictions\ny_pred = model.predict(X_test)'
                        },
                        {
                            'title': 'Evaluate model',
                            'content': 'Assess your model\'s performance',
                            'code': '# Calculate metrics\nmse = mean_squared_error(y_test, y_pred)\nr2 = r2_score(y_test, y_pred)\n\nprint(f"Mean Squared Error: {mse:.2f}")\nprint(f"R² Score: {r2:.2f}")\n\n# Plot results\nplt.scatter(y_test, y_pred)\nplt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], "r--")\nplt.xlabel("Actual")\nplt.ylabel("Predicted")\nplt.title("Actual vs Predicted")\nplt.show()'
                        }
                    ]
                }
            }
        ]
        
        return sample_tutorials
    
    def _train_vectorizer(self, sample_data):
        """Train TF-IDF vectorizer"""
        texts = []
        for item in sample_data:
            text = f"{item['topic']} {item['description']} {item['difficulty']}"
            texts.append(text)
        
        self.vectorizer = TfidfVectorizer(max_features=5000, stop_words='english')
        self.vectorizer.fit(texts)
    
    def _train_neural_networks(self, sample_data):
        """Train encoder and decoder networks"""
        # Initialize networks
        self.encoder = TutorialEncoder().to(self.device)
        self.decoder = TutorialDecoder().to(self.device)
        
        # For this example, we'll use a simple similarity-based approach
        # In a real implementation, you'd train these networks with proper data
        self.encoder.eval()
        self.decoder.eval()
        
        # Store tutorial templates for similarity matching
        self.tutorial_templates = sample_data
    
    def _save_models(self):
        """Save trained models"""
        # Save vectorizer
        with open(os.path.join(self.model_path, 'vectorizer.pkl'), 'wb') as f:
            pickle.dump(self.vectorizer, f)
        
        # Save neural networks
        torch.save(self.encoder.state_dict(), os.path.join(self.model_path, 'encoder.pth'))
        torch.save(self.decoder.state_dict(), os.path.join(self.model_path, 'decoder.pth'))
        
        # Save tutorial templates
        with open(os.path.join(self.model_path, 'tutorial_templates.json'), 'w') as f:
            json.dump(self.tutorial_templates, f, indent=2)
    
    def generate_tutorial(self, topic, description, difficulty):
        """Generate tutorial using ML models"""
        try:
            # Create input text
            input_text = f"{topic} {description} {difficulty}"
            
            # Get sentence embedding
            input_embedding = self.sentence_transformer.encode([input_text])
            
            # Find most similar tutorial template
            best_match = self._find_best_match(topic, description, difficulty)
            
            # Generate tutorial based on best match
            generated_tutorial = self._generate_from_template(best_match, topic, description, difficulty)
            
            return generated_tutorial
            
        except Exception as e:
            logger.error(f"Error generating tutorial: {e}")
            return self._get_fallback_tutorial(topic, description, difficulty)
    
    def _find_best_match(self, topic, description, difficulty):
        """Find the most similar tutorial template"""
        input_text = f"{topic} {description} {difficulty}"
        input_embedding = self.sentence_transformer.encode([input_text])
        
        best_score = 0
        best_match = None
        
        for template in self.tutorial_templates:
            template_text = f"{template['topic']} {template['description']} {template['difficulty']}"
            template_embedding = self.sentence_transformer.encode([template_text])
            
            similarity = cosine_similarity(input_embedding, template_embedding)[0][0]
            
            if similarity > best_score:
                best_score = similarity
                best_match = template
        
        return best_match if best_match else self.tutorial_templates[0]
    
    def _generate_from_template(self, template, topic, description, difficulty):
        """Generate tutorial from template"""
        # Customize the template based on input
        tutorial = template['tutorial'].copy()
        
        # Customize title and description
        tutorial['title'] = f"Learning {topic}"
        tutorial['description'] = description or f"A comprehensive guide to {topic}"
        
        # Adjust difficulty-based duration
        difficulty_multipliers = {'beginner': 0.8, 'intermediate': 1.0, 'advanced': 1.5}
        base_duration = tutorial.get('duration', 30)
        tutorial['duration'] = int(base_duration * difficulty_multipliers.get(difficulty, 1.0))
        
        # Customize steps based on topic
        if 'steps' in tutorial:
            tutorial['steps'] = self._customize_steps(tutorial['steps'], topic, difficulty)
        
        return tutorial
    
    def _customize_steps(self, steps, topic, difficulty):
        """Customize tutorial steps based on topic and difficulty"""
        customized_steps = []
        
        for step in steps:
            customized_step = step.copy()
            
            # Add topic-specific content
            if topic.lower() in customized_step['content'].lower():
                customized_step['content'] = customized_step['content'].replace(
                    topic, f"**{topic}**"
                )
            
            # Add difficulty-specific notes
            if difficulty == 'beginner':
                customized_step['content'] += "\n\n💡 **Beginner Tip**: Take your time with this step and don't hesitate to refer to documentation."
            elif difficulty == 'advanced':
                customized_step['content'] += "\n\n🚀 **Advanced Note**: Consider optimization and best practices for production use."
            
            customized_steps.append(customized_step)
        
        return customized_steps
    
    def _get_fallback_tutorial(self, topic, description, difficulty):
        """Return a fallback tutorial if generation fails"""
        return {
            'title': f"Introduction to {topic}",
            'description': description or f"Learn the basics of {topic}",
            'duration': 30,
            'prerequisites': ['Basic programming knowledge'],
            'steps': [
                {
                    'title': 'Getting Started',
                    'content': f'Begin your journey with {topic}',
                    'code': '# Your first step in learning ' + topic
                },
                {
                    'title': 'Basic Concepts',
                    'content': f'Understand the fundamental concepts of {topic}',
                    'code': '# Explore the core principles'
                },
                {
                    'title': 'Practical Example',
                    'content': f'Apply what you\'ve learned with a hands-on example',
                    'code': '# Build something practical'
                },
                {
                    'title': 'Next Steps',
                    'content': f'Continue your learning journey with {topic}',
                    'code': '# Keep practicing and exploring'
                }
            ]
        }
