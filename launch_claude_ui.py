#!/usr/bin/env python3
"""
Launch script for AI Content Creation Studio with Claude Integration
"""

import subprocess
import sys
import os

def main():
    """Launch the Streamlit UI with Claude AI integration."""
    
    print("=" * 60)
    print("🚀 AI CONTENT CREATION STUDIO WITH CLAUDE AI")
    print("=" * 60)
    print()
    print("🤖 Features Available:")
    print("• Claude AI-powered content generation")
    print("• Gemini LLM content summarization")
    print("• Multi-agent autonomous systems")
    print("• Advanced content optimization")
    print("• Quality analysis and validation")
    print()
    print("📋 Available Processing Modes:")
    print("• Basic Pipeline (Fast)")
    print("• Advanced Autonomous System")
    print("• Enhanced with Gemini Analysis")
    print("• 🆕 Claude AI-Powered (Elite)")
    print()
    print("🔧 Setup:")
    print("• Set CLAUDE_API_KEY or ANTHROPIC_API_KEY for Claude features")
    print("• Set GEMINI_API_KEY for Gemini features")
    print("• Set OPENAI_API_KEY for OpenAI features")
    print("• All features work in mock mode without API keys")
    print()
    print("🌐 Starting Streamlit UI...")
    print()
    
    try:
        # Change to the script directory
        script_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(script_dir)
        
        # Launch Streamlit
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", 
            "streamlit_ui.py",
            "--server.port", "8501",
            "--server.address", "localhost"
        ])
        
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye! Thanks for using AI Content Creation Studio!")
    except Exception as e:
        print(f"\n❌ Error launching Streamlit: {e}")
        print("\nTry running manually with:")
        print("streamlit run streamlit_ui.py")

if __name__ == "__main__":
    main()