import axios from 'axios';

const API_BASE_URL = 'http://127.0.0.1:8000';

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
    const token = localStorage.getItem('authToken');
    if (token) {
      config.headers.Authorization = `Token ${token}`;
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
      // Handle unauthorized access
      localStorage.removeItem('authToken');
      window.location.href = '/login';
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
  updatePost: (id, data) => api.put(`/blog/api/posts/${id}/`, data),
  deletePost: (id) => api.delete(`/blog/api/posts/${id}/`),
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
  login: (credentials) => api.post('/api-auth/login/', credentials),
  logout: () => api.post('/api-auth/logout/'),
  register: (userData) => api.post('/api-auth/register/', userData),
  getProfile: () => api.get('/api-auth/user/'),
};

export default api;
