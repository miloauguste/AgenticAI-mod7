"""
Quick install and run script
"""
import subprocess
import sys
import os

def install_package(package):
    """Install a package using pip"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        return True
    except subprocess.CalledProcessError:
        return False

def main():
    print("Installing Streamlit...")
    
    # Install essential packages
    packages = [
        "streamlit",
        "plotly", 
        "pandas",
        "python-dotenv"
    ]
    
    for package in packages:
        print(f"Installing {package}...")
        if install_package(package):
            print(f"✅ {package} installed")
        else:
            print(f"❌ Failed to install {package}")
    
    print("\nInstallation complete!")
    print("Run: streamlit run streamlit_app.py")

if __name__ == "__main__":
    main()