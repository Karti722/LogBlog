import React from 'react';
import { Navigate, useLocation } from 'react-router-dom';

const ProtectedRoute = ({ children }) => {
  const location = useLocation();
  const authToken = localStorage.getItem('authToken');
  
  if (!authToken) {
    // Redirect to login with the current location so we can redirect back after login
    return <Navigate to="/login" state={{ from: location }} replace />;
  }
  
  return children;
};

export default ProtectedRoute;
