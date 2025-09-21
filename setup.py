#!/usr/bin/env python3
"""
Setup script for Unified IT Support System
"""

import os
import subprocess
import sys
from pathlib import Path

def run_command(command, cwd=None):
    """Run a command and return the result."""
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            cwd=cwd,
            capture_output=True,
            text=True
        )
        print(f"✓ {command}")
        return result
    except subprocess.CalledProcessError as e:
        print(f"✗ {command}")
        print(f"Error: {e.stderr}")
        return None

def setup_backend():
    """Set up the backend environment."""
    print("\n🔧 Setting up backend...")

    # Create virtual environment
    if not os.path.exists("backend/venv"):
        run_command("python -m venv venv", cwd="backend")

    # Install dependencies
    if os.name == 'nt':  # Windows
        activate_cmd = "venv\\Scripts\\activate"
    else:  # Unix/Linux/MacOS
        activate_cmd = "source venv/bin/activate"

    run_command(f"{activate_cmd} && pip install --upgrade pip", cwd="backend")
    run_command(f"{activate_cmd} && pip install -r requirements.txt", cwd="backend")

    print("✓ Backend setup complete")

def setup_frontend():
    """Set up the frontend environment."""
    print("\n🔧 Setting up frontend...")

    # Install dependencies
    run_command("npm install", cwd="frontend")

    print("✓ Frontend setup complete")

def create_env_file():
    """Create environment file from template."""
    print("\n🔧 Creating environment file...")

    if not os.path.exists(".env"):
        if os.path.exists("env.example"):
            run_command("cp env.example .env")
            print("✓ Created .env file from template")
            print("⚠️  Please update .env with your actual configuration values")
        else:
            print("⚠️  env.example not found, please create .env manually")
    else:
        print("✓ .env file already exists")

def main():
    """Main setup function."""
    print("🚀 Setting up Unified IT Support System")
    print("=" * 50)

    # Check if we're in the right directory
    if not os.path.exists("backend") or not os.path.exists("frontend"):
        print("❌ Please run this script from the project root directory")
        sys.exit(1)

    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        sys.exit(1)

    # Check Node.js
    result = run_command("node --version")
    if not result:
        print("❌ Node.js is required but not installed")
        sys.exit(1)

    # Setup components
    setup_backend()
    setup_frontend()
    create_env_file()

    print("\n🎉 Setup complete!")
    print("\nNext steps:")
    print("1. Update .env file with your configuration")
    print("2. Run 'docker-compose up' to start the application")
    print("3. Or run manually:")
    print("   - Backend: cd backend && python main.py")
    print("   - Frontend: cd frontend && npm start")
    print("\nAccess the application at http://localhost:3000")

if __name__ == "__main__":
    main()

