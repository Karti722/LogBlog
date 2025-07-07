# ML-Based AI Tutorial Generator Setup Guide

This guide will help you set up the ML-based AI tutorial generator using PyTorch, scikit-learn, and other machine learning libraries.

## What is this ML System?

Our custom ML system uses:
- **PyTorch** for neural network-based text generation
- **Scikit-learn** for feature extraction and similarity matching
- **Sentence Transformers** for semantic understanding
- **NLTK** for natural language processing
- **Template-based generation** for structured tutorial creation

## Features

✅ **Completely Free** - No API costs or subscriptions
✅ **Offline Capable** - Works without internet connection
✅ **Customizable** - Train with your own data
✅ **Fast** - Local inference with pre-trained models
✅ **Privacy** - All data stays on your machine
✅ **Scalable** - Can be extended with more sophisticated models

## Quick Setup

### Option 1: Automated Setup (Recommended)
```powershell
.\setup_ml_ai.ps1
```

### Option 2: Manual Setup

1. **Install Dependencies**
   ```powershell
   # Activate virtual environment
   .\logenv\Scripts\Activate.ps1
   
   # Install PyTorch (CPU version)
   pip install torch==2.1.0 torchvision==0.16.0 --index-url https://download.pytorch.org/whl/cpu
   
   # Install other ML dependencies
   pip install scikit-learn==1.3.2 numpy==1.24.3 pandas==2.0.3 nltk==3.8.1 transformers==4.35.2 sentence-transformers==2.2.2 joblib==1.3.2
   ```

2. **Download NLTK Data**
   ```powershell
   python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
   ```

3. **Train Models**
   ```powershell
   cd backend
   python manage.py train_ml_models
   ```

## ML Model Architecture

### 1. Tutorial Encoder
- **Input**: Tutorial request (topic, description, difficulty)
- **Architecture**: Multi-layer neural network with attention
- **Output**: Encoded representation vector

### 2. Tutorial Decoder
- **Input**: Encoded representation
- **Architecture**: LSTM-based sequence generator
- **Output**: Structured tutorial content

### 3. Similarity Matching
- **Engine**: Sentence Transformers + Cosine Similarity
- **Purpose**: Find best matching tutorial templates
- **Features**: Semantic understanding of tutorial topics

### 4. Template System
- **Pre-trained templates** for common programming topics
- **Dynamic customization** based on user input
- **Difficulty-based adaptation**

## Training Data

The system comes with sample training data covering:
- **Django REST APIs** - Backend development
- **React Components** - Frontend development
- **Python Data Analysis** - Data science
- **Machine Learning** - AI/ML tutorials

You can extend this by:
1. Adding more templates to `ml_models.py`
2. Training with your own tutorial data
3. Fine-tuning the neural networks

## Configuration

Environment variables:
- `USE_ML_GENERATOR=True` - Enable ML generation
- `ML_MODEL_PATH=backend/ai_tutorial/models/` - Model storage path
- `ML_DEVICE=auto` - Device selection (auto/cpu/cuda)

## Usage

Once set up, the system automatically:
1. **Encodes** user requests using sentence transformers
2. **Matches** against trained templates using similarity
3. **Generates** customized tutorials using neural networks
4. **Formats** output as structured tutorial data

## Performance & Requirements

### System Requirements
- **RAM**: 4GB+ (8GB recommended)
- **Storage**: 2GB for models and dependencies
- **CPU**: Any modern processor (GPU optional)

### Performance
- **Training**: 1-5 minutes (first time only)
- **Inference**: <1 second per tutorial
- **Accuracy**: High quality for supported domains

## Extending the System

### Adding New Tutorial Templates
```python
# In ml_models.py, add to sample_tutorials
{
    'topic': 'Your New Topic',
    'description': 'Description of the topic',
    'difficulty': 'beginner',
    'tutorial': {
        'title': 'Tutorial Title',
        'description': 'Tutorial description',
        'duration': 60,
        'prerequisites': ['Prerequisite 1'],
        'steps': [
            {
                'title': 'Step 1',
                'content': 'Step content',
                'code': 'Code example'
            }
        ]
    }
}
```

### Training with Custom Data
```python
# Create your own training data
custom_data = [
    # Your tutorial data here
]

# Train with custom data
ml_generator = MLTutorialGenerator()
ml_generator._train_with_custom_data(custom_data)
```

## Troubleshooting

### Common Issues

1. **PyTorch Installation Issues**
   - Use CPU version for compatibility
   - Install from official PyTorch index

2. **Memory Issues**
   - Reduce batch size in training
   - Use CPU instead of GPU for inference

3. **Model Loading Errors**
   - Delete models folder and retrain
   - Check file permissions

4. **Slow Performance**
   - Ensure virtual environment is activated
   - Use SSD storage for models

### Performance Optimization

1. **GPU Acceleration** (if available)
   ```powershell
   # Install CUDA version
   pip install torch==2.1.0 torchvision==0.16.0 --index-url https://download.pytorch.org/whl/cu118
   ```

2. **Model Optimization**
   - Use model quantization for smaller size
   - Implement caching for repeated requests

## Comparison with Other Solutions

| Feature | Our ML System | OpenAI API | Ollama |
|---------|---------------|------------|--------|
| **Cost** | Free | Pay per use | Free |
| **Privacy** | Complete | Limited | Complete |
| **Customization** | High | Medium | Medium |
| **Setup** | Moderate | Easy | Easy |
| **Performance** | Fast | Variable | Fast |
| **Offline** | Yes | No | Yes |

## Future Enhancements

- **Fine-tuning** with domain-specific data
- **Multi-language** support
- **Code generation** improvements
- **Interactive tutorials**
- **Feedback learning**

## Support

If you encounter issues:
1. Check the logs in Django admin
2. Verify all dependencies are installed
3. Ensure models are properly trained
4. Try retraining with `python manage.py train_ml_models --force`

The system automatically falls back to mock data if ML models are unavailable, ensuring your application always works.
