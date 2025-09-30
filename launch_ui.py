#!/usr/bin/env python3
"""
Launcher script for the Streamlit UI
"""

import subprocess
import sys
import os

def check_streamlit_installed():
    """Check if Streamlit is installed."""
    try:
        import streamlit
        return True
    except ImportError:
        return False

def install_requirements():
    """Install required packages."""
    print("Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements_streamlit.txt"])
        print("✅ Requirements installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing requirements: {e}")
        return False

def launch_streamlit():
    """Launch the Streamlit application."""
    print("🚀 Launching AI Content Creation Studio...")
    print("📱 The web interface will open in your default browser")
    print("🔗 URL: http://localhost:8501")
    print("\n" + "="*60)
    print("AI CONTENT CREATION STUDIO - STREAMLIT UI")
    print("Innovate Marketing Solutions")
    print("="*60)
    
    try:
        # Launch Streamlit
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "streamlit_ui.py",
            "--server.headless", "false",
            "--server.port", "8501",
            "--browser.gatherUsageStats", "false"
        ])
    except KeyboardInterrupt:
        print("\n\n👋 Shutting down AI Content Creation Studio...")
    except Exception as e:
        print(f"❌ Error launching Streamlit: {e}")

def main():
    """Main launcher function."""
    
    print("="*60)
    print("AI CONTENT CREATION STUDIO LAUNCHER")
    print("Autonomous Multi-Agent Content Creation System")
    print("="*60)
    
    # Check if we're in the right directory
    if not os.path.exists("streamlit_ui.py"):
        print("❌ Error: streamlit_ui.py not found in current directory")
        print("Please run this script from the Module7 directory")
        return
    
    # Check if Streamlit is installed
    if not check_streamlit_installed():
        print("📦 Streamlit not found. Installing requirements...")
        if not install_requirements():
            print("❌ Failed to install requirements. Please install manually:")
            print("pip install -r requirements_streamlit.txt")
            return
    
    # Launch the UI
    launch_streamlit()

if __name__ == "__main__":
    main()