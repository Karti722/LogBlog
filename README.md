# LogBlog - AI-Powered Blog Tutorial Platform

LogBlog is a comprehensive web application that combines a modern blog platform with AI-powered tutorial generation. Built with Django (backend) and React (frontend), it provides users with educational content and personalized learning experiences.

## 🚀 Features

### Blog Platform
- **Modern Blog Interface**: Clean, responsive design with Tailwind CSS
- **Content Management**: Create, edit, and manage blog posts
- **Categories & Tags**: Organize content with categories and tags
- **User Engagement**: Like posts, comment system, and view tracking
- **Search & Filtering**: Advanced search and filtering capabilities

### AI Tutorial Generator
- **AI-Powered Tutorials**: Generate personalized tutorials using OpenAI GPT
- **Step-by-Step Learning**: Structured tutorials with code examples
- **Difficulty Levels**: Beginner, intermediate, and advanced content
- **Progress Tracking**: Track learning progress through tutorials
- **Tutorial Ratings**: Rate and review tutorials

### User Experience
- **Responsive Design**: Works seamlessly on desktop and mobile
- **Modern UI/UX**: Beautiful interface with smooth animations
- **Fast Performance**: Optimized with Vite and modern React
- **SEO Friendly**: Proper meta tags and semantic HTML

## 🛠 Technology Stack

### Backend
- **Django 5.2.4**: Web framework
- **Django REST Framework**: API development
- **PostgreSQL**: Database (via Supabase)
- **OpenAI API**: AI tutorial generation
- **CORS Headers**: Cross-origin resource sharing

### Frontend
- **React 19**: UI library
- **Vite**: Build tool and dev server
- **Tailwind CSS**: Utility-first CSS framework
- **React Router**: Client-side routing
- **Axios**: HTTP client
- **Heroicons**: Icon library

## 📦 Installation & Setup

### Prerequisites
- Python 3.12+
- Node.js 18+
- PostgreSQL database (Supabase account)
- OpenAI API key

### Backend Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd LogBlog
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv logenv
   # On Windows:
   .\logenv\Scripts\activate
   # On macOS/Linux:
   source logenv/bin/activate
   ```

3. **Install Python dependencies**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

4. **Environment Configuration**
   Create a `.env` file in the `backend` directory:
   ```env
   # Database Configuration
   DATABASE_URL=postgresql://username:password@host:port/database
   DIRECT_URL=postgresql://username:password@host:port/database
   
   # Django Configuration
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   
   # OpenAI Configuration
   OPENAI_API_KEY=your-openai-api-key-here
   ```

5. **Run database migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create sample data (optional)**
   ```bash
   python manage.py create_sample_data
   ```

7. **Start the Django server**
   ```bash
   python manage.py runserver
   ```

### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Install Node.js dependencies**
   ```bash
   npm install
   ```

3. **Start the development server**
   ```bash
   npm run dev
   ```

## 🚀 Usage

### Accessing the Application
- **Frontend**: http://localhost:5173
- **Backend API**: http://127.0.0.1:8000
- **Django Admin**: http://127.0.0.1:8000/admin

### Default Credentials (if using sample data)
- **Admin User**: admin / admin123
- **Test Users**: user1, user2, user3 / password123

### API Endpoints

#### Blog API
- `GET /blog/api/posts/` - List all posts
- `GET /blog/api/posts/{slug}/` - Get specific post
- `POST /blog/api/posts/` - Create new post
- `GET /blog/api/categories/` - List categories
- `GET /blog/api/tags/` - List tags
- `POST /blog/api/comments/` - Create comment

#### AI Tutorial API
- `GET /ai-tutorial/api/tutorials/` - List tutorials
- `POST /ai-tutorial/api/requests/` - Generate new tutorial
- `POST /ai-tutorial/api/requests/suggestions/` - Get AI suggestions
- `POST /ai-tutorial/api/tutorials/{id}/start/` - Start tutorial
- `POST /ai-tutorial/api/tutorials/{id}/rate/` - Rate tutorial

## 🎯 Key Features Explained

### AI Tutorial Generation
1. **Request Tutorial**: Users describe what they want to learn
2. **AI Processing**: OpenAI GPT generates structured content
3. **Tutorial Creation**: System creates tutorial with steps and code examples
4. **Progress Tracking**: Users can track their learning progress

### Blog Management
1. **Content Creation**: Rich text editor for blog posts
2. **Media Upload**: Support for featured images
3. **SEO Optimization**: Meta tags and structured data
4. **Social Features**: Comments, likes, and sharing

### User Experience
1. **Responsive Design**: Mobile-first approach
2. **Fast Loading**: Optimized images and code splitting
3. **Accessibility**: WCAG compliant interface
4. **Search**: Full-text search across content

## 🔧 Development

### Project Structure
```
LogBlog/
├── backend/                 # Django backend
│   ├── backend/            # Django project settings
│   ├── blog/               # Blog app
│   ├── ai_tutorial/        # AI tutorial app
│   ├── manage.py
│   └── requirements.txt
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/     # Reusable components
│   │   ├── pages/          # Page components
│   │   ├── services/       # API services
│   │   └── App.jsx
│   ├── package.json
│   └── vite.config.js
└── README.md
```

### Adding New Features

#### Backend (Django)
1. Create new models in `models.py`
2. Add serializers in `serializers.py`
3. Create views in `views.py`
4. Update URL patterns in `urls.py`
5. Run migrations

#### Frontend (React)
1. Create components in `src/components/`
2. Add pages in `src/pages/`
3. Update API services in `src/services/api.js`
4. Add routes in `App.jsx`

## 🔒 Security

- **CORS**: Configured for local development
- **Authentication**: Django session authentication
- **Data Validation**: Input validation on both frontend and backend
- **SQL Injection**: Protected by Django ORM
- **XSS Protection**: React's built-in protection

## 🚀 Deployment

### Backend Deployment
1. Configure production settings
2. Set up PostgreSQL database
3. Configure static file serving
4. Deploy to platform (Heroku, DigitalOcean, etc.)

### Frontend Deployment
1. Build the application: `npm run build`
2. Deploy to static hosting (Netlify, Vercel, etc.)
3. Update API base URL for production

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- OpenAI for providing the GPT API for tutorial generation
- Django community for the excellent web framework
- React team for the powerful UI library
- Tailwind CSS for the utility-first CSS framework
- All contributors and users of this project

## 📞 Support

For support, email support@logblog.com or create an issue in the GitHub repository.

---

**Happy Learning! 🚀**