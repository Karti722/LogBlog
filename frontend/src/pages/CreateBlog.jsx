import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { blogAPI } from '../services/api';
import BlogTutorialModal from '../components/BlogTutorialModal';
import { 
  SparklesIcon, 
  PencilIcon, 
  DocumentTextIcon, 
  LightBulbIcon,
  PlusIcon,
  EyeIcon,
  XMarkIcon,
  QuestionMarkCircleIcon
} from '@heroicons/react/24/outline';

const CreateBlog = () => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [categories, setCategories] = useState([]);
  const [tags, setTags] = useState([]);
  const [aiAssistance, setAIAssistance] = useState({
    showTitleSuggestions: false,
    showOutline: false,
    showWritingTips: false,
    titleSuggestions: [],
    outline: '',
    writingTips: ''
  });

  const [formData, setFormData] = useState({
    title: '',
    content: '',
    excerpt: '',
    category: '',
    tags: [],
    status: 'draft',
    is_featured: false
  });

  const [aiHelpers, setAIHelpers] = useState({
    topic: '',
    keywords: '',
    target_audience: 'general',
    content_type: 'tutorial'
  });

  const [errors, setErrors] = useState({});
  const [preview, setPreview] = useState(false);
  const [showTutorial, setShowTutorial] = useState(false);

  useEffect(() => {
    fetchCategories();
    fetchTags();
  }, []);

  const fetchCategories = async () => {
    try {
      const response = await blogAPI.getCategories();
      setCategories(response.data.results || response.data);
    } catch (error) {
      console.error('Error fetching categories:', error);
    }
  };

  const fetchTags = async () => {
    try {
      const response = await blogAPI.getTags();
      setTags(response.data.results || response.data);
    } catch (error) {
      console.error('Error fetching tags:', error);
    }
  };

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

  const handleAITitleSuggestions = async () => {
    if (!aiHelpers.topic) {
      alert('Please enter a topic first');
      return;
    }

    setLoading(true);
    try {
      const keywords = aiHelpers.keywords.split(',').map(k => k.trim()).filter(k => k);
      const response = await blogAPI.getAITitleSuggestions({
        topic: aiHelpers.topic,
        keywords: keywords
      });
      
      setAIAssistance(prev => ({
        ...prev,
        titleSuggestions: response.data.suggestions,
        showTitleSuggestions: true
      }));
    } catch (error) {
      console.error('Error getting title suggestions:', error);
      alert('Failed to get AI suggestions. Please check your OpenAI API key.');
    } finally {
      setLoading(false);
    }
  };

  const handleAIContentOutline = async () => {
    if (!formData.title) {
      alert('Please enter a title first');
      return;
    }

    setLoading(true);
    try {
      const response = await blogAPI.getAIContentOutline({
        title: formData.title,
        target_audience: aiHelpers.target_audience,
        content_type: aiHelpers.content_type
      });
      
      setAIAssistance(prev => ({
        ...prev,
        outline: response.data.outline,
        showOutline: true
      }));
    } catch (error) {
      console.error('Error getting content outline:', error);
      alert('Failed to get content outline. Please check your OpenAI API key.');
    } finally {
      setLoading(false);
    }
  };

  const handleAIWritingTips = async () => {
    if (!formData.content || formData.content.length < 100) {
      alert('Please write at least 100 characters of content first');
      return;
    }

    setLoading(true);
    try {
      const response = await blogAPI.getAIWritingTips({
        title: formData.title,
        content: formData.content,
        focus: 'general'
      });
      
      setAIAssistance(prev => ({
        ...prev,
        writingTips: response.data.tips,
        showWritingTips: true
      }));
    } catch (error) {
      console.error('Error getting writing tips:', error);
      alert('Failed to get writing tips. Please check your OpenAI API key.');
    } finally {
      setLoading(false);
    }
  };

  const selectTitle = (title) => {
    setFormData(prev => ({ ...prev, title }));
    setAIAssistance(prev => ({ ...prev, showTitleSuggestions: false }));
  };

  const insertOutline = () => {
    setFormData(prev => ({ 
      ...prev, 
      content: prev.content + '\n\n' + aiAssistance.outline 
    }));
    setAIAssistance(prev => ({ ...prev, showOutline: false }));
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

      const response = await blogAPI.createPost(postData);
      
      alert('Blog post created successfully!');
      navigate(`/blog/${response.data.slug}`);
    } catch (error) {
      console.error('Error creating blog post:', error);
      if (error.response?.data) {
        setErrors(error.response.data);
      } else {
        alert('Failed to create blog post. Please try again.');
      }
    } finally {
      setLoading(false);
    }
  };

  const togglePreview = () => {
    setPreview(!preview);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="bg-white rounded-lg shadow-lg overflow-hidden">
          {/* Header */}
          <div className="bg-gradient-to-r from-blue-600 to-purple-600 text-white p-6">
            <div className="flex justify-between items-center">
              <div>
                <h1 className="text-3xl font-bold flex items-center">
                  <PencilIcon className="h-8 w-8 mr-3" />
                  Create New Blog Post
                </h1>
                <p className="mt-2 text-blue-100">
                  Use our AI-powered assistant to help you write engaging blog content
                </p>
              </div>
              <button
                onClick={() => setShowTutorial(true)}
                className="bg-white bg-opacity-20 hover:bg-opacity-30 px-4 py-2 rounded-lg flex items-center transition-colors"
              >
                <QuestionMarkCircleIcon className="h-5 w-5 mr-2" />
                How it Works
              </button>
            </div>
          </div>

          <div className="flex">
            {/* Main Content */}
            <div className="flex-1 p-6">
              <form onSubmit={handleSubmit} className="space-y-6">
                {/* AI Topic Helper */}
                <div className="bg-purple-50 border border-purple-200 rounded-lg p-4">
                  <h3 className="text-lg font-semibold text-purple-800 mb-3 flex items-center">
                    <SparklesIcon className="h-5 w-5 mr-2" />
                    AI Blog Assistant
                  </h3>
                  <div className="grid md:grid-cols-2 gap-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        Topic/Subject
                      </label>
                      <input
                        type="text"
                        value={aiHelpers.topic}
                        onChange={(e) => setAIHelpers(prev => ({ ...prev, topic: e.target.value }))}
                        placeholder="e.g., React Hooks, Django REST API"
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        Keywords (comma-separated)
                      </label>
                      <input
                        type="text"
                        value={aiHelpers.keywords}
                        onChange={(e) => setAIHelpers(prev => ({ ...prev, keywords: e.target.value }))}
                        placeholder="e.g., tutorial, beginner, guide"
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        Target Audience
                      </label>
                      <select
                        value={aiHelpers.target_audience}
                        onChange={(e) => setAIHelpers(prev => ({ ...prev, target_audience: e.target.value }))}
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                      >
                        <option value="beginner">Beginner</option>
                        <option value="intermediate">Intermediate</option>
                        <option value="advanced">Advanced</option>
                        <option value="general">General</option>
                      </select>
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        Content Type
                      </label>
                      <select
                        value={aiHelpers.content_type}
                        onChange={(e) => setAIHelpers(prev => ({ ...prev, content_type: e.target.value }))}
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                      >
                        <option value="tutorial">Tutorial</option>
                        <option value="guide">Guide</option>
                        <option value="review">Review</option>
                        <option value="opinion">Opinion</option>
                        <option value="news">News</option>
                        <option value="listicle">Listicle</option>
                      </select>
                    </div>
                  </div>
                  
                  <div className="flex flex-wrap gap-3 mt-4">
                    <button
                      type="button"
                      onClick={handleAITitleSuggestions}
                      disabled={loading}
                      className="inline-flex items-center px-4 py-2 bg-purple-600 text-white rounded-md hover:bg-purple-700 disabled:opacity-50"
                    >
                      <SparklesIcon className="h-4 w-4 mr-2" />
                      Get Title Ideas
                    </button>
                    <button
                      type="button"
                      onClick={handleAIContentOutline}
                      disabled={loading}
                      className="inline-flex items-center px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50"
                    >
                      <DocumentTextIcon className="h-4 w-4 mr-2" />
                      Generate Outline
                    </button>
                    <button
                      type="button"
                      onClick={handleAIWritingTips}
                      disabled={loading}
                      className="inline-flex items-center px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 disabled:opacity-50"
                    >
                      <LightBulbIcon className="h-4 w-4 mr-2" />
                      Get Writing Tips
                    </button>
                  </div>
                </div>

                {/* Title */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Title *
                  </label>
                  <input
                    type="text"
                    name="title"
                    value={formData.title}
                    onChange={handleInputChange}
                    className={`w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 ${
                      errors.title ? 'border-red-500' : 'border-gray-300'
                    }`}
                    placeholder="Enter your blog post title"
                  />
                  {errors.title && <p className="text-red-500 text-sm mt-1">{errors.title}</p>}
                </div>

                {/* Content */}
                <div>
                  <div className="flex justify-between items-center mb-1">
                    <label className="block text-sm font-medium text-gray-700">
                      Content *
                    </label>
                    <button
                      type="button"
                      onClick={togglePreview}
                      className="inline-flex items-center text-sm text-blue-600 hover:text-blue-800"
                    >
                      <EyeIcon className="h-4 w-4 mr-1" />
                      {preview ? 'Edit' : 'Preview'}
                    </button>
                  </div>
                  
                  {preview ? (
                    <div className="w-full min-h-96 px-3 py-2 border border-gray-300 rounded-md bg-gray-50 prose max-w-none">
                      {formData.content ? (
                        <div dangerouslySetInnerHTML={{ __html: formData.content.replace(/\n/g, '<br>') }} />
                      ) : (
                        <p className="text-gray-500">No content to preview</p>
                      )}
                    </div>
                  ) : (
                    <textarea
                      name="content"
                      value={formData.content}
                      onChange={handleInputChange}
                      rows={15}
                      className={`w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 ${
                        errors.content ? 'border-red-500' : 'border-gray-300'
                      }`}
                      placeholder="Write your blog post content here... You can use Markdown formatting."
                    />
                  )}
                  {errors.content && <p className="text-red-500 text-sm mt-1">{errors.content}</p>}
                </div>

                {/* Excerpt */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Excerpt *
                  </label>
                  <textarea
                    name="excerpt"
                    value={formData.excerpt}
                    onChange={handleInputChange}
                    rows={3}
                    className={`w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 ${
                      errors.excerpt ? 'border-red-500' : 'border-gray-300'
                    }`}
                    placeholder="Write a brief excerpt that will appear in blog listings..."
                  />
                  {errors.excerpt && <p className="text-red-500 text-sm mt-1">{errors.excerpt}</p>}
                </div>

                {/* Category and Tags */}
                <div className="grid md:grid-cols-2 gap-6">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Category *
                    </label>
                    <select
                      name="category"
                      value={formData.category}
                      onChange={handleInputChange}
                      className={`w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 ${
                        errors.category ? 'border-red-500' : 'border-gray-300'
                      }`}
                    >
                      <option value="">Select a category</option>
                      {categories.map(category => (
                        <option key={category.id} value={category.id}>
                          {category.name}
                        </option>
                      ))}
                    </select>
                    {errors.category && <p className="text-red-500 text-sm mt-1">{errors.category}</p>}
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Tags
                    </label>
                    <div className="border border-gray-300 rounded-md p-3 max-h-32 overflow-y-auto">
                      <div className="flex flex-wrap gap-2">
                        {tags.map(tag => (
                          <label key={tag.id} className="inline-flex items-center">
                            <input
                              type="checkbox"
                              checked={formData.tags.includes(tag.id)}
                              onChange={() => handleTagToggle(tag.id)}
                              className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                            />
                            <span className="ml-2 text-sm text-gray-700">{tag.name}</span>
                          </label>
                        ))}
                      </div>
                    </div>
                  </div>
                </div>

                {/* Status and Featured */}
                <div className="flex flex-wrap gap-6">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Status
                    </label>
                    <select
                      name="status"
                      value={formData.status}
                      onChange={handleInputChange}
                      className="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    >
                      <option value="draft">Draft</option>
                      <option value="published">Published</option>
                    </select>
                  </div>

                  <div className="flex items-center">
                    <label className="inline-flex items-center">
                      <input
                        type="checkbox"
                        name="is_featured"
                        checked={formData.is_featured}
                        onChange={handleInputChange}
                        className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                      />
                      <span className="ml-2 text-sm font-medium text-gray-700">Featured Post</span>
                    </label>
                  </div>
                </div>

                {/* Submit Buttons */}
                <div className="flex gap-4 pt-6">
                  <button
                    type="submit"
                    disabled={loading}
                    className="flex-1 bg-blue-600 text-white py-3 px-4 rounded-md hover:bg-blue-700 disabled:opacity-50 font-medium"
                  >
                    {loading ? 'Creating...' : 'Create Blog Post'}
                  </button>
                  <button
                    type="button"
                    onClick={() => navigate('/blog')}
                    className="px-6 py-3 border border-gray-300 text-gray-700 rounded-md hover:bg-gray-50"
                  >
                    Cancel
                  </button>
                </div>
              </form>
            </div>

            {/* AI Assistance Sidebar */}
            <div className="w-96 bg-gray-50 border-l border-gray-200 p-6">
              <h3 className="text-lg font-semibold text-gray-800 mb-4 flex items-center">
                <SparklesIcon className="h-5 w-5 mr-2 text-purple-600" />
                AI Assistance
              </h3>

              {/* Title Suggestions */}
              {aiAssistance.showTitleSuggestions && (
                <div className="mb-6 bg-white rounded-lg p-4 border border-purple-200">
                  <div className="flex justify-between items-center mb-3">
                    <h4 className="font-medium text-purple-800">Title Suggestions</h4>
                    <button
                      onClick={() => setAIAssistance(prev => ({ ...prev, showTitleSuggestions: false }))}
                      className="text-gray-400 hover:text-gray-600"
                    >
                      <XMarkIcon className="h-4 w-4" />
                    </button>
                  </div>
                  <div className="space-y-2">
                    {aiAssistance.titleSuggestions.map((title, index) => (
                      <button
                        key={index}
                        onClick={() => selectTitle(title)}
                        className="w-full text-left p-2 text-sm bg-purple-50 hover:bg-purple-100 rounded border border-purple-200 transition-colors"
                      >
                        {title}
                      </button>
                    ))}
                  </div>
                </div>
              )}

              {/* Content Outline */}
              {aiAssistance.showOutline && (
                <div className="mb-6 bg-white rounded-lg p-4 border border-blue-200">
                  <div className="flex justify-between items-center mb-3">
                    <h4 className="font-medium text-blue-800">Content Outline</h4>
                    <div className="flex gap-2">
                      <button
                        onClick={insertOutline}
                        className="text-xs bg-blue-600 text-white px-2 py-1 rounded hover:bg-blue-700"
                      >
                        Insert
                      </button>
                      <button
                        onClick={() => setAIAssistance(prev => ({ ...prev, showOutline: false }))}
                        className="text-gray-400 hover:text-gray-600"
                      >
                        <XMarkIcon className="h-4 w-4" />
                      </button>
                    </div>
                  </div>
                  <div className="text-sm text-gray-700 whitespace-pre-wrap max-h-64 overflow-y-auto">
                    {aiAssistance.outline}
                  </div>
                </div>
              )}

              {/* Writing Tips */}
              {aiAssistance.showWritingTips && (
                <div className="mb-6 bg-white rounded-lg p-4 border border-green-200">
                  <div className="flex justify-between items-center mb-3">
                    <h4 className="font-medium text-green-800">Writing Tips</h4>
                    <button
                      onClick={() => setAIAssistance(prev => ({ ...prev, showWritingTips: false }))}
                      className="text-gray-400 hover:text-gray-600"
                    >
                      <XMarkIcon className="h-4 w-4" />
                    </button>
                  </div>
                  <div className="text-sm text-gray-700 whitespace-pre-wrap max-h-64 overflow-y-auto">
                    {aiAssistance.writingTips}
                  </div>
                </div>
              )}

              {/* Help Tips */}
              <div className="bg-blue-50 rounded-lg p-4 border border-blue-200">
                <h4 className="font-medium text-blue-800 mb-2">💡 Tips for Great Blog Posts</h4>
                <ul className="text-sm text-blue-700 space-y-1">
                  <li>• Start with an engaging introduction</li>
                  <li>• Use clear headings and subheadings</li>
                  <li>• Include examples and code snippets</li>
                  <li>• Write for your target audience</li>
                  <li>• End with a strong conclusion</li>
                  <li>• Proofread before publishing</li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      {/* Tutorial Modal */}
      <BlogTutorialModal 
        isOpen={showTutorial} 
        onClose={() => setShowTutorial(false)} 
      />
    </div>
  );
};

export default CreateBlog;
