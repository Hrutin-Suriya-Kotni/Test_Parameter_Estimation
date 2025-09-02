# CRED Conversation Analysis - Modular Architecture

A modular, scalable Python tool for analyzing CRED customer service conversations using multiple AI models. The system is designed to be easily extensible for new models and conversation types.

## 🏗️ Architecture Overview

The system is built with a modular architecture that separates concerns and makes it easy to add new models:

```
Check_DATA/
├── model_clients/           # AI model client implementations
│   ├── __init__.py
│   ├── base_client.py      # Abstract base class for all models
│   ├── mistral_client.py   # Mistral model client (local OpenChat)
│   └── gemini_client.py    # Gemini model client (Google API)
├── test_runners/           # Test execution framework
│   ├── __init__.py
│   ├── base_test_runner.py # Base test runner with common functionality
│   ├── test_mistral.py     # Mistral-specific test runner
│   ├── test_gemini.py      # Gemini-specific test runner
│   ├── test_comparison.py  # Model comparison test runner
│   └── run_all_models.py   # Master test runner for all models
├── results/                # Organized results storage
│   ├── mistral/           # Mistral-specific results
│   ├── gemini/            # Gemini-specific results
│   └── comparison/        # Model comparison results
├── run_tests.py           # Easy test launcher from root
├── model_config.py        # Model configuration and registry
└── [existing files...]    # Original project files
```

## 🚀 Quick Start

### 1. Setup Environment
```bash
# Install dependencies
pip install -r requirements.txt

# Create .env file with your API keys
echo "GEMINI_API_KEY=your_gemini_api_key_here" > .env
```

### 2. Test Individual Models
```bash
# Easy launcher (recommended)
python run_tests.py

# Or run directly from test_runners directory
python test_runners/test_mistral.py
python test_runners/test_gemini.py
```

### 3. Compare Models
```bash
# Easy launcher (recommended)
python run_tests.py

# Or run directly
python test_runners/test_comparison.py
```

### 4. Run All Models
```bash
# Easy launcher (recommended)
python run_tests.py

# Or run directly
python test_runners/run_all_models.py
```

## 📊 Available Models

### Currently Supported Models

| Model | Type | Description | API Key Required |
|-------|------|-------------|------------------|
| **Mistral** | Local | Mistral model via OpenChat server | No |
| **Gemini** | Cloud | Google Gemini 2.0 Flash via API | Yes |

### Adding New Models

To add a new model, follow these steps:

1. **Create Model Client** (`model_clients/new_model_client.py`):
```python
from model_clients.base_client import BaseModelClient

class NewModelClient(BaseModelClient):
    def __init__(self):
        super().__init__("NewModel")
        # Initialize your model-specific settings
    
    def initialize(self) -> bool:
        # Initialize your model client
        pass
    
    def analyze_conversation(self, prompt: str, transcript: str) -> str:
        # Implement conversation analysis
        pass
    
    def test_connection(self) -> bool:
        # Test model connectivity
        pass
```

2. **Register Model** in `model_config.py`:
```python
AVAILABLE_MODELS = {
    # ... existing models ...
    'new_model': {
        'class_name': 'NewModelClient',
        'module_path': 'model_clients.new_model_client',
        'display_name': 'New Model',
        'description': 'Description of the new model',
        'requires_api_key': True,
        'api_key_env_var': 'NEW_MODEL_API_KEY',
        'config': {
            'api_url': 'https://api.newmodel.com',
            'model': 'new-model-v1',
            'max_tokens': 512,
            'temperature': 0.1
        }
    }
}
```

3. **Create Test Runner** (`test_runners/test_new_model.py`):
```python
from model_clients.new_model_client import NewModelClient
from test_runners.base_test_runner import BaseTestRunner
from prompts import ASSESSMENT_PROMPTS

class NewModelTestRunner:
    def __init__(self):
        self.model_client = NewModelClient()
        # ... rest of implementation
```

## 🧪 Test Types

The system supports 5 conversation analysis types:

