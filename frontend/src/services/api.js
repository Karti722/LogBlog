import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'https://logblog-production.up.railway.app';

// Create axios instance with default config
const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token if available
api.interceptors.request.use(
  (config) => {
    // Don't add auth token for login/register/forgot-password requests
    const authEndpoints = ['/auth/login/', '/auth/register/', '/auth/forgot-password/', '/auth/reset-password/'];
    const isAuthEndpoint = authEndpoints.some(endpoint => config.url.includes(endpoint));
    
    if (!isAuthEndpoint) {
      const token = localStorage.getItem('authToken');
      if (token) {
        config.headers.Authorization = `Token ${token}`;
      }
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Only redirect if not already on login/register/reset pages
      const currentPath = window.location.pathname;
      const authPages = ['/login', '/register', '/forgot-password', '/reset-password'];
      const isOnAuthPage = authPages.some(page => currentPath.includes(page));
      
      if (!isOnAuthPage) {
        localStorage.removeItem('authToken');
        localStorage.removeItem('currentUser');
        window.location.href = '/login';
      }
    }
    return Promise.reject(error);
  }
);

// Blog API endpoints
export const blogAPI = {
  // Posts
  getPosts: (params = {}) => api.get('/blog/api/posts/', { params }),
  getPost: (slug) => api.get(`/blog/api/posts/${slug}/`),
  createPost: (data) => api.post('/blog/api/posts/', data),
  updatePost: (slug, data) => api.put(`/blog/api/posts/${slug}/`, data),
  deletePost: (slug) => api.delete(`/blog/api/posts/${slug}/`),
  likePost: (id) => api.post(`/blog/api/posts/${id}/like/`),
  getFeaturedPosts: () => api.get('/blog/api/posts/featured/'),
  getPopularPosts: () => api.get('/blog/api/posts/popular/'),
  getRecentPosts: () => api.get('/blog/api/posts/recent/'),

  // Categories
  getCategories: () => api.get('/blog/api/categories/'),
  getCategory: (id) => api.get(`/blog/api/categories/${id}/`),

  // Tags
  getTags: (params = {}) => api.get('/blog/api/tags/', { params }),
  getTag: (id) => api.get(`/blog/api/tags/${id}/`),

  // Comments
  getComments: (params = {}) => api.get('/blog/api/comments/', { params }),
  createComment: (data) => api.post('/blog/api/comments/', data),
  updateComment: (id, data) => api.put(`/blog/api/comments/${id}/`, data),
  deleteComment: (id) => api.delete(`/blog/api/comments/${id}/`),

  // AI Blog Assistance
  getAITitleSuggestions: (data) => api.post('/blog/api/posts/ai_title_suggestions/', data),
  getAIContentOutline: (data) => api.post('/blog/api/posts/ai_content_outline/', data),
  getAIWritingTips: (data) => api.post('/blog/api/posts/ai_writing_tips/', data),
};

// AI Tutorial API endpoints
export const tutorialAPI = {
  // Tutorials
  getTutorials: (params = {}) => api.get('/ai-tutorial/api/tutorials/', { params }),
  getTutorial: (slug) => api.get(`/ai-tutorial/api/tutorials/${slug}/`),
  startTutorial: (id) => api.post(`/ai-tutorial/api/tutorials/${id}/start/`),
  updateProgress: (id, data) => api.post(`/ai-tutorial/api/tutorials/${id}/update_progress/`, data),
  rateTutorial: (id, data) => api.post(`/ai-tutorial/api/tutorials/${id}/rate/`, data),
  getPopularTutorials: () => api.get('/ai-tutorial/api/tutorials/popular/'),
  getRecommendedTutorials: () => api.get('/ai-tutorial/api/tutorials/recommended/'),

  // Categories
  getTutorialCategories: () => api.get('/ai-tutorial/api/categories/'),

  // AI Requests
  createTutorialRequest: (data) => api.post('/ai-tutorial/api/requests/', data),
  getTutorialRequests: () => api.get('/ai-tutorial/api/requests/'),
  getTutorialSuggestions: (data) => api.post('/ai-tutorial/api/requests/suggestions/', data),
  regenerateTutorial: (id) => api.post(`/ai-tutorial/api/requests/${id}/regenerate/`),
};

// Auth API endpoints
export const authAPI = {
  login: (credentials) => api.post('/auth/login/', credentials),
  logout: () => api.post('/auth/logout/'),
  register: (userData) => api.post('/auth/register/', userData),
  forgotPassword: (email) => api.post('/auth/forgot-password/', { email }),
  resetPassword: (data) => api.post('/auth/reset-password/', data),
  getProfile: () => api.get('/auth/profile/'),
  isAuthenticated: () => {
    return !!localStorage.getItem('authToken');
  },
};

export default api;
