"""
Run the dynamic IT Support System
"""
import asyncio
import subprocess
import sys
import os
from pathlib import Path

def run_command(command, cwd=None):
    """Run a command and return the result"""
    try:
        result = subprocess.run(
            command,
            shell=True,
            cwd=cwd,
            capture_output=True,
            text=True
        )
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def main():
    """Main function to start the dynamic system"""
    print("🚀 Starting Dynamic IT Support System...")

    # Check if we're in the right directory
    if not os.path.exists("prisma/schema.prisma"):
        print("❌ Please run this script from the backend directory")
        sys.exit(1)

    # Install dependencies
    print("📦 Installing dependencies...")
    success, stdout, stderr = run_command("pip install -r requirements.txt")
    if not success:
        print(f"❌ Error installing dependencies: {stderr}")
        sys.exit(1)

    # Generate Prisma client
    print("🔧 Generating Prisma client...")
    success, stdout, stderr = run_command("prisma generate")
    if not success:
        print(f"❌ Error generating Prisma client: {stderr}")
        sys.exit(1)

    # Push database schema
    print("🗄️ Setting up database...")
    success, stdout, stderr = run_command("prisma db push")
    if not success:
        print(f"❌ Error setting up database: {stderr}")
        sys.exit(1)

    # Initialize database with sample data
    print("🌱 Initializing database with sample data...")
    success, stdout, stderr = run_command("python init_database.py")
    if not success:
        print(f"❌ Error initializing database: {stderr}")
        sys.exit(1)

    print("✅ Database setup complete!")
    print("🎯 Starting dynamic IT support system...")
    print("📊 Features enabled:")
    print("   - Real-time system monitoring")
    print("   - Auto-triage and SLA tracking")
    print("   - Role-based access control")
    print("   - AI-powered chatbot")
    print("   - WebSocket real-time updates")
    print("   - Dynamic dashboards")
    print("")
    print("🌐 Server will be available at: http://127.0.0.1:8001")
    print("📚 API documentation: http://127.0.0.1:8001/docs")
    print("")
    print("🔑 Default login credentials:")
    print("   - Admin: admin / admin123")
    print("   - Agent: agent / agent123")
    print("   - Customer: customer / customer123")
    print("")
    print("Press Ctrl+C to stop the server")
    print("=" * 50)

    # Start the server
    try:
        run_command("python main_dynamic.py")
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")

if __name__ == "__main__":
    main()




