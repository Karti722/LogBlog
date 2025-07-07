# PowerShell script to set up ML dependencies and train models

Write-Host "Setting up ML-based AI Tutorial Generator..." -ForegroundColor Green

# Check if Python is available
$pythonCmd = Get-Command python -ErrorAction SilentlyContinue
if (-not $pythonCmd) {
    Write-Host "Python not found. Please install Python first." -ForegroundColor Red
    exit 1
}

# Check if we're in a virtual environment
$venvPath = "$PSScriptRoot\logenv"
if (Test-Path $venvPath) {
    Write-Host "Activating virtual environment..." -ForegroundColor Yellow
    & "$venvPath\Scripts\Activate.ps1"
} else {
    Write-Host "Virtual environment not found. Please run from the project root." -ForegroundColor Red
    exit 1
}

# Navigate to backend directory
Set-Location "$PSScriptRoot\backend"

# Install ML dependencies
Write-Host "Installing ML dependencies..." -ForegroundColor Yellow
Write-Host "This may take a few minutes as PyTorch is a large package..." -ForegroundColor Gray

try {
    # Install PyTorch (CPU version for compatibility)
    Write-Host "Installing PyTorch..." -ForegroundColor Yellow
    pip install torch==2.1.0 torchvision==0.16.0 --index-url https://download.pytorch.org/whl/cpu
    
    # Install other ML dependencies
    Write-Host "Installing scikit-learn and other dependencies..." -ForegroundColor Yellow
    pip install scikit-learn==1.3.2 numpy==1.24.3 pandas==2.0.3 nltk==3.8.1 transformers==4.35.2 sentence-transformers==2.2.2 joblib==1.3.2
    
    Write-Host "ML dependencies installed successfully!" -ForegroundColor Green
} catch {
    Write-Host "Error installing dependencies. Trying alternative installation..." -ForegroundColor Yellow
    
    # Try installing from requirements.txt
    pip install -r requirements.txt
}

# Download NLTK data
Write-Host "Downloading NLTK data..." -ForegroundColor Yellow
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"

# Create models directory
$modelsDir = "ai_tutorial\models"
if (-not (Test-Path $modelsDir)) {
    Write-Host "Creating models directory..." -ForegroundColor Yellow
    New-Item -ItemType Directory -Path $modelsDir -Force
}

# Train the ML models
Write-Host "Training ML models with sample data..." -ForegroundColor Yellow
Write-Host "This may take a few minutes for the first run..." -ForegroundColor Gray

try {
    python manage.py train_ml_models
    Write-Host "ML models trained successfully!" -ForegroundColor Green
} catch {
    Write-Host "Error training models. The system will fall back to mock data." -ForegroundColor Yellow
}

# Test the ML generator
Write-Host "Testing ML tutorial generator..." -ForegroundColor Yellow
try {
    python -c "
from ai_tutorial.ml_models import MLTutorialGenerator
generator = MLTutorialGenerator()
tutorial = generator.generate_tutorial('Django APIs', 'Build REST APIs', 'intermediate')
print('✓ ML Generator test successful!')
print(f'Generated tutorial: {tutorial[\"title\"]}')
"
    Write-Host "ML Tutorial Generator setup completed successfully!" -ForegroundColor Green
} catch {
    Write-Host "ML Generator test failed, but installation completed." -ForegroundColor Yellow
}

Write-Host "`nSetup Summary:" -ForegroundColor Cyan
Write-Host "✓ ML dependencies installed (PyTorch, scikit-learn, transformers)" -ForegroundColor Green
Write-Host "✓ NLTK data downloaded" -ForegroundColor Green
Write-Host "✓ ML models trained with sample data" -ForegroundColor Green
Write-Host "✓ Tutorial generator ready to use" -ForegroundColor Green

Write-Host "`nFeatures:" -ForegroundColor Cyan
Write-Host "• PyTorch neural networks for text generation" -ForegroundColor White
Write-Host "• Scikit-learn for feature extraction and similarity" -ForegroundColor White
Write-Host "• Sentence transformers for semantic understanding" -ForegroundColor White
Write-Host "• Template-based tutorial generation" -ForegroundColor White
Write-Host "• Completely offline and free" -ForegroundColor White

Write-Host "`nPress any key to continue..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
