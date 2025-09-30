"""
Startup script for the Innovate Marketing Solutions Content Creation System
"""
import subprocess
import sys
import os
from pathlib import Path

def check_requirements():
    """Check if required packages are installed"""
    required_packages = [
        'streamlit',
        'crewai', 
        'langgraph',
        'openai',
        'python-dotenv',
        'plotly',
        'pandas'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    return missing_packages

def install_requirements():
    """Install missing requirements"""
    print("📦 Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ All packages installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing packages: {e}")
        return False

def check_env_file():
    """Check if .env file exists"""
    env_path = Path(".env")
    env_example_path = Path(".env.example")
    
    if not env_path.exists():
        print("⚠️ .env file not found!")
        
        if env_example_path.exists():
            print("💡 Creating .env file from template...")
            try:
                with open(env_example_path, 'r') as source:
                    content = source.read()
                
                with open(env_path, 'w') as target:
                    target.write(content)
                
                print("✅ Created .env file from template")
                print("📝 Please edit .env file and add your API keys:")
                print("   - OPENAI_API_KEY=your_openai_key_here")
                print("   - SERPAPI_API_KEY=your_serpapi_key_here")
                return False
            except Exception as e:
                print(f"❌ Error creating .env file: {e}")
                return False
        else:
            print("❌ No .env.example template found")
            return False
    
    return True

def run_streamlit_app():
    """Run the Streamlit application"""
    print("🚀 Starting Innovate Marketing Solutions Content Creation System...")
    
    try:
        # Change to the script directory
        script_dir = Path(__file__).parent
        os.chdir(script_dir)
        
        # Run Streamlit
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "streamlit_app.py",
            "--theme.base", "light",
            "--theme.primaryColor", "#1f77b4",
            "--theme.backgroundColor", "#ffffff",
            "--theme.secondaryBackgroundColor", "#f0f2f6"
        ])
        
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except Exception as e:
        print(f"❌ Error running application: {e}")

def main():
    """Main startup function"""
    print("="*60)
    print("🚀 INNOVATE MARKETING SOLUTIONS")
    print("   Content Creation System Startup")
    print("="*60)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        sys.exit(1)
    
    print(f"✅ Python {sys.version.split()[0]} detected")
    
    # Check for missing packages
    missing = check_requirements()
    if missing:
        print(f"⚠️ Missing packages: {', '.join(missing)}")
        install_choice = input("📦 Install missing packages? (y/n): ").lower().strip()
        
        if install_choice in ['y', 'yes']:
            if not install_requirements():
                print("❌ Failed to install packages. Please install manually:")
                print("   pip install -r requirements.txt")
                sys.exit(1)
        else:
            print("❌ Cannot proceed without required packages")
            sys.exit(1)
    else:
        print("✅ All required packages are installed")
    
    # Check environment configuration
    if not check_env_file():
        print("\n⚠️ Please configure your .env file with API keys before running the application")
        print("📝 Required keys:")
        print("   - OPENAI_API_KEY: Get from https://platform.openai.com/api-keys")
        print("   - SERPAPI_API_KEY: Get from https://serpapi.com/manage-api-key")
        
        continue_anyway = input("\n🤔 Continue without API keys? (y/n): ").lower().strip()
        if continue_anyway not in ['y', 'yes']:
            print("👋 Please set up your API keys and run again")
            sys.exit(0)
    
    print("\n🎯 System ready! Starting Streamlit application...")
    print("📱 The application will open in your default web browser")
    print("🔗 Default URL: http://localhost:8501")
    print("\n💡 Tips:")
    print("   - Use Ctrl+C to stop the application")
    print("   - Refresh browser if needed")
    print("   - Check console for any error messages")
    
    input("\n⏳ Press Enter to start the application...")
    
    # Run the Streamlit app
    run_streamlit_app()

if __name__ == "__main__":
    main()