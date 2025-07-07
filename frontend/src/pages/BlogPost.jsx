import React from 'react';

const BlogPost = () => {
  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="bg-white rounded-lg shadow-lg p-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-4">Blog Post Detail</h1>
          <p className="text-gray-600">
            This page will display individual blog posts. The functionality will be implemented 
            when you access a specific blog post from the blog list.
          </p>
        </div>
      </div>
    </div>
  );
};

export default BlogPost;