1. **Opening** - Agent greeting and introduction protocols
2. **Closing** - Call closing and feedback request protocols  
3. **Reassurance** - Customer reassurance statements
4. **Hold** - Proper hold request procedures
5. **Further Assistance** - Additional help offers

## 📁 Results Organization

Results are automatically organized by model and test type:

```
results/
├── mistral/
│   ├── opening_test_results_20250101_120000.csv
│   ├── closing_test_results_20250101_120500.csv
│   └── ...
├── gemini/
│   ├── opening_test_results_20250101_120000.csv
│   ├── closing_test_results_20250101_120500.csv
│   └── ...
└── comparison/
    ├── opening_comparison_results_20250101_120000.csv
    ├── closing_comparison_results_20250101_120500.csv
    └── ...
```

## 🔧 Configuration

### Model Configuration
Edit `model_config.py` to:
- Add new models
- Modify existing model settings
- Configure API endpoints and parameters

### Environment Variables
Create a `.env` file with your API keys:
```bash
# Google Gemini API Key
GEMINI_API_KEY=your_gemini_api_key_here

# Add other model API keys as needed
# NEW_MODEL_API_KEY=your_new_model_api_key_here
```

### Test Parameters
Modify test parameters in individual test runners:
- `max_conversations`: Limit number of conversations to test
- `REQUEST_TIMEOUT`: API request timeout
- `RETRY_DELAY`: Delay between API calls

## 🎯 Usage Examples

### Test Single Model
```bash
# Test Mistral on opening conversations only
python run_tests.py
# Select option 1, then follow prompts

# Or run directly
python test_runners/test_mistral.py
# Select option 2, then select "opening"
```

### Compare Models
```bash
# Compare Mistral vs Gemini on all conversation types
python run_tests.py
# Select option 3, then follow prompts

# Or run directly
python test_runners/test_comparison.py
# Select option 2 for all test types
```

### Run All Models
```bash
# Run all available models on all conversation types
python run_tests.py
# Select option 4, then follow prompts

# Or run directly
python test_runners/run_all_models.py
# Select option 4 for comprehensive testing
```

## 📊 Output Analysis

### Individual Model Results
Each model generates CSV files with:
- Conversation ID and transcript preview
- Model result (Met/Not Met)
- Evidence from the conversation
- Response time and success status

### Comparison Results
Comparison files include:
- Side-by-side results from all models
- Agreement analysis between models
- Performance metrics comparison
- Success rate statistics

## 🔍 Troubleshooting

### Model Initialization Issues
```bash
# Check model status
python model_config.py
```

### API Connection Problems
- **Mistral**: Ensure OpenChat server is running at `http://192.168.30.239:8000/chat`
- **Gemini**: Verify API key in `.env` file and check quota

### Test Failures
- Check console output for specific error messages
- Verify data files are in the correct location
- Ensure sufficient API quota/credits

## 🚀 Performance Tips

1. **Start Small**: Begin with 5-10 conversations to test setup
2. **Monitor Progress**: Watch console output for real-time results
3. **Check Results**: Review CSV output for detailed analysis
4. **Iterate**: Adjust prompts based on results
5. **Scale Up**: Increase conversation count once setup is validated

## 🔮 Future Enhancements

The modular architecture makes it easy to add:
- New AI models (Claude, GPT-4, etc.)
- Additional conversation analysis types
- Real-time monitoring dashboards
- Automated report generation
- Model performance analytics

## 📝 Migration from Old Structure

If you have existing test files in `test_files/`, they will continue to work. The new modular structure provides:
- Better organization
- Easier model addition
- Improved reusability
- Cleaner results storage

## 🆘 Support

For issues:
1. Check the console output for specific error messages
2. Verify your API keys and connectivity
3. Ensure your data files are properly formatted
4. Review the model configuration in `model_config.py`

---

**Status**: ✅ Modular Architecture Complete - Ready for Multi-Model Testing
**Last Updated**: Current session
**Next Action**: Test the new modular structure with your available models
