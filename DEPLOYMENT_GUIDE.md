# Streamlit Community Cloud Deployment Guide

## Quick Fix for CrewAI Version Error

The error you're encountering is due to Python version compatibility. Here's how to fix it:

### Option 1: Use Updated Requirements (Recommended)

Replace your `requirements.txt` with the updated version that includes:

```txt
# Streamlit Community Cloud Compatible Requirements
streamlit
pandas
plotly
matplotlib
requests
python-dotenv

# LangChain ecosystem - use latest versions that auto-resolve dependencies
langchain
langchain-openai
langgraph
openai

# Search and web tools
ddgs
google-search-results
serpapi

# AI providers (optional - will work without API keys)
anthropic
google-generativeai

# Text processing
tiktoken
beautifulsoup4
lxml

# Optional: Only install if compatible with current Python version
# crewai
```

### Option 2: Force Python 3.11

Add a `runtime.txt` file to your repository root:

```txt
python-3.11
```

### Option 3: Use Compatible CrewAI Version

If you need CrewAI, use a compatible version:

```txt
crewai>=0.193.0
```

## Features Available Without CrewAI

The app has been updated to work gracefully without CrewAI:

✅ **Available Features:**
- Basic Content Pipeline (LangGraph + LangChain)
- Human Editor Review System
- Content Analytics Dashboard
- Claude AI Studio (if API key provided)
- Gemini Analysis Tools (if API key provided)
- Real-time DuckDuckGo Search Integration
- Content Feedback Loop

❌ **Unavailable Features (without CrewAI):**
- Advanced Autonomous System
- Enhanced Multi-Agent Workflows

## Deployment Steps

1. **Update files in your repository:**
   ```
   requirements.txt  (use the updated version above)
   runtime.txt       (add this file with "python-3.11")
   ```

2. **Commit and push to your repository**

3. **Deploy on Streamlit Community Cloud:**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Connect your GitHub repository
   - Select your main script file (streamlit_ui.py)
   - Deploy

## Environment Variables (Optional)

Add these to your Streamlit Cloud app settings for full functionality:

```
OPENAI_API_KEY=your_openai_key
CLAUDE_API_KEY=your_claude_key
GEMINI_API_KEY=your_gemini_key
SERPAPI_API_KEY=your_serpapi_key
```

## Troubleshooting

### If you still get dependency errors:

1. **Clear the cache:** In Streamlit Cloud, go to your app settings and clear the cache
2. **Restart the app:** Force restart from the app settings
3. **Check Python version:** Ensure `runtime.txt` contains `python-3.11`

### If some features don't work:

- The app will show warning messages for unavailable features
- Check the System Status in the sidebar to see what's available
- Core functionality (Basic Pipeline + Human Editor) will always work

## Performance Optimization

For better performance on Streamlit Cloud:

1. **Enable caching** for API calls
2. **Use session state** efficiently
3. **Minimize large dependencies**

The app has been optimized to gracefully handle missing dependencies and provide fallback functionality.