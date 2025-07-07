import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './contexts/AuthContext';
import Navbar from './components/Navbar';
import Footer from './components/Footer';
import ProtectedRoute from './components/ProtectedRoute';
import Home from './pages/Home';
import BlogList from './pages/BlogList';
import BlogPost from './pages/BlogPost';
import CreateBlog from './pages/CreateBlog';
import EditBlog from './pages/EditBlog';
import Login from './pages/Login';
import Register from './pages/Register';
import ForgotPassword from './pages/ForgotPassword';
import ResetPassword from './pages/ResetPassword';
import TutorialList from './pages/TutorialList';
import TutorialDetail from './pages/TutorialDetail';
import AITutorialRequest from './pages/AITutorialRequest';
import About from './pages/About';

function App() {
  return (
    <AuthProvider>
      <Router>
        <div className="min-h-screen bg-gray-50">
          <Navbar />
          <main>
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/blog" element={<BlogList />} />
              <Route path="/blog/:slug" element={<BlogPost />} />
              <Route 
                path="/blog/create" 
                element={
                  <ProtectedRoute>
                    <CreateBlog />
                  </ProtectedRoute>
                } 
              />
              <Route 
                path="/blog/:slug/edit" 
                element={
                  <ProtectedRoute>
                    <EditBlog />
                  </ProtectedRoute>
                } 
              />
              <Route path="/login" element={<Login />} />
              <Route path="/register" element={<Register />} />
              <Route path="/forgot-password" element={<ForgotPassword />} />
              <Route path="/reset-password/:uid/:token" element={<ResetPassword />} />
              <Route path="/tutorials" element={<TutorialList />} />
              <Route path="/tutorials/:slug" element={<TutorialDetail />} />
              <Route path="/ai-tutorial" element={<AITutorialRequest />} />
              <Route path="/about" element={<About />} />
            </Routes>
          </main>
          <Footer />
        </div>
      </Router>
    </AuthProvider>
  );
}

export default App;
