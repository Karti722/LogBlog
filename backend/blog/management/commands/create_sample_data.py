from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils.text import slugify
from blog.models import Category, Tag, Post
from ai_tutorial.models import TutorialCategory, Tutorial, TutorialStep
import random


class Command(BaseCommand):
    help = 'Create sample data for the blog and AI tutorial apps'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Creating sample data...'))
        
        # Create superuser if not exists
        if not User.objects.filter(username='admin').exists():
            admin_user = User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='admin123'
            )
            self.stdout.write(self.style.SUCCESS('Created admin user'))
        else:
            admin_user = User.objects.get(username='admin')
        
        # Create sample users
        users = []
        for i in range(3):
            username = f'user{i+1}'
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(
                    username=username,
                    email=f'{username}@example.com',
                    password='password123',
                    first_name=f'User {i+1}',
                    last_name='Test'
                )
                users.append(user)
            else:
                users.append(User.objects.get(username=username))
        
        # Create blog categories
        blog_categories = [
            ('Web Development', 'All about web development, frameworks, and best practices'),
            ('JavaScript', 'JavaScript tutorials, tips, and tricks'),
            ('Django', 'Django framework tutorials and guides'),
            ('React', 'React.js tutorials and components'),
            ('CSS', 'CSS styling and design tutorials'),
        ]
        
        for name, description in blog_categories:
            category, created = Category.objects.get_or_create(
                name=name,
                defaults={'description': description}
            )
            if created:
                self.stdout.write(f'Created blog category: {name}')
        
        # Create blog tags
        blog_tags = ['tutorial', 'beginner', 'advanced', 'tips', 'guide', 'javascript', 'python', 'django', 'react', 'css']
        
        for tag_name in blog_tags:
            tag, created = Tag.objects.get_or_create(name=tag_name)
            if created:
                self.stdout.write(f'Created blog tag: {tag_name}')
        
        # Create sample blog posts
        sample_posts = [
            {
                'title': 'Getting Started with Django Web Development',
                'content': '''Django is a high-level Python web framework that encourages rapid development and clean, pragmatic design. In this tutorial, we'll walk through the basics of setting up a Django project and creating your first web application.
                
## What is Django?

Django is a free and open-source web framework written in Python. It follows the model-view-template (MVT) architectural pattern and is designed to help developers build web applications quickly and efficiently.

## Setting up Django

First, you'll need to install Django. You can do this using pip:

```bash
pip install django
```

Once installed, you can create a new Django project:

```bash
django-admin startproject myproject
cd myproject
```

## Creating Your First App

Django projects are organized into apps. Each app serves a specific purpose in your web application. To create an app:

```bash
python manage.py startapp myapp
```

This creates a new directory with the basic structure for your app.

## Running the Development Server

To see your Django application in action, run:

```bash
python manage.py runserver
```

Visit http://127.0.0.1:8000 in your browser to see the Django welcome page.

## Next Steps

From here, you can start building your models, views, and templates to create a fully functional web application. Django's documentation is excellent and provides detailed guidance on every aspect of the framework.''',
                'excerpt': 'Learn the fundamentals of Django web development and create your first web application.',
                'category': 'Django',
                'tags': ['tutorial', 'beginner', 'django', 'python'],
                'is_featured': True
            },
            {
                'title': 'Modern JavaScript ES6+ Features You Should Know',
                'content': '''JavaScript has evolved significantly over the years. ES6 (ECMAScript 2015) and later versions have introduced many powerful features that make JavaScript more expressive and easier to work with.

## Arrow Functions

Arrow functions provide a more concise way to write functions:

```javascript
// Traditional function
function add(a, b) {
    return a + b;
}

// Arrow function
const add = (a, b) => a + b;
```

## Destructuring

Destructuring allows you to extract values from arrays and objects:

```javascript
// Array destructuring
const [first, second] = [1, 2, 3];

// Object destructuring
const {name, age} = {name: 'John', age: 30};
```

## Template Literals

Template literals make string interpolation much easier:

```javascript
const name = 'World';
const greeting = `Hello, ${name}!`;
```

## Async/Await

Async/await makes working with promises much more readable:

```javascript
async function fetchData() {
    try {
        const response = await fetch('/api/data');
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error:', error);
    }
}
```

These features make JavaScript more powerful and enjoyable to work with.''',
                'excerpt': 'Discover the modern JavaScript features that will improve your code quality and developer experience.',
                'category': 'JavaScript',
                'tags': ['javascript', 'es6', 'tutorial', 'advanced'],
                'is_featured': True
            },
            {
                'title': 'Building Responsive Layouts with CSS Grid',
                'content': '''CSS Grid is a powerful layout system that makes it easy to create complex, responsive layouts with just a few lines of code.

## What is CSS Grid?

CSS Grid is a two-dimensional layout system that allows you to create layouts using rows and columns. It's perfect for creating complex layouts that adapt to different screen sizes.

## Basic Grid Setup

```css
.container {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    grid-template-rows: auto;
    gap: 20px;
}
```

## Responsive Design

CSS Grid makes responsive design straightforward:

```css
.container {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 20px;
}
```

This creates a responsive grid that automatically adjusts the number of columns based on the available space.

## Grid Areas

You can define named grid areas for more semantic layouts:

```css
.container {
    display: grid;
    grid-template-areas: 
        "header header header"
        "sidebar main main"
        "footer footer footer";
}

.header { grid-area: header; }
.sidebar { grid-area: sidebar; }
.main { grid-area: main; }
.footer { grid-area: footer; }
```

CSS Grid is an essential tool for modern web development.''',
                'excerpt': 'Learn how to create beautiful, responsive layouts using CSS Grid.',
                'category': 'CSS',
                'tags': ['css', 'grid', 'responsive', 'tutorial'],
                'is_featured': False
            }
        ]
        
        for post_data in sample_posts:
            if not Post.objects.filter(slug=slugify(post_data['title'])).exists():
                category = Category.objects.get(name=post_data['category'])
                post = Post.objects.create(
                    title=post_data['title'],
                    slug=slugify(post_data['title']),
                    author=admin_user,
                    content=post_data['content'],
                    excerpt=post_data['excerpt'],
                    category=category,
                    status='published',
                    is_featured=post_data['is_featured']
                )
                
                # Add tags
                for tag_name in post_data['tags']:
                    tag, created = Tag.objects.get_or_create(name=tag_name)
                    post.tags.add(tag)
                
                self.stdout.write(f'Created blog post: {post.title}')
        
        # Create tutorial categories
        tutorial_categories = [
            ('Web Development', 'Learn web development from scratch', 'fas fa-code'),
            ('Blog Creation', 'Tutorials on creating and managing blogs', 'fas fa-blog'),
            ('Frontend Development', 'HTML, CSS, JavaScript tutorials', 'fas fa-laptop-code'),
            ('Backend Development', 'Server-side programming tutorials', 'fas fa-server'),
            ('Deployment', 'Learn how to deploy your applications', 'fas fa-cloud'),
        ]
        
        for name, description, icon in tutorial_categories:
            category, created = TutorialCategory.objects.get_or_create(
                name=name,
                defaults={'description': description, 'icon': icon}
            )
            if created:
                self.stdout.write(f'Created tutorial category: {name}')
        
        # Create sample tutorials
        sample_tutorials = [
            {
                'title': 'How to Create Your First Blog',
                'category': 'Blog Creation',
                'description': 'A comprehensive guide to creating your first blog from scratch.',
                'difficulty': 'beginner',
                'estimated_duration': 45,
                'steps': [
                    {
                        'title': 'Choose Your Platform',
                        'content': 'First, you need to decide which platform to use for your blog. Popular options include WordPress, Django, or static site generators like Jekyll.',
                        'code_example': ''
                    },
                    {
                        'title': 'Set Up Your Environment',
                        'content': 'Install the necessary tools and dependencies for your chosen platform.',
                        'code_example': 'pip install django\ndjango-admin startproject myblog'
                    },
                    {
                        'title': 'Design Your Blog Layout',
                        'content': 'Create a clean, responsive design for your blog. Consider your audience and the type of content you\'ll be publishing.',
                        'code_example': ''
                    },
                    {
                        'title': 'Create Your First Post',
                        'content': 'Write your inaugural blog post. Make it engaging and give readers a taste of what to expect.',
                        'code_example': ''
                    },
                    {
                        'title': 'Deploy Your Blog',
                        'content': 'Make your blog live on the internet using platforms like Heroku, Netlify, or your own server.',
                        'code_example': 'git push heroku main'
                    }
                ]
            },
            {
                'title': 'Building a REST API with Django',
                'category': 'Backend Development',
                'description': 'Learn how to build a RESTful API using Django and Django REST Framework.',
                'difficulty': 'intermediate',
                'estimated_duration': 60,
                'steps': [
                    {
                        'title': 'Install Django REST Framework',
                        'content': 'First, install Django REST Framework and add it to your project.',
                        'code_example': 'pip install djangorestframework'
                    },
                    {
                        'title': 'Create Your Models',
                        'content': 'Define the data models for your API.',
                        'code_example': 'class Post(models.Model):\n    title = models.CharField(max_length=200)\n    content = models.TextField()'
                    },
                    {
                        'title': 'Create Serializers',
                        'content': 'Serializers define how your data is converted to and from JSON.',
                        'code_example': 'class PostSerializer(serializers.ModelSerializer):\n    class Meta:\n        model = Post\n        fields = \'__all__\''
                    },
                    {
                        'title': 'Create API Views',
                        'content': 'Define the views that handle API requests.',
                        'code_example': 'class PostViewSet(viewsets.ModelViewSet):\n    queryset = Post.objects.all()\n    serializer_class = PostSerializer'
                    },
                    {
                        'title': 'Configure URLs',
                        'content': 'Set up URL routing for your API endpoints.',
                        'code_example': 'router.register(r\'posts\', PostViewSet)'
                    }
                ]
            }
        ]
        
        for tutorial_data in sample_tutorials:
            if not Tutorial.objects.filter(slug=slugify(tutorial_data['title'])).exists():
                category = TutorialCategory.objects.get(name=tutorial_data['category'])
                tutorial = Tutorial.objects.create(
                    title=tutorial_data['title'],
                    slug=slugify(tutorial_data['title']),
                    category=category,
                    description=tutorial_data['description'],
                    difficulty=tutorial_data['difficulty'],
                    estimated_duration=tutorial_data['estimated_duration'],
                    is_ai_generated=False
                )
                
                # Create tutorial steps
                for idx, step_data in enumerate(tutorial_data['steps'], 1):
                    TutorialStep.objects.create(
                        tutorial=tutorial,
                        title=step_data['title'],
                        content=step_data['content'],
                        code_example=step_data['code_example'],
                        step_number=idx
                    )
                
                self.stdout.write(f'Created tutorial: {tutorial.title}')
        
        self.stdout.write(self.style.SUCCESS('Sample data created successfully!'))
        self.stdout.write(self.style.SUCCESS('Admin user: admin / admin123'))
        self.stdout.write(self.style.SUCCESS('Test users: user1, user2, user3 / password123'))
