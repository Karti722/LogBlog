import React, { useState, useEffect } from 'react';
import { Link, useSearchParams } from 'react-router-dom';
import { blogAPI } from '../services/api';
import { MagnifyingGlassIcon, TagIcon, CalendarIcon, EyeIcon, HeartIcon, PlusIcon } from '@heroicons/react/24/outline';
import { formatDate } from '../utils/dateFormat';

const BlogList = () => {
  const [posts, setPosts] = useState([]);
  const [categories, setCategories] = useState([]);
  const [tags, setTags] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchParams, setSearchParams] = useSearchParams();
  
  // Check authentication status
  const isAuthenticated = !!localStorage.getItem('authToken');
  
  const [filters, setFilters] = useState({
    search: searchParams.get('search') || '',
    category: searchParams.get('category') || '',
    tag: searchParams.get('tag') || '',
    ordering: searchParams.get('ordering') || '-created_at'
  });

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const params = {};
        
        if (filters.search) params.search = filters.search;
        if (filters.category) params.category = filters.category;
        if (filters.tag) params.tags = filters.tag;
        if (filters.ordering) params.ordering = filters.ordering;

        const response = await blogAPI.getPosts(params);
        setPosts(response.data.results || response.data);
      } catch (error) {
        console.error('Error fetching posts:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
    fetchFilters();
  }, [filters]);

  const fetchFilters = async () => {
    try {
      const [categoriesResponse, tagsResponse] = await Promise.all([
        blogAPI.getCategories(),
        blogAPI.getTags()
      ]);
      
      setCategories(categoriesResponse.data.results || categoriesResponse.data);
      setTags(tagsResponse.data.results || tagsResponse.data);
    } catch (error) {
      console.error('Error fetching filters:', error);
    }
  };

  const handleFilterChange = (key, value) => {
    const newFilters = { ...filters, [key]: value };
    setFilters(newFilters);
    
    const newSearchParams = new URLSearchParams();
    Object.entries(newFilters).forEach(([k, v]) => {
      if (v) newSearchParams.set(k, v);
    });
    
    setSearchParams(newSearchParams);
  };

  const clearFilters = () => {
    setFilters({
      search: '',
      category: '',
      tag: '',
      ordering: '-created_at'
    });
    setSearchParams({});
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-indigo-600"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="flex justify-between items-center">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">Blog Posts</h1>
              <p className="mt-2 text-gray-600">
                Discover insights, tutorials, and stories from our community
              </p>
              <p className="mt-1 text-sm text-gray-500">
                Platform by <span className="font-medium text-indigo-600">Kartikeya Kumaria</span>
              </p>
            </div>
            {isAuthenticated && (
              <Link
                to="/blog/create"
                className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
              >
                <PlusIcon className="h-5 w-5 mr-2" />
                Create Post
              </Link>
            )}
          </div>
        </div>
      </div>

      {/* Login Prompt for Unauthenticated Users */}
      {!isAuthenticated && (
        <div className="bg-indigo-50 border-l-4 border-indigo-400 p-4 mx-4 mt-4 sm:mx-6 lg:mx-8">
          <div className="flex">
            <div className="flex-shrink-0">
              <PlusIcon className="h-5 w-5 text-indigo-400" />
            </div>
            <div className="ml-3">
              <p className="text-sm text-indigo-700">
                Want to share your knowledge?{' '}
                <Link to="/login" className="font-medium underline hover:text-indigo-600">
                  Sign in
                </Link>{' '}
                or{' '}
                <Link to="/register" className="font-medium underline hover:text-indigo-600">
                  create an account
                </Link>{' '}
                to start writing and managing your own blog posts!
              </p>
            </div>
          </div>
        </div>
      )}

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="lg:grid lg:grid-cols-4 lg:gap-8">
          {/* Sidebar - Filters */}
          <div className="lg:col-span-1">
            <div className="bg-white rounded-lg shadow p-6 mb-8 lg:mb-0">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Filters</h3>
              
              {/* Search */}
              <div className="mb-6">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Search
                </label>
                <div className="relative">
                  <MagnifyingGlassIcon className="h-5 w-5 absolute left-3 top-3 text-gray-400" />
                  <input
                    type="text"
                    placeholder="Search posts..."
                    value={filters.search}
                    onChange={(e) => handleFilterChange('search', e.target.value)}
                    className="w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
                  />
                </div>
              </div>

              {/* Category Filter */}
              <div className="mb-6">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Category
                </label>
                <select
                  value={filters.category}
                  onChange={(e) => handleFilterChange('category', e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
                >
                  <option value="">All Categories</option>
                  {categories.map((category) => (
                    <option key={category.id} value={category.id}>
                      {category.name} ({category.posts_count})
                    </option>
                  ))}
                </select>
              </div>

              {/* Tag Filter */}
              <div className="mb-6">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Tag
                </label>
                <select
                  value={filters.tag}
                  onChange={(e) => handleFilterChange('tag', e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
                >
                  <option value="">All Tags</option>
                  {tags.map((tag) => (
                    <option key={tag.id} value={tag.id}>
                      {tag.name} ({tag.posts_count})
                    </option>
                  ))}
                </select>
              </div>

              {/* Sort */}
              <div className="mb-6">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Sort By
                </label>
                <select
                  value={filters.ordering}
                  onChange={(e) => handleFilterChange('ordering', e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
                >
                  <option value="-created_at">Newest First</option>
                  <option value="created_at">Oldest First</option>
                  <option value="-views_count">Most Viewed</option>
                  <option value="-likes_count">Most Liked</option>
                  <option value="title">Alphabetical</option>
                </select>
              </div>

              <button
                onClick={clearFilters}
                className="w-full bg-gray-100 hover:bg-gray-200 text-gray-800 py-2 px-4 rounded-md transition-colors"
              >
                Clear Filters
              </button>
            </div>
          </div>

          {/* Main Content */}
          <div className="lg:col-span-3">
            {posts.length === 0 ? (
              <div className="text-center py-12">
                <p className="text-gray-500 text-lg">No posts found.</p>
              </div>
            ) : (
              <div className="space-y-8">
                {posts.map((post) => (
                  <article key={post.id} className="bg-white rounded-lg shadow hover:shadow-lg transition-shadow overflow-hidden">
                    <div className="p-6">
                      <div className="flex items-center mb-3">
                        {post.category && (
                          <span className="bg-indigo-100 text-indigo-800 text-xs font-medium px-2.5 py-0.5 rounded mr-2">
                            {post.category.name}
                          </span>
                        )}
                        {post.is_featured && (
                          <span className="bg-yellow-100 text-yellow-800 text-xs font-medium px-2.5 py-0.5 rounded mr-2">
                            Featured
                          </span>
                        )}
                        <span className="text-gray-500 text-sm flex items-center ml-auto">
                          <CalendarIcon className="h-4 w-4 mr-1" />
                          {formatDate(post.created_at)}
                        </span>
                      </div>
                      
                      <h2 className="text-2xl font-bold text-gray-900 mb-2">
                        <Link to={`/blog/${post.slug}`} className="hover:text-indigo-600">
                          {post.title}
                        </Link>
                      </h2>
                      
                      <p className="text-gray-600 mb-4">{post.excerpt}</p>
                      
                      {/* Tags */}
                      {post.tags && post.tags.length > 0 && (
                        <div className="flex flex-wrap gap-2 mb-4">
                          {post.tags.map((tag) => (
                            <span
                              key={tag.id}
                              className="inline-flex items-center text-xs bg-gray-100 text-gray-700 px-2 py-1 rounded"
                            >
                              <TagIcon className="h-3 w-3 mr-1" />
                              {tag.name}
                            </span>
                          ))}
                        </div>
                      )}
                      
                      <div className="flex items-center justify-between">
                        <div className="flex items-center space-x-4">
                          <span className="text-sm text-gray-500">
                            By {post.author.first_name} {post.author.last_name}
                          </span>
                          <span className="text-sm text-gray-500">
                            {post.reading_time} min read
                          </span>
                        </div>
                        
                        <div className="flex items-center space-x-4">
                          <span className="flex items-center text-sm text-gray-500">
                            <EyeIcon className="h-4 w-4 mr-1" />
                            {post.views_count}
                          </span>
                          <span className="flex items-center text-sm text-gray-500">
                            <HeartIcon className="h-4 w-4 mr-1" />
                            {post.likes_count}
                          </span>
                          <Link
                            to={`/blog/${post.slug}`}
                            className="text-indigo-600 hover:text-indigo-800 font-medium"
                          >
                            Read more →
                          </Link>
                        </div>
                      </div>
                    </div>
                  </article>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default BlogList;
