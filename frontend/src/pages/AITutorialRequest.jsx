import React, { useState } from 'react';
import { tutorialAPI } from '../services/api';
import { SparklesIcon, LightBulbIcon, BookOpenIcon, ClockIcon } from '@heroicons/react/24/outline';

const AITutorialRequest = () => {
  const [formData, setFormData] = useState({
    topic: '',
    description: '',
    difficulty: 'beginner'
  });
  const [loading, setLoading] = useState(false);
  const [generatedTutorial, setGeneratedTutorial] = useState(null);
  const [suggestions, setSuggestions] = useState([]);
  const [error, setError] = useState('');

  const handleInputChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const response = await tutorialAPI.createTutorialRequest(formData);
      
      if (response.data.tutorial) {
        setGeneratedTutorial(response.data.tutorial);
      } else {
        setError('Tutorial request created but generation failed. Please try again.');
      }
    } catch (err) {
      setError('Failed to generate tutorial. Please try again.');
      console.error('Error:', err);
    } finally {
      setLoading(false);
    }
  };

  const getSuggestions = async () => {
    if (!formData.topic.trim()) return;

    try {
      const response = await tutorialAPI.getTutorialSuggestions({ topic: formData.topic });
      setSuggestions(response.data.suggestions || []);
    } catch (err) {
      console.error('Error getting suggestions:', err);
    }
  };

  const selectSuggestion = (suggestion) => {
    setFormData({
      topic: suggestion.title,
      description: suggestion.description,
      difficulty: suggestion.difficulty
    });
    setSuggestions([]);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-gradient-to-r from-purple-600 to-indigo-600 text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          <div className="text-center">
            <SparklesIcon className="h-16 w-16 mx-auto mb-4 text-yellow-300" />
            <h1 className="text-4xl font-bold mb-4">AI Tutorial Generator</h1>
            <p className="text-xl text-purple-100 max-w-2xl mx-auto">
              Describe what you want to learn, and our AI will create a personalized tutorial just for you
            </p>
          </div>
        </div>
      </div>

      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {!generatedTutorial ? (
          /* Tutorial Request Form */
          <div className="bg-white rounded-lg shadow-lg p-8">
            <form onSubmit={handleSubmit} className="space-y-6">
              <div>
                <label htmlFor="topic" className="block text-sm font-medium text-gray-700 mb-2">
                  What do you want to learn?
                </label>
                <input
                  type="text"
                  id="topic"
                  name="topic"
                  value={formData.topic}
                  onChange={handleInputChange}
                  placeholder="e.g., How to build a React contact form"
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500"
                  required
                />
                <button
                  type="button"
                  onClick={getSuggestions}
                  className="mt-2 text-sm text-indigo-600 hover:text-indigo-800 flex items-center"
                >
                  <LightBulbIcon className="h-4 w-4 mr-1" />
                  Get AI suggestions
                </button>
              </div>

              {suggestions.length > 0 && (
                <div className="bg-blue-50 rounded-lg p-4">
                  <h3 className="text-sm font-medium text-gray-900 mb-2">AI Suggestions:</h3>
                  <div className="space-y-2">
                    {suggestions.map((suggestion, index) => (
                      <button
                        key={index}
                        type="button"
                        onClick={() => selectSuggestion(suggestion)}
                        className="block w-full text-left p-3 bg-white rounded border hover:border-indigo-500 hover:shadow-sm transition-all"
                      >
                        <div className="font-medium text-gray-900">{suggestion.title}</div>
                        <div className="text-sm text-gray-600 mt-1">{suggestion.description}</div>
                        <div className="flex items-center mt-2">
                          <span className={`px-2 py-1 text-xs font-medium rounded ${
                            suggestion.difficulty === 'beginner' ? 'bg-green-100 text-green-800' :
                            suggestion.difficulty === 'intermediate' ? 'bg-yellow-100 text-yellow-800' :
                            'bg-red-100 text-red-800'
                          }`}>
                            {suggestion.difficulty}
                          </span>
                          <span className="text-xs text-gray-500 ml-2">
                            {suggestion.estimated_duration} min
                          </span>
                        </div>
                      </button>
                    ))}
                  </div>
                </div>
              )}

              <div>
                <label htmlFor="description" className="block text-sm font-medium text-gray-700 mb-2">
                  Additional details (optional)
                </label>
                <textarea
                  id="description"
                  name="description"
                  value={formData.description}
                  onChange={handleInputChange}
                  rows={4}
                  placeholder="Provide any specific requirements or context..."
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500"
                />
              </div>

              <div>
                <label htmlFor="difficulty" className="block text-sm font-medium text-gray-700 mb-2">
                  Difficulty Level
                </label>
                <select
                  id="difficulty"
                  name="difficulty"
                  value={formData.difficulty}
                  onChange={handleInputChange}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500"
                >
                  <option value="beginner">Beginner</option>
                  <option value="intermediate">Intermediate</option>
                  <option value="advanced">Advanced</option>
                </select>
              </div>

              {error && (
                <div className="bg-red-50 border border-red-200 rounded-lg p-4">
                  <p className="text-red-800">{error}</p>
                </div>
              )}

              <button
                type="submit"
                disabled={loading || !formData.topic.trim()}
                className="w-full bg-indigo-600 hover:bg-indigo-700 disabled:bg-gray-400 text-white py-3 px-6 rounded-lg font-semibold flex items-center justify-center transition-colors"
              >
                {loading ? (
                  <>
                    <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
                    Generating Tutorial...
                  </>
                ) : (
                  <>
                    <SparklesIcon className="h-5 w-5 mr-2" />
                    Generate Tutorial
                  </>
                )}
              </button>
            </form>
          </div>
        ) : (
          /* Generated Tutorial Display */
          <div className="space-y-8">
            <div className="bg-white rounded-lg shadow-lg overflow-hidden">
              <div className="bg-gradient-to-r from-green-500 to-blue-500 text-white p-6">
                <div className="flex items-center">
                  <BookOpenIcon className="h-8 w-8 mr-3" />
                  <div>
                    <h2 className="text-2xl font-bold">{generatedTutorial.title}</h2>
                    <p className="text-green-100 mt-1">{generatedTutorial.description}</p>
                  </div>
                </div>
                <div className="flex items-center mt-4 space-x-6">
                  <div className="flex items-center">
                    <ClockIcon className="h-5 w-5 mr-2" />
                    <span>{generatedTutorial.estimated_duration} minutes</span>
                  </div>
                  <span className={`px-3 py-1 text-sm font-medium rounded-full ${
                    generatedTutorial.difficulty === 'beginner' ? 'bg-green-100 text-green-800' :
                    generatedTutorial.difficulty === 'intermediate' ? 'bg-yellow-100 text-yellow-800' :
                    'bg-red-100 text-red-800'
                  }`}>
                    {generatedTutorial.difficulty}
                  </span>
                  <span className="bg-white text-indigo-600 px-3 py-1 text-sm font-medium rounded-full">
                    {generatedTutorial.steps.length} steps
                  </span>
                </div>
              </div>

              <div className="p-6">
                <div className="space-y-6">
                  {generatedTutorial.steps.map((step) => (
                    <div key={step.id} className="border-l-4 border-indigo-500 pl-6">
                      <div className="flex items-center mb-2">
                        <span className="bg-indigo-100 text-indigo-800 text-sm font-medium px-3 py-1 rounded-full mr-3">
                          Step {step.step_number}
                        </span>
                        <h3 className="text-lg font-semibold text-gray-900">{step.title}</h3>
                      </div>
                      <div className="text-gray-700 mb-4 whitespace-pre-line">
                        {step.content}
                      </div>
                      {step.code_example && (
                        <div className="bg-gray-900 rounded-lg p-4 overflow-x-auto">
                          <pre className="text-green-400 text-sm">
                            <code>{step.code_example}</code>
                          </pre>
                        </div>
                      )}
                    </div>
                  ))}
                </div>

                <div className="mt-8 pt-6 border-t border-gray-200">
                  <div className="flex justify-between items-center">
                    <button
                      onClick={() => {
                        setGeneratedTutorial(null);
                        setFormData({ topic: '', description: '', difficulty: 'beginner' });
                      }}
                      className="bg-gray-100 hover:bg-gray-200 text-gray-800 py-2 px-4 rounded-lg transition-colors"
                    >
                      Generate Another Tutorial
                    </button>
                    <div className="text-sm text-gray-500">
                      Tutorial generated by AI • {new Date().toLocaleDateString()}
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default AITutorialRequest;
