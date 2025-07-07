from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils.text import slugify
from blog.models import Category, Tag, Post
from ai_tutorial.models import TutorialCategory, Tutorial, TutorialStep


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
        blog_tags = ['tutorial', 'beginner', 'advanced', 'tips', 'guide', 'javascript', 'python', 'django', 'react', 'css', 'api', 'backend', 'frontend', 'hooks', 'es6', 'rest', 'grid', 'responsive']
        
        for tag_name in blog_tags:
            tag, created = Tag.objects.get_or_create(name=tag_name)
            if created:
                self.stdout.write(f'Created blog tag: {tag_name}')
        
        # Create comprehensive sample blog posts
        sample_posts = [
            {
                'title': 'Getting Started with Django Web Development',
                'content': 'Django is a high-level Python web framework that encourages rapid development and clean, pragmatic design. In this comprehensive tutorial, we will walk through the basics of setting up a Django project and creating your first web application. Django follows the model-view-template (MVT) architectural pattern and is designed to help developers build web applications quickly and efficiently. Key features include an admin interface, ORM for database operations, URL routing, template system, and built-in security features. To get started, install Django using pip, create a new project, and explore the project structure. Django projects are organized into apps, each serving a specific purpose. Learn about models for data structure, views for business logic, and templates for presentation. Run the development server to see your application in action. Django provides excellent documentation and is perfect for building complex web applications.',
                'excerpt': 'Learn the fundamentals of Django web development and create your first web application with this comprehensive guide.',
                'category': 'Django',
                'tags': ['tutorial', 'beginner', 'django', 'python'],
                'is_featured': True
            },
            {
                'title': 'Modern JavaScript ES6+ Features You Should Know',
                'content': 'JavaScript has evolved significantly with ES6 and later versions introducing powerful features that make code more expressive and easier to work with. Arrow functions provide concise syntax and different this behavior. Destructuring allows extracting values from arrays and objects. Template literals enable string interpolation and multi-line strings. Spread and rest operators help with array and object manipulation. Async/await makes promise handling more readable. Classes introduce familiar OOP syntax. Modules enable code organization across files. Default parameters make functions more robust. These features improve code quality, readability, and maintainability. Modern JavaScript development heavily relies on these features for building scalable applications.',
                'excerpt': 'Discover the modern JavaScript features that will improve your code quality and developer experience.',
                'category': 'JavaScript',
                'tags': ['javascript', 'es6', 'tutorial', 'advanced'],
                'is_featured': True
            },
            {
                'title': 'Building Responsive Layouts with CSS Grid',
                'content': 'CSS Grid is a powerful two-dimensional layout system that excels at creating complex, responsive layouts. Unlike Flexbox which is one-dimensional, Grid works with rows and columns simultaneously. Basic setup involves display: grid with grid-template-columns and rows. The fr unit represents fractional space distribution. Grid template areas allow semantic layout definitions with named regions. Responsive design becomes straightforward with auto-fit, auto-fill, and minmax functions. Advanced techniques include explicit vs implicit grids, grid line names, and fractional units. Grid is perfect for magazine layouts, card grids, and complex responsive designs. It has excellent browser support with fallback options for older browsers. Performance tips include using grid-template-areas for readability and combining Grid with Flexbox when needed.',
                'excerpt': 'Learn how to create beautiful, responsive layouts using CSS Grid with practical examples and real-world techniques.',
                'category': 'CSS',
                'tags': ['css', 'grid', 'responsive', 'tutorial'],
                'is_featured': False
            },
            {
                'title': 'React Hooks: A Complete Guide',
                'content': 'React Hooks revolutionized functional component development by providing access to state and lifecycle features. useState manages component state with array destructuring for current value and setter function. useEffect handles side effects, replacing lifecycle methods with cleanup capabilities. useContext accesses context without nesting Consumer components. useReducer manages complex state logic with reducer patterns. Custom hooks enable reusable stateful logic sharing between components. Performance optimization uses useMemo for expensive calculations and useCallback for function memoization. useRef provides DOM access and persistent values without re-renders. Hook rules require top-level calls in consistent order from React functions only. Best practices include multiple state variables, proper dependency arrays, and cleanup for side effects.',
                'excerpt': 'Master React Hooks with this comprehensive guide covering useState, useEffect, custom hooks, and performance optimization.',
                'category': 'React',
                'tags': ['react', 'hooks', 'tutorial', 'advanced'],
                'is_featured': True
            },
            {
                'title': 'Building RESTful APIs with Django REST Framework',
                'content': 'Django REST Framework (DRF) is a powerful toolkit for building Web APIs with features like serialization, authentication, permissions, and automatic documentation. Installation involves pip install and settings configuration for authentication, permissions, and pagination. Models should be well-structured with proper relationships and constraints. Serializers convert between complex data types and Python datatypes, handling validation. ModelSerializer automatically generates fields from models. ViewSets provide CRUD operations with minimal code. Authentication options include token-based and session authentication. Permissions control access with built-in and custom classes. Filtering, searching, and ordering enhance API functionality. Pagination handles large datasets efficiently. Automatic documentation provides interactive API browsers and schema generation. Testing ensures endpoint reliability and security. Performance optimization includes database query optimization, caching, and rate limiting.',
                'excerpt': 'Learn how to build powerful RESTful APIs using Django REST Framework with authentication, permissions, and best practices.',
                'category': 'Django',
                'tags': ['django', 'api', 'rest', 'tutorial', 'backend'],
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
                        'content': 'First, decide which platform to use for your blog. Popular options include WordPress, Django, or static site generators.',
                        'code_example': ''
                    },
                    {
                        'title': 'Set Up Your Environment',
                        'content': 'Install the necessary tools and dependencies for your chosen platform.',
                        'code_example': 'pip install django'
                    },
                    {
                        'title': 'Design Your Blog Layout',
                        'content': 'Create a clean, responsive design for your blog.',
                        'code_example': ''
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
