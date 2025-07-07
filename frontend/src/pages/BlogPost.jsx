import React, { useState, useEffect } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import { blogAPI } from '../services/api';
import { 
  CalendarIcon, 
  TagIcon, 
  UserIcon, 
  EyeIcon, 
  ArrowLeftIcon,
  PencilIcon,
  TrashIcon
} from '@heroicons/react/24/outline';
import { formatDate } from '../utils/dateFormat';

const BlogPost = () => {
  const { slug } = useParams();
  const navigate = useNavigate();
  const [post, setPost] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [relatedPosts, setRelatedPosts] = useState([]);
  const [currentUser, setCurrentUser] = useState(null);
  const [showDeleteModal, setShowDeleteModal] = useState(false);

  useEffect(() => {
    const fetchPost = async () => {
      try {
        setLoading(true);
        const response = await blogAPI.getPost(slug);
        setPost(response.data);
        
        // Fetch related posts
        if (response.data.category) {
          const relatedResponse = await blogAPI.getPosts({
            category: response.data.category.id,
            exclude: response.data.id
          });
          setRelatedPosts(relatedResponse.data.results?.slice(0, 3) || []);
        }
      } catch (error) {
        console.error('Error fetching post:', error);
        setError('Failed to load blog post');
      } finally {
        setLoading(false);
      }
    };

    const fetchCurrentUser = async () => {
      try {
        const token = localStorage.getItem('authToken');
        const storedUser = localStorage.getItem('currentUser');
        
        if (token && storedUser) {
          setCurrentUser(JSON.parse(storedUser));
        } else if (token) {
          // For now, we'll simulate getting the current user
          // In a real app, you'd call an API to get current user info
          setCurrentUser({ id: 1, username: 'admin' }); // Placeholder
        }
      } catch (error) {
        console.error('Error fetching current user:', error);
      }
    };

    if (slug) {
      fetchPost();
      fetchCurrentUser();
    }
  }, [slug]);

  const handleDeletePost = async () => {
    if (window.confirm('Are you sure you want to delete this blog post? This action cannot be undone.')) {
      try {
        await blogAPI.deletePost(slug);
        alert('Blog post deleted successfully!');
        navigate('/blog');
      } catch (error) {
        console.error('Error deleting post:', error);
        alert('Failed to delete blog post. Please try again.');
      }
    }
    setShowDeleteModal(false);
  };

  const isAuthor = currentUser && post && (currentUser.id === post.author?.id || currentUser.username === 'admin');

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          <div className="animate-pulse">
            <div className="bg-gray-200 h-8 rounded w-3/4 mb-4"></div>
            <div className="bg-gray-200 h-4 rounded w-1/2 mb-8"></div>
            <div className="bg-gray-200 h-64 rounded mb-4"></div>
            <div className="space-y-2">
              <div className="bg-gray-200 h-4 rounded"></div>
              <div className="bg-gray-200 h-4 rounded"></div>
              <div className="bg-gray-200 h-4 rounded w-2/3"></div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  if (error || !post) {
    return (
      <div className="min-h-screen bg-gray-50">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          <div className="bg-white rounded-lg shadow-lg p-8 text-center">
            <h1 className="text-3xl font-bold text-gray-900 mb-4">Post Not Found</h1>
            <p className="text-gray-600 mb-6">
              {error || 'The blog post you are looking for does not exist.'}
            </p>
            <Link
              to="/blog"
              className="inline-flex items-center px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors"
            >
              <ArrowLeftIcon className="h-5 w-5 mr-2" />
              Back to Blog
            </Link>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Back to Blog Link */}
        <Link
          to="/blog"
          className="inline-flex items-center text-blue-600 hover:text-blue-800 mb-6 transition-colors"
        >
          <ArrowLeftIcon className="h-5 w-5 mr-2" />
          Back to Blog
        </Link>

        {/* Main Content */}
        <article className="bg-white rounded-lg shadow-lg overflow-hidden">
          {/* Featured Badge */}
          {post.is_featured && (
            <div className="bg-gradient-to-r from-blue-500 to-purple-600 text-white px-4 py-2">
              <span className="text-sm font-medium">Featured Post</span>
            </div>
          )}

          {/* Header */}
          <div className="p-8 pb-6">
            <div className="flex justify-between items-start mb-4">
              <div className="flex items-center space-x-4 text-sm text-gray-600">
                <div className="flex items-center">
                  <UserIcon className="h-4 w-4 mr-1" />
                  <span>{post.author?.first_name || post.author?.username}</span>
                </div>
                <div className="flex items-center">
                  <CalendarIcon className="h-4 w-4 mr-1" />
                  <span>{formatDate(post.created_at)}</span>
                </div>
                <div className="flex items-center">
                  <EyeIcon className="h-4 w-4 mr-1" />
                  <span>{post.views || 0} views</span>
                </div>
              </div>

              {/* Edit and Delete Buttons */}
              {isAuthor && (
                <div className="flex items-center space-x-2">
                  <Link
                    to={`/blog/${slug}/edit`}
                    className="inline-flex items-center px-3 py-2 bg-blue-600 text-white text-sm font-medium rounded-md hover:bg-blue-700 transition-colors"
                  >
                    <PencilIcon className="h-4 w-4 mr-1" />
                    Edit
                  </Link>
                  <button
                    onClick={() => setShowDeleteModal(true)}
                    className="inline-flex items-center px-3 py-2 bg-red-600 text-white text-sm font-medium rounded-md hover:bg-red-700 transition-colors"
                  >
                    <TrashIcon className="h-4 w-4 mr-1" />
                    Delete
                  </button>
                </div>
              )}
            </div>

            <h1 className="text-4xl font-bold text-gray-900 mb-4 leading-tight">
              {post.title}
            </h1>

            {post.excerpt && (
              <p className="text-xl text-gray-600 mb-6 leading-relaxed">
                {post.excerpt}
              </p>
            )}

            {/* Category and Tags */}
            <div className="flex flex-wrap items-center gap-4 mb-6">
              {post.category && (
                <Link
                  to={`/blog?category=${post.category.id}`}
                  className="inline-flex items-center px-3 py-1 bg-blue-100 text-blue-800 text-sm font-medium rounded-full hover:bg-blue-200 transition-colors"
                >
                  {post.category.name}
                </Link>
              )}
              
              {post.tags && post.tags.length > 0 && (
                <div className="flex items-center space-x-2">
                  <TagIcon className="h-4 w-4 text-gray-500" />
                  {post.tags.map(tag => (
                    <Link
                      key={tag.id}
                      to={`/blog?tag=${tag.id}`}
                      className="text-sm text-gray-600 hover:text-blue-600 transition-colors"
                    >
                      #{tag.name}
                    </Link>
                  ))}
                </div>
              )}
            </div>
          </div>

          {/* Content */}
          <div className="px-8 pb-8">
            <div 
              className="prose prose-lg max-w-none prose-headings:text-gray-900 prose-p:text-gray-700 prose-a:text-blue-600 prose-code:bg-gray-100 prose-code:px-2 prose-code:py-1 prose-code:rounded prose-pre:bg-gray-900 prose-pre:text-gray-100"
              dangerouslySetInnerHTML={{ __html: post.content.replace(/\n/g, '<br>') }}
            />
          </div>
        </article>

        {/* Related Posts */}
        {relatedPosts.length > 0 && (
          <div className="mt-12">
            <h2 className="text-2xl font-bold text-gray-900 mb-6">Related Posts</h2>
            <div className="grid md:grid-cols-3 gap-6">
              {relatedPosts.map(relatedPost => (
                <Link
                  key={relatedPost.id}
                  to={`/blog/${relatedPost.slug}`}
                  className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow"
                >
                  <div className="p-4">
                    <h3 className="font-semibold text-gray-900 mb-2 line-clamp-2">
                      {relatedPost.title}
                    </h3>
                    <p className="text-sm text-gray-600 mb-3 line-clamp-2">
                      {relatedPost.excerpt}
                    </p>
                    <div className="flex items-center text-xs text-gray-500">
                      <CalendarIcon className="h-3 w-3 mr-1" />
                      <span>{formatDate(relatedPost.created_at)}</span>
                    </div>
                  </div>
                </Link>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Delete Confirmation Modal */}
      {showDeleteModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg max-w-md w-full mx-4 p-6">
            <div className="flex items-center mb-4">
              <TrashIcon className="h-6 w-6 text-red-600 mr-3" />
              <h3 className="text-lg font-semibold text-gray-900">Delete Blog Post</h3>
            </div>
            <p className="text-gray-600 mb-6">
              Are you sure you want to delete "{post.title}"? This action cannot be undone.
            </p>
            <div className="flex justify-end space-x-3">
              <button
                onClick={() => setShowDeleteModal(false)}
                className="px-4 py-2 text-gray-700 bg-gray-200 rounded-md hover:bg-gray-300 transition-colors"
              >
                Cancel
              </button>
              <button
                onClick={handleDeletePost}
                className="px-4 py-2 text-white bg-red-600 rounded-md hover:bg-red-700 transition-colors"
              >
                Delete
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default BlogPost;
