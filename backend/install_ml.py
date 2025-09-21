#!/usr/bin/env python3
"""
Install Machine Learning dependencies for IT Support System
"""

import subprocess
import sys
import os

def install_requirements():
    """Install ML requirements"""
    requirements_file = os.path.join(os.path.dirname(__file__), 'requirements_ml.txt')

    if not os.path.exists(requirements_file):
        print("❌ requirements_ml.txt not found!")
        return False

    try:
        print("🤖 Installing Machine Learning dependencies...")
        print("This may take a few minutes...")

        # Install requirements
        result = subprocess.run([
            sys.executable, "-m", "pip", "install", "-r", requirements_file
        ], capture_output=True, text=True)

        if result.returncode == 0:
            print("✅ ML dependencies installed successfully!")
            return True
        else:
            print(f"❌ Installation failed: {result.stderr}")
            return False

    except Exception as e:
        print(f"❌ Error installing dependencies: {e}")
        return False

def test_ml_import():
    """Test if ML libraries can be imported"""
    try:
        import sklearn
        import pandas
        import numpy
        import nltk
        from textblob import TextBlob
        from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

        print("✅ All ML libraries imported successfully!")
        return True

    except ImportError as e:
        print(f"❌ ML library import failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 IT Support System - ML Setup")
    print("=" * 40)

    # Install dependencies
    if install_requirements():
        print("\n🧪 Testing ML imports...")
        if test_ml_import():
            print("\n🎉 ML setup completed successfully!")
            print("You can now run the server with ML capabilities.")
        else:
            print("\n⚠️ ML setup completed but some libraries may have issues.")
    else:
        print("\n❌ ML setup failed. Please check the error messages above.")
        print("You can still run the server without ML features.")
