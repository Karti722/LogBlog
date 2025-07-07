from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from blog.models import Post, Category, Tag
from django.utils import timezone
from django.utils.text import slugify


class Command(BaseCommand):
    help = 'Create sample blog data for testing'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample blog data...')

        # Create or get a user
        user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@example.com',
                'first_name': 'Admin',
                'last_name': 'User',
                'is_staff': True,
                'is_superuser': True
            }
        )
        if created:
            user.set_password('admin123')
            user.save()
            self.stdout.write(f'Created user: {user.username}')

        # Create categories
        categories_data = [
            {'name': 'Web Development', 'description': 'Frontend and backend web development tutorials'},
            {'name': 'JavaScript', 'description': 'JavaScript programming and frameworks'},
            {'name': 'Python', 'description': 'Python programming tutorials and tips'},
            {'name': 'React', 'description': 'React.js library and ecosystem'},
            {'name': 'CSS', 'description': 'CSS styling and design tutorials'},
            {'name': 'Node.js', 'description': 'Node.js backend development'},
            {'name': 'Database', 'description': 'Database design and management'},
        ]

        categories = []
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={
                    'description': cat_data['description']
                }
            )
            categories.append(category)
            if created:
                self.stdout.write(f'Created category: {category.name}')

        # Create tags
        tags_data = [
            'beginner', 'intermediate', 'advanced', 'tutorial', 'guide',
            'frontend', 'backend', 'fullstack', 'api', 'database',
            'responsive', 'mobile', 'performance', 'security', 'testing',
            'deployment', 'tools', 'best-practices', 'tips', 'tricks'
        ]

        tags = []
        for tag_name in tags_data:
            tag, created = Tag.objects.get_or_create(
                name=tag_name
            )
            tags.append(tag)
            if created:
                self.stdout.write(f'Created tag: {tag.name}')

        # Create sample blog posts
        posts_data = [
            {
                'title': 'Getting Started with React Hooks',
                'content': '''
React Hooks revolutionized how we write React components by allowing us to use state and other React features in functional components. In this comprehensive guide, we'll explore the most commonly used hooks and how to implement them effectively.

## What are React Hooks?

React Hooks are functions that let you "hook into" React state and lifecycle features from function components. They were introduced in React 16.8 and have since become the preferred way to write React components.

## useState Hook

The useState hook is the most fundamental hook for managing state in functional components:

```javascript
import React, { useState } from 'react';

function Counter() {
  const [count, setCount] = useState(0);

  return (
    <div>
      <p>You clicked {count} times</p>
      <button onClick={() => setCount(count + 1)}>
        Click me
      </button>
    </div>
  );
}
```

## useEffect Hook

The useEffect hook lets you perform side effects in function components. It's similar to componentDidMount, componentDidUpdate, and componentWillUnmount combined:

```javascript
import React, { useState, useEffect } from 'react';

function Example() {
  const [count, setCount] = useState(0);

  useEffect(() => {
    document.title = `You clicked ${count} times`;
  });

  return (
    <div>
      <p>You clicked {count} times</p>
      <button onClick={() => setCount(count + 1)}>
        Click me
      </button>
    </div>
  );
}
```

## Best Practices

1. **Always use hooks at the top level** - Don't call hooks inside loops, conditions, or nested functions
2. **Use multiple useEffect hooks** - Separate concerns by using multiple useEffect hooks for different purposes
3. **Optimize with dependencies** - Always include dependencies in the dependency array to avoid infinite loops

## Conclusion

React Hooks provide a powerful and flexible way to manage state and side effects in functional components. Start with useState and useEffect, then explore other hooks as your needs grow.
                ''',
                'excerpt': 'Learn how to use React Hooks effectively with practical examples and best practices.',
                'category': categories[3],  # React
                'tags': [tags[0], tags[3], tags[5]],  # beginner, tutorial, frontend
                'status': 'published',
                'is_featured': True
            },
            {
                'title': 'Python Web Development with Django',
                'content': '''
Django is a high-level Python web framework that encourages rapid development and clean, pragmatic design. In this tutorial, we'll build a complete web application from scratch.

## Setting Up Django

First, let's create a new Django project:

```bash
pip install django
django-admin startproject myproject
cd myproject
python manage.py runserver
```

## Creating Models

Models in Django represent your data structure:

```python
from django.db import models

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
```

## Views and Templates

Django follows the Model-View-Template (MVT) pattern:

```python
from django.shortcuts import render
from .models import BlogPost

def blog_list(request):
    posts = BlogPost.objects.all()
    return render(request, 'blog/list.html', {'posts': posts})
```

## URL Configuration

Define your URL patterns:

```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.blog_list, name='blog_list'),
]
```

## Conclusion

Django provides a robust framework for building web applications quickly and efficiently. Its batteries-included approach makes it perfect for both beginners and experienced developers.
                ''',
                'excerpt': 'Build web applications with Django - from models to deployment.',
                'category': categories[2],  # Python
                'tags': [tags[1], tags[3], tags[7]],  # intermediate, tutorial, backend
                'status': 'published',
                'is_featured': True
            },
            {
                'title': 'Modern CSS Grid Layout Techniques',
                'content': '''
CSS Grid is a powerful layout system that allows you to create complex, responsive layouts with ease. Let's explore advanced grid techniques that will transform your web designs.

## Basic Grid Setup

Start with a simple grid container:

```css
.grid-container {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  grid-gap: 20px;
}
```

## Advanced Grid Areas

Use named grid areas for complex layouts:

```css
.layout {
  display: grid;
  grid-template-areas:
    "header header header"
    "sidebar main main"
    "footer footer footer";
  grid-template-columns: 200px 1fr 1fr;
  grid-template-rows: auto 1fr auto;
}

.header { grid-area: header; }
.sidebar { grid-area: sidebar; }
.main { grid-area: main; }
.footer { grid-area: footer; }
```

## Responsive Grid

Create responsive grids without media queries:

```css
.responsive-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
}
```

## Grid Animations

Animate grid properties for smooth transitions:

```css
.grid-item {
  transition: all 0.3s ease;
}

.grid-item:hover {
  transform: scale(1.05);
}
```

## Conclusion

CSS Grid opens up new possibilities for web layout design. Master these techniques to create stunning, responsive layouts with minimal code.
                ''',
                'excerpt': 'Master CSS Grid with advanced techniques for modern web layouts.',
                'category': categories[4],  # CSS
                'tags': [tags[1], tags[3], tags[5], tags[10]],  # intermediate, tutorial, frontend, responsive
                'status': 'published',
                'is_featured': False
            }
        ]

        for post_data in posts_data:
            # Create slug from title
            slug = slugify(post_data['title'])
            
            # Check if post already exists
            if not Post.objects.filter(slug=slug).exists():
                post = Post.objects.create(
                    title=post_data['title'],
                    slug=slug,
                    content=post_data['content'],
                    excerpt=post_data['excerpt'],
                    author=user,
                    category=post_data['category'],
                    status=post_data['status'],
                    is_featured=post_data['is_featured'],
                    published_at=timezone.now() if post_data['status'] == 'published' else None
                )
                
                # Add tags
                post.tags.set(post_data['tags'])
                
                self.stdout.write(f'Created post: {post.title}')
            else:
                self.stdout.write(f'Post already exists: {post_data["title"]}')

        self.stdout.write(
            self.style.SUCCESS('Successfully created sample blog data!')
        )
