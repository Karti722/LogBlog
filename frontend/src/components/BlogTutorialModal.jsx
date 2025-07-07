import React, { useState } from 'react';
import { 
  SparklesIcon, 
  PencilIcon, 
  DocumentTextIcon, 
  LightBulbIcon,
  XMarkIcon,
  PlayIcon
} from '@heroicons/react/24/outline';

const BlogTutorialModal = ({ isOpen, onClose }) => {
  const [currentStep, setCurrentStep] = useState(0);

  const steps = [
    {
      title: "Welcome to AI-Powered Blog Creation!",
      content: (
        <div className="text-center">
          <SparklesIcon className="h-16 w-16 text-purple-500 mx-auto mb-4" />
          <p className="text-gray-600 mb-4">
            Our AI assistant will guide you through creating amazing blog content. 
            Let's take a quick tour of the features!
          </p>
        </div>
      )
    },
    {
      title: "Step 1: Get AI Title Suggestions",
      content: (
        <div>
          <div className="bg-blue-50 p-4 rounded-lg mb-4">
            <h4 className="font-semibold text-blue-800 mb-2">Try this example:</h4>
            <div className="text-sm text-blue-700 space-y-1">
              <p><strong>Topic:</strong> JavaScript for beginners</p>
              <p><strong>Keywords:</strong> functions, variables, loops</p>
              <p><strong>Audience:</strong> Beginner</p>
            </div>
          </div>
          <p className="text-gray-600">
            The AI will generate multiple catchy, SEO-friendly titles that you can choose from.
          </p>
        </div>
      )
    },
    {
      title: "Step 2: Generate Content Outline",
      content: (
        <div>
          <DocumentTextIcon className="h-12 w-12 text-green-500 mb-4" />
          <p className="text-gray-600 mb-4">
            Once you have a title, the AI will create a structured outline with:
          </p>
          <ul className="text-gray-600 space-y-2">
            <li>• Introduction and overview</li>
            <li>• Main sections and subsections</li>
            <li>• Key points to cover</li>
            <li>• Conclusion suggestions</li>
          </ul>
        </div>
      )
    },
    {
      title: "Step 3: Get Writing Tips",
      content: (
        <div>
          <LightBulbIcon className="h-12 w-12 text-yellow-500 mb-4" />
          <p className="text-gray-600 mb-4">
            As you write, get AI-powered feedback on:
          </p>
          <ul className="text-gray-600 space-y-2">
            <li>• Content structure and flow</li>
            <li>• Readability improvements</li>
            <li>• Engagement suggestions</li>
            <li>• SEO optimization tips</li>
          </ul>
        </div>
      )
    },
    {
      title: "Ready to Start Writing!",
      content: (
        <div className="text-center">
          <PencilIcon className="h-16 w-16 text-purple-500 mx-auto mb-4" />
          <p className="text-gray-600 mb-4">
            You're all set! Start by filling in your topic and keywords in the AI Assistant panel.
          </p>
          <div className="bg-purple-50 p-4 rounded-lg">
            <p className="text-purple-800 font-medium">
              💡 Pro Tip: The more specific your topic and keywords, the better the AI suggestions!
            </p>
          </div>
        </div>
      )
    }
  ];

  if (!isOpen) return null;

  const nextStep = () => {
    if (currentStep < steps.length - 1) {
      setCurrentStep(currentStep + 1);
    } else {
      onClose();
    }
  };

  const prevStep = () => {
    if (currentStep > 0) {
      setCurrentStep(currentStep - 1);
    }
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg max-w-md w-full mx-4 p-6">
        {/* Header */}
        <div className="flex justify-between items-center mb-4">
          <h3 className="text-lg font-semibold text-gray-900">
            Blog Creation Tutorial
          </h3>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600"
          >
            <XMarkIcon className="h-6 w-6" />
          </button>
        </div>

        {/* Progress Bar */}
        <div className="mb-6">
          <div className="flex justify-between text-xs text-gray-500 mb-2">
            <span>Step {currentStep + 1} of {steps.length}</span>
            <span>{Math.round(((currentStep + 1) / steps.length) * 100)}%</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div 
              className="bg-purple-600 h-2 rounded-full transition-all duration-300"
              style={{ width: `${((currentStep + 1) / steps.length) * 100}%` }}
            ></div>
          </div>
        </div>

        {/* Content */}
        <div className="mb-6">
          <h4 className="text-lg font-medium text-gray-900 mb-4">
            {steps[currentStep].title}
          </h4>
          <div>
            {steps[currentStep].content}
          </div>
        </div>

        {/* Navigation */}
        <div className="flex justify-between">
          <button
            onClick={prevStep}
            disabled={currentStep === 0}
            className={`px-4 py-2 rounded-md ${
              currentStep === 0
                ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
                : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
            }`}
          >
            Previous
          </button>
          <button
            onClick={nextStep}
            className="px-4 py-2 bg-purple-600 text-white rounded-md hover:bg-purple-700 flex items-center"
          >
            {currentStep === steps.length - 1 ? (
              <>
                <PlayIcon className="h-4 w-4 mr-2" />
                Start Creating
              </>
            ) : (
              'Next'
            )}
          </button>
        </div>
      </div>
    </div>
  );
};

export default BlogTutorialModal;
