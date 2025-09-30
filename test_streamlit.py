"""
Test if Streamlit is working properly
"""
import sys

def test_streamlit():
    try:
        import streamlit as st
        print("✅ Streamlit imported successfully")
        print(f"Streamlit version: {st.__version__}")
        return True
    except ImportError as e:
        print(f"❌ Streamlit import failed: {e}")
        return False

def test_other_packages():
    packages = ["pandas", "plotly", "requests"]
    results = []
    
    for package in packages:
        try:
            __import__(package)
            print(f"✅ {package} imported successfully")
            results.append(True)
        except ImportError as e:
            print(f"❌ {package} import failed: {e}")
            results.append(False)
    
    return all(results)

if __name__ == "__main__":
    print("Testing package installations...")
    print(f"Python version: {sys.version}")
    print("-" * 40)
    
    streamlit_ok = test_streamlit()
    other_packages_ok = test_other_packages()
    
    print("-" * 40)
    if streamlit_ok:
        print("🎉 Ready to run Streamlit app!")
        print("Run: streamlit run simple_demo.py")
    else:
        print("❌ Installation issues detected")
        print("Try running: setup_environment.bat")