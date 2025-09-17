# 🍕 Pizzaria Forecast Demo

A machine learning-powered pizzaria sales forecasting application built with FastAPI backend and Streamlit frontend.

## 🚀 Features

- **FastAPI Backend**: RESTful API for pizza sales forecasting
- **Streamlit Frontend**: Interactive dashboard and login interface  
- **Machine Learning**: XGBoost model for sales predictions
- **Weather Integration**: Weather data API integration
- **14-day Forecasting**: Automated predictions with confidence intervals
- **Excel Export**: Download forecast data as Excel files

## 🛠️ VS Code Setup with GitHub Copilot

This project is optimized for development with VS Code and GitHub Copilot.

### Quick Start

1. **Open in VS Code**:
   ```bash
   code pizzaria-forecast-demo.code-workspace
   ```

2. **Install Recommended Extensions**:
   - VS Code will prompt to install recommended extensions
   - Key extensions: Python, GitHub Copilot, Black Formatter, Pylint

3. **Set up Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

### Available Tasks (Ctrl+Shift+P → "Tasks: Run Task")

- **Start Streamlit App** - Launch main application on port 8501
- **Start Forecast Dashboard** - Launch forecast dashboard on port 8502  
- **Start FastAPI Backend** - Launch API server on port 8000
- **Train ML Model** - Retrain the forecasting model
- **Install Dependencies** - Install Python packages
- **Format Python Code** - Format code with Black

### Debug Configurations

- **Debug Streamlit App** - Debug main Streamlit application
- **Debug Forecast Dashboard** - Debug forecast dashboard
- **Debug FastAPI Backend** - Debug API server with hot reload
- **Debug Python File** - Debug currently open Python file
- **Train ML Model** - Debug model training script
- **Launch Full Stack** - Start both backend and frontend together

### GitHub Copilot Features

- **Code Completion**: AI-powered code suggestions as you type
- **Chat Integration**: Ask Copilot questions about the code
- **Code Explanation**: Get explanations for complex code blocks
- **Test Generation**: Generate tests for your functions
- **Documentation**: Auto-generate docstrings and comments

## 📁 Project Structure

```
pizzaria-forecast-demo/
├── app.py                      # Main Streamlit app with login
├── forecast_dashboard.py       # Forecast visualization dashboard
├── main.py                    # FastAPI backend API
├── train_model.py             # ML model training script
├── Weather_utils.py           # Weather API utilities
├── requirements.txt           # Python dependencies
├── pizza_model.joblib         # Trained ML model
├── demo_forecast.json         # Sample forecast data
├── .vscode/                   # VS Code configuration
│   ├── settings.json          # Editor settings & Copilot config
│   ├── launch.json            # Debug configurations
│   ├── tasks.json             # Build tasks
│   └── extensions.json        # Recommended extensions
└── pizzaria-forecast-demo.code-workspace  # VS Code workspace
```

## 🔧 Development Workflow

1. **Open Workspace**: Double-click `pizzaria-forecast-demo.code-workspace`
2. **Install Extensions**: Accept VS Code's extension recommendations
3. **Activate Environment**: VS Code will auto-detect and activate virtual environment
4. **Start Coding**: Use GitHub Copilot for AI-assisted development
5. **Debug**: Use built-in debug configurations
6. **Test**: Run tasks to start applications

## 🤖 Using GitHub Copilot

### Code Completion
- Type function names or comments describing what you want
- Copilot will suggest complete implementations
- Press Tab to accept suggestions

### Copilot Chat
- Open with Ctrl+Shift+I (Windows/Linux) or Cmd+Shift+I (Mac)
- Ask questions like:
  - "Explain this function"
  - "Add error handling to this code"
  - "Generate tests for this class"
  - "Optimize this algorithm"

### Example Prompts
```python
# Generate a function to validate pizza order data
# Copilot will suggest complete implementation

# Create a test for the forecast endpoint
# Copilot will generate pytest tests

# Add logging to this function
# Copilot will add appropriate logging statements
```

## 🏃‍♂️ Running the Applications

### Method 1: VS Code Tasks
- Press `Ctrl+Shift+P` → "Tasks: Run Task"
- Choose from available tasks

### Method 2: Terminal Commands
```bash
# Start FastAPI backend
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# Start Streamlit main app
streamlit run app.py --server.port 8501

# Start forecast dashboard
streamlit run forecast_dashboard.py --server.port 8502

# Train model
python train_model.py
```

## 🌐 Application URLs

- **Main App**: http://localhost:8501 (Login: Demo/Demo123)
- **Forecast Dashboard**: http://localhost:8502
- **API Backend**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## 📊 API Endpoints

- `GET /` - Health check
- `POST /pizza-forecast` - Single day forecast
- `GET /pizza-forecast-14d` - 14-day forecast
- `GET /download-forecast` - Export forecast as Excel

## 🧪 Model Features

The ML model uses these features for prediction:
- Day of week (0-6)
- Campaign active (0/1)
- Weather temperature (°C)
- Holiday indicator (0/1)
- Rain weather (0/1)
- Weekend evening (0/1)

## 📝 License

This is a demo project for showcasing ML forecasting capabilities.