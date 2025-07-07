import React, { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { blogAPI } from '../services/api';
import { 
  SparklesIcon, 
  PencilIcon, 
  DocumentTextIcon, 
  LightBulbIcon,
  PlusIcon,
  EyeIcon,
  XMarkIcon,
  QuestionMarkCircleIcon,
  ArrowLeftIcon
} from '@heroicons/react/24/outline';

const EditBlog = () => {
  const navigate = useNavigate();
  const { slug } = useParams();
  const [loading, setLoading] = useState(false);
  const [initialLoading, setInitialLoading] = useState(true);
  const [categories, setCategories] = useState([]);
  const [tags, setTags] = useState([]);
  
  const [formData, setFormData] = useState({
    title: '',
    content: '',
    excerpt: '',
    category: '',
    tags: [],
    status: 'draft',
    is_featured: false
  });

  const [errors, setErrors] = useState({});
  const [preview, setPreview] = useState(false);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setInitialLoading(true);
        const [postResponse, categoriesResponse, tagsResponse] = await Promise.all([
          blogAPI.getPost(slug),
          blogAPI.getCategories(),
          blogAPI.getTags()
        ]);
        
        const post = postResponse.data;
        setFormData({
          title: post.title,
          content: post.content,
          excerpt: post.excerpt,
          category: post.category?.id || '',
          tags: post.tags?.map(tag => tag.id) || [],
          status: post.status,
          is_featured: post.is_featured
        });
        
        setCategories(categoriesResponse.data.results || categoriesResponse.data);
        setTags(tagsResponse.data.results || tagsResponse.data);
      } catch (error) {
        console.error('Error fetching data:', error);
        alert('Failed to load blog post for editing');
        navigate('/blog');
      } finally {
        setInitialLoading(false);
      }
    };

    fetchData();
  }, [slug, navigate]);

  const handleInputChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
  };

  const handleTagToggle = (tagId) => {
    setFormData(prev => ({
      ...prev,
      tags: prev.tags.includes(tagId)
        ? prev.tags.filter(id => id !== tagId)
        : [...prev.tags, tagId]
    }));
  };

  const validateForm = () => {
    const newErrors = {};
    
    if (!formData.title.trim()) newErrors.title = 'Title is required';
    if (!formData.content.trim()) newErrors.content = 'Content is required';
    if (!formData.excerpt.trim()) newErrors.excerpt = 'Excerpt is required';
    if (!formData.category) newErrors.category = 'Category is required';
    
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!validateForm()) return;

    setLoading(true);
    try {
      const postData = {
        ...formData,
        tags: formData.tags
      };

      await blogAPI.updatePost(slug, postData);
      
      alert('Blog post updated successfully!');
      navigate(`/blog/${slug}`);
    } catch (error) {
      console.error('Error updating blog post:', error);
      if (error.response?.data) {
        setErrors(error.response.data);
      } else {
        alert('Failed to update blog post. Please try again.');
      }
    } finally {
      setLoading(false);
    }
  };

  const togglePreview = () => {
    setPreview(!preview);
  };

  if (initialLoading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-indigo-600"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="bg-white rounded-lg shadow-lg overflow-hidden">
          {/* Header */}
          <div className="bg-gradient-to-r from-green-600 to-blue-600 text-white p-6">
            <div className="flex justify-between items-center">
              <div>
                <h1 className="text-3xl font-bold flex items-center">
                  <PencilIcon className="h-8 w-8 mr-3" />
                  Edit Blog Post
                </h1>
                <p className="mt-2 text-green-100">
                  Update your blog post content and settings
                </p>
              </div>
              <button
                onClick={() => navigate(`/blog/${slug}`)}
                className="bg-white bg-opacity-20 hover:bg-opacity-30 px-4 py-2 rounded-lg flex items-center transition-colors"
              >
                <ArrowLeftIcon className="h-5 w-5 mr-2" />
                Back to Post
              </button>
            </div>
          </div>

          <div className="flex">
            {/* Main Content */}
            <div className="flex-1 p-6">
              <form onSubmit={handleSubmit} className="space-y-6">
                {/* Title */}
                <div>
                  <label htmlFor="title" className="block text-sm font-medium text-gray-700 mb-2">
                    Blog Title *
                  </label>
                  <input
                    type="text"
                    id="title"
                    name="title"
                    value={formData.title}
                    onChange={handleInputChange}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    placeholder="Enter your blog title"
                  />
                  {errors.title && <p className="mt-1 text-sm text-red-600">{errors.title}</p>}
                </div>

                {/* Category and Status */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label htmlFor="category" className="block text-sm font-medium text-gray-700 mb-2">
                      Category *
                    </label>
                    <select
                      id="category"
                      name="category"
                      value={formData.category}
                      onChange={handleInputChange}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    >
                      <option value="">Select a category</option>
                      {categories.map(category => (
                        <option key={category.id} value={category.id}>
                          {category.name}
                        </option>
                      ))}
                    </select>
                    {errors.category && <p className="mt-1 text-sm text-red-600">{errors.category}</p>}
                  </div>

                  <div>
                    <label htmlFor="status" className="block text-sm font-medium text-gray-700 mb-2">
                      Status
                    </label>
                    <select
                      id="status"
                      name="status"
                      value={formData.status}
                      onChange={handleInputChange}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    >
                      <option value="draft">Draft</option>
                      <option value="published">Published</option>
                      <option value="archived">Archived</option>
                    </select>
                  </div>
                </div>

                {/* Tags */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Tags
                  </label>
                  <div className="flex flex-wrap gap-2 max-h-32 overflow-y-auto p-2 border border-gray-300 rounded-md">
                    {tags.map(tag => (
                      <button
                        key={tag.id}
                        type="button"
                        onClick={() => handleTagToggle(tag.id)}
                        className={`px-3 py-1 rounded-full text-xs font-medium transition-colors ${
                          formData.tags.includes(tag.id)
                            ? 'bg-blue-600 text-white'
                            : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                        }`}
                      >
                        {tag.name}
                      </button>
                    ))}
                  </div>
                </div>

                {/* Excerpt */}
                <div>
                  <label htmlFor="excerpt" className="block text-sm font-medium text-gray-700 mb-2">
                    Excerpt *
                  </label>
                  <textarea
                    id="excerpt"
                    name="excerpt"
                    value={formData.excerpt}
                    onChange={handleInputChange}
                    rows={3}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    placeholder="Brief description of your blog post"
                  />
                  {errors.excerpt && <p className="mt-1 text-sm text-red-600">{errors.excerpt}</p>}
                </div>

                {/* Content */}
                <div>
                  <div className="flex justify-between items-center mb-2">
                    <label htmlFor="content" className="block text-sm font-medium text-gray-700">
                      Content *
                    </label>
                    <button
                      type="button"
                      onClick={togglePreview}
                      className="flex items-center text-sm text-blue-600 hover:text-blue-800"
                    >
                      <EyeIcon className="h-4 w-4 mr-1" />
                      {preview ? 'Edit' : 'Preview'}
                    </button>
                  </div>
                  
                  {preview ? (
                    <div className="w-full min-h-96 p-4 border border-gray-300 rounded-md bg-gray-50 prose max-w-none">
                      <div dangerouslySetInnerHTML={{ __html: formData.content.replace(/\n/g, '<br>') }} />
                    </div>
                  ) : (
                    <textarea
                      id="content"
                      name="content"
                      value={formData.content}
                      onChange={handleInputChange}
                      rows={20}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 font-mono text-sm"
                      placeholder="Write your blog content here..."
                    />
                  )}
                  {errors.content && <p className="mt-1 text-sm text-red-600">{errors.content}</p>}
                </div>

                {/* Featured */}
                <div className="flex items-center">
                  <input
                    type="checkbox"
                    id="is_featured"
                    name="is_featured"
                    checked={formData.is_featured}
                    onChange={handleInputChange}
                    className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                  />
                  <label htmlFor="is_featured" className="ml-2 block text-sm text-gray-700">
                    Mark as featured post
                  </label>
                </div>

                {/* Submit Button */}
                <div className="flex gap-4">
                  <button
                    type="submit"
                    disabled={loading}
                    className={`flex-1 bg-green-600 text-white py-3 px-6 rounded-lg font-semibold hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500 transition-colors ${
                      loading ? 'opacity-50 cursor-not-allowed' : ''
                    }`}
                  >
                    {loading ? 'Updating...' : 'Update Blog Post'}
                  </button>
                  
                  <button
                    type="button"
                    onClick={() => navigate(`/blog/${slug}`)}
                    className="px-6 py-3 border border-gray-300 text-gray-700 rounded-lg font-semibold hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-gray-500 transition-colors"
                  >
                    Cancel
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default EditBlog;
