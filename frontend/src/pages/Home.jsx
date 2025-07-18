import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { blogAPI, tutorialAPI } from '../services/api';
import { ArrowRightIcon, BookOpenIcon, CodeBracketIcon, SparklesIcon } from '@heroicons/react/24/outline';

const Home = () => {
  const [featuredPosts, setFeaturedPosts] = useState([]);
  const [popularTutorials, setPopularTutorials] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [postsResponse, tutorialsResponse] = await Promise.all([
          blogAPI.getFeaturedPosts(),
          tutorialAPI.getPopularTutorials()
        ]);
        
        setFeaturedPosts(postsResponse.data.slice(0, 3));
        setPopularTutorials(tutorialsResponse.data.slice(0, 3));
      } catch (error) {
        console.error('Error fetching data:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-indigo-600"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="bg-gradient-to-r from-indigo-600 to-purple-600 text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
          <div className="text-center">
            <h1 className="text-4xl md:text-6xl font-bold mb-6">
              Welcome to <span className="text-yellow-300">LogBlog</span>
            </h1>
            <p className="text-lg mb-4 text-indigo-200">
              Created by <span className="font-semibold text-yellow-300">Kartikeya Kumaria</span>
            </p>
            <p className="text-xl md:text-2xl mb-8 text-indigo-100">
              Your ultimate destination for learning web development and creating amazing blogs
            </p>
            <p className="text-lg mb-10 text-indigo-200 max-w-3xl mx-auto">
              Discover comprehensive tutorials, get AI-powered learning assistance, and master the art of building modern web applications from scratch.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link
                to="/blog/create"
                className="bg-yellow-400 text-purple-900 px-8 py-3 rounded-lg font-semibold hover:bg-yellow-300 transition-colors inline-flex items-center"
              >
                <SparklesIcon className="h-5 w-5 mr-2" />
                Create AI-Powered Blog
              </Link>
              <Link
                to="/ai-tutorial"
                className="border-2 border-white text-white px-8 py-3 rounded-lg font-semibold hover:bg-white hover:text-indigo-600 transition-colors inline-flex items-center"
              >
                <SparklesIcon className="h-5 w-5 mr-2" />
                Try AI Tutorial Generator
              </Link>
              <Link
                to="/blog"
                className="border-2 border-white text-white px-8 py-3 rounded-lg font-semibold hover:bg-white hover:text-indigo-600 transition-colors inline-flex items-center"
              >
                <BookOpenIcon className="h-5 w-5 mr-2" />
                Explore Blog Posts
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-16 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">
              Everything You Need to Build Amazing Blogs
            </h2>
            <p className="text-lg text-gray-600 max-w-2xl mx-auto">
              From beginner tutorials to advanced techniques, we've got you covered
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="text-center p-6 rounded-lg border hover:shadow-lg transition-shadow">
              <div className="bg-indigo-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                <BookOpenIcon className="h-8 w-8 text-indigo-600" />
              </div>
              <h3 className="text-xl font-semibold mb-3">Comprehensive Tutorials</h3>
              <p className="text-gray-600">
                Step-by-step guides covering everything from basic HTML to advanced React concepts
              </p>
            </div>
            
            <div className="text-center p-6 rounded-lg border hover:shadow-lg transition-shadow">
              <div className="bg-purple-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                <SparklesIcon className="h-8 w-8 text-purple-600" />
              </div>
              <h3 className="text-xl font-semibold mb-3">AI-Powered Learning</h3>
              <p className="text-gray-600">
                Get personalized tutorials generated by AI based on your specific learning needs
              </p>
            </div>
            
            <div className="text-center p-6 rounded-lg border hover:shadow-lg transition-shadow">
              <div className="bg-green-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                <CodeBracketIcon className="h-8 w-8 text-green-600" />
              </div>
              <h3 className="text-xl font-semibold mb-3">Hands-on Projects</h3>
              <p className="text-gray-600">
                Build real-world projects with practical examples and downloadable code
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Featured Posts Section */}
      <section className="py-16 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center mb-8">
            <h2 className="text-3xl font-bold text-gray-900">Featured Blog Posts</h2>
            <Link
              to="/blog"
              className="text-indigo-600 hover:text-indigo-800 font-medium inline-flex items-center"
            >
              View all posts
              <ArrowRightIcon className="h-4 w-4 ml-1" />
            </Link>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {featuredPosts.map((post) => (
              <article key={post.id} className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow">
                {post.featured_image && (
                  <img
                    src={post.featured_image}
                    alt={post.title}
                    className="w-full h-48 object-cover"
                  />
                )}
                <div className="p-6">
                  <div className="flex items-center mb-2">
                    {post.category && (
                      <span className="bg-indigo-100 text-indigo-800 text-xs font-medium px-2.5 py-0.5 rounded">
                        {post.category.name}
                      </span>
                    )}
                    <span className="text-gray-500 text-sm ml-auto">
                      {post.reading_time} min read
                    </span>
                  </div>
                  <h3 className="text-xl font-semibold text-gray-900 mb-2">
                    <Link to={`/blog/${post.slug}`} className="hover:text-indigo-600">
                      {post.title}
                    </Link>
                  </h3>
                  <p className="text-gray-600 mb-4">{post.excerpt}</p>
                  <div className="flex items-center justify-between">
                    <div className="flex items-center">
                      <span className="text-sm text-gray-500">
                        By {post.author.first_name} {post.author.last_name}
                      </span>
                    </div>
                    <Link
                      to={`/blog/${post.slug}`}
                      className="text-indigo-600 hover:text-indigo-800 font-medium"
                    >
                      Read more
                    </Link>
                  </div>
                </div>
              </article>
            ))}
          </div>
        </div>
      </section>

      {/* Popular Tutorials Section */}
      <section className="py-16 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center mb-8">
            <h2 className="text-3xl font-bold text-gray-900">Popular Tutorials</h2>
            <Link
              to="/tutorials"
              className="text-indigo-600 hover:text-indigo-800 font-medium inline-flex items-center"
            >
              View all tutorials
              <ArrowRightIcon className="h-4 w-4 ml-1" />
            </Link>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {popularTutorials.map((tutorial) => (
              <div key={tutorial.id} className="bg-white rounded-lg border hover:shadow-lg transition-shadow p-6">
                <div className="flex items-center mb-3">
                  <span className={`px-2 py-1 text-xs font-medium rounded ${
                    tutorial.difficulty === 'beginner' ? 'bg-green-100 text-green-800' :
                    tutorial.difficulty === 'intermediate' ? 'bg-yellow-100 text-yellow-800' :
                    'bg-red-100 text-red-800'
                  }`}>
                    {tutorial.difficulty}
                  </span>
                  <span className="text-gray-500 text-sm ml-auto">
                    {tutorial.estimated_duration} min
                  </span>
                </div>
                <h3 className="text-xl font-semibold text-gray-900 mb-2">
                  <Link to={`/tutorials/${tutorial.slug}`} className="hover:text-indigo-600">
                    {tutorial.title}
                  </Link>
                </h3>
                <p className="text-gray-600 mb-4">{tutorial.description}</p>
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-500">
                    {tutorial.steps_count} steps
                  </span>
                  <Link
                    to={`/tutorials/${tutorial.slug}`}
                    className="text-indigo-600 hover:text-indigo-800 font-medium"
                  >
                    Start Tutorial
                  </Link>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-16 bg-indigo-600">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-3xl font-bold text-white mb-4">
            Ready to Start Your Learning Journey?
          </h2>
          <p className="text-xl text-indigo-100 mb-8 max-w-2xl mx-auto">
            Join thousands of developers who are already building amazing projects with our tutorials
          </p>
          <Link
            to="/ai-tutorial"
            className="bg-yellow-400 text-purple-900 px-8 py-3 rounded-lg font-semibold hover:bg-yellow-300 transition-colors inline-flex items-center"
          >
            <SparklesIcon className="h-5 w-5 mr-2" />
            Generate Your First AI Tutorial
          </Link>
        </div>
      </section>
    </div>
  );
};

export default Home;
