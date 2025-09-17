#!/usr/bin/env python3
"""
Validation script for VS Code Copilot setup
This script tests that all components are properly configured
"""

import os
import json
import sys
from pathlib import Path


def check_file_exists(file_path: str, description: str) -> bool:
    """Check if a file exists and report status"""
    if os.path.exists(file_path):
        print(f"✅ {description}: {file_path}")
        return True
    else:
        print(f"❌ {description}: {file_path} (Missing)")
        return False


def check_json_valid(file_path: str, description: str) -> bool:
    """Check if JSON file is valid"""
    try:
        with open(file_path, 'r') as f:
            json.load(f)
        print(f"✅ {description}: Valid JSON")
        return True
    except Exception as e:
        print(f"❌ {description}: Invalid JSON - {e}")
        return False


def main():
    """Main validation function"""
    print("🔍 Validating VS Code Copilot Setup for Pizzaria Forecast Demo")
    print("=" * 60)
    
    workspace_root = Path(__file__).parent
    os.chdir(workspace_root)
    
    # Check core application files
    print("\n📁 Core Application Files:")
    core_files = [
        ("app.py", "Main Streamlit app"),
        ("main.py", "FastAPI backend"), 
        ("forecast_dashboard.py", "Forecast dashboard"),
        ("train_model.py", "ML model training"),
        ("requirements.txt", "Python dependencies"),
        ("pizza_model.joblib", "Trained ML model")
    ]
    
    for file_path, desc in core_files:
        check_file_exists(file_path, desc)
    
    # Check VS Code configuration
    print("\n🛠️ VS Code Configuration:")
    vscode_files = [
        (".vscode/settings.json", "VS Code settings"),
        (".vscode/launch.json", "Debug configurations"),
        (".vscode/tasks.json", "Build tasks"),
        (".vscode/extensions.json", "Recommended extensions"),
        ("pizzaria-forecast-demo.code-workspace", "VS Code workspace")
    ]
    
    for file_path, desc in vscode_files:
        if check_file_exists(file_path, desc):
            if file_path.endswith('.json'):
                check_json_valid(file_path, f"{desc} validation")
    
    # Check project structure
    print("\n📂 Project Structure:")
    check_file_exists(".gitignore", "Git ignore file")
    check_file_exists("README.md", "Documentation")
    
    # Test imports
    print("\n🐍 Python Dependencies:")
    try:
        import streamlit
        print(f"✅ Streamlit: {streamlit.__version__}")
    except ImportError:
        print("❌ Streamlit: Not installed")
    
    try:
        import fastapi
        print(f"✅ FastAPI: {fastapi.__version__}")
    except ImportError:
        print("❌ FastAPI: Not installed")
    
    try:
        import numpy
        print(f"✅ NumPy: {numpy.__version__}")
    except ImportError:
        print("❌ NumPy: Not installed")
    
    try:
        import pandas
        print(f"✅ Pandas: {pandas.__version__}")
    except ImportError:
        print("❌ Pandas: Not installed")
    
    try:
        import xgboost
        print(f"✅ XGBoost: {xgboost.__version__}")
    except ImportError:
        print("❌ XGBoost: Not installed")
    
    # GitHub Copilot readiness check
    print("\n🤖 GitHub Copilot Readiness:")
    
    # Check settings.json for Copilot configuration
    if os.path.exists(".vscode/settings.json"):
        try:
            with open(".vscode/settings.json", 'r') as f:
                settings = json.load(f)
            
            if "github.copilot.enable" in settings:
                print("✅ GitHub Copilot enabled in settings")
            else:
                print("❌ GitHub Copilot not configured in settings")
                
            if settings.get("python.defaultInterpreterPath"):
                print("✅ Python interpreter path configured")
            else:
                print("❌ Python interpreter path not configured")
                
        except Exception as e:
            print(f"❌ Could not read settings.json: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 Setup validation complete!")
    print("\n💡 Next steps:")
    print("1. Open VS Code: code pizzaria-forecast-demo.code-workspace")
    print("2. Install recommended extensions when prompted")
    print("3. Set up virtual environment if needed")
    print("4. Start coding with GitHub Copilot assistance!")


if __name__ == "__main__":
    main()