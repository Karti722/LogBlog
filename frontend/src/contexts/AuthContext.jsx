import React, { createContext, useContext, useState, useEffect } from 'react';
import { authAPI } from '../services/api';
import Toast from '../components/Toast';

const AuthContext = createContext();

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [toast, setToast] = useState(null);

  useEffect(() => {
    const checkAuth = async () => {
      const token = localStorage.getItem('authToken');
      const storedUser = localStorage.getItem('currentUser');
      
      if (token && storedUser) {
        try {
          setUser(JSON.parse(storedUser));
          setIsAuthenticated(true);
        } catch (error) {
          console.error('Auth check failed:', error);
          localStorage.removeItem('authToken');
          localStorage.removeItem('currentUser');
          setIsAuthenticated(false);
        }
      }
      setLoading(false);
    };

    checkAuth();
  }, []);

  const login = async (credentials) => {
    try {
      // Clear any existing invalid tokens before login attempt
      localStorage.removeItem('authToken');
      localStorage.removeItem('currentUser');
      setIsAuthenticated(false);
      
      const response = await authAPI.login(credentials);
      if (response.data.success) {
        const { token, user } = response.data;
        localStorage.setItem('authToken', token);
        localStorage.setItem('currentUser', JSON.stringify(user));
        setUser(user);
        setIsAuthenticated(true);
        showToast('Successfully logged in!', 'success');
        return { success: true };
      } else {
        showToast(response.data.error || 'Login failed', 'error');
        return { success: false, error: response.data.error };
      }
    } catch (error) {
      console.error('Login failed:', error);
      const errorMessage = error.response?.data?.error || 'Login failed. Please try again.';
      showToast(errorMessage, 'error');
      return { success: false, error: errorMessage };
    }
  };

  const register = async (userData) => {
    try {
      const response = await authAPI.register(userData);
      if (response.data.success) {
        showToast('Registration successful! Please log in.', 'success');
        return { success: true };
      } else {
        const errors = response.data.errors;
        let errorMessage = 'Registration failed';
        
        if (errors) {
          // Handle field-specific errors
          const errorMessages = [];
          Object.keys(errors).forEach(field => {
            const fieldErrors = Array.isArray(errors[field]) ? errors[field] : [errors[field]];
            fieldErrors.forEach(error => {
              errorMessages.push(`${field}: ${error}`);
            });
          });
          errorMessage = errorMessages.join(', ');
        }
        
        showToast(errorMessage, 'error');
        return { success: false, error: errorMessage, fieldErrors: errors };
      }
    } catch (error) {
      console.error('Registration failed:', error);
      let errorMessage = 'Registration failed. Please try again.';
      let fieldErrors = null;
      
      if (error.response?.data?.errors) {
        fieldErrors = error.response.data.errors;
        const errorMessages = [];
        Object.keys(fieldErrors).forEach(field => {
          const fieldErrors = Array.isArray(fieldErrors[field]) ? fieldErrors[field] : [fieldErrors[field]];
          fieldErrors.forEach(err => {
            errorMessages.push(`${field}: ${err}`);
          });
        });
        errorMessage = errorMessages.join(', ');
      } else if (error.response?.data?.error) {
        errorMessage = error.response.data.error;
      }
      
      showToast(errorMessage, 'error');
      return { success: false, error: errorMessage, fieldErrors };
    }
  };

  const forgotPassword = async (email) => {
    try {
      const response = await authAPI.forgotPassword(email);
      if (response.data.success) {
        showToast(response.data.message, 'success');
        return { success: true, resetLink: response.data.reset_link }; // For demo
      }
      return response.data;
    } catch (error) {
      console.error('Forgot password failed:', error);
      const errorMessage = error.response?.data?.error || 'Failed to send reset email';
      showToast(errorMessage, 'error');
      return { success: false, error: errorMessage };
    }
  };

  const resetPassword = async (data) => {
    try {
      const response = await authAPI.resetPassword(data);
      if (response.data.success) {
        showToast('Password reset successful! Please log in.', 'success');
        return { success: true };
      } else {
        showToast(response.data.error, 'error');
        return { success: false, error: response.data.error };
      }
    } catch (error) {
      console.error('Password reset failed:', error);
      const errorMessage = error.response?.data?.error || 'Password reset failed';
      showToast(errorMessage, 'error');
      return { success: false, error: errorMessage };
    }
  };

  const logout = async () => {
    try {
      await authAPI.logout();
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      localStorage.removeItem('authToken');
      localStorage.removeItem('currentUser');
      setUser(null);
      setIsAuthenticated(false);
      showToast('Successfully logged out!', 'info');
    }
  };

  const showToast = (message, type = 'info', duration = 3000) => {
    setToast({ message, type, duration, id: Date.now() });
  };

  const hideToast = () => {
    setToast(null);
  };

  const value = {
    user,
    isAuthenticated,
    loading,
    login,
    register,
    logout,
    forgotPassword,
    resetPassword,
    showToast,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
      {toast && (
        <Toast
          key={toast.id}
          message={toast.message}
          type={toast.type}
          duration={toast.duration}
          onClose={hideToast}
        />
      )}
    </AuthContext.Provider>
  );
};
