# 🚀 Innovate Marketing Solutions - Multi-Agent Content Creation System

A comprehensive AI-powered content creation system designed for digital marketing agencies and technology startups. This system leverages multiple AI agents to automate research, writing, SEO optimization, and quality assurance processes.

## 🎯 Features

### Multi-Agent Architecture
- **Research Agent**: Automated topic research and trend analysis using SerpAPI
- **Content Writing Agent**: AI-powered content generation for multiple formats
- **SEO Specialist Agent**: Search engine optimization and keyword integration
- **Quality Assurance Agent**: Automated content review and quality scoring

### Dual Workflow Systems
- **CrewAI Implementation**: Sequential agent collaboration with memory
- **LangGraph Implementation**: State-based workflow with conditional logic

### Streamlit Web Interface
- **Interactive Dashboard**: Real-time content generation with progress tracking
- **Analytics Dashboard**: Performance metrics and workflow comparison
- **Settings Panel**: Configuration management and API key setup
- **Export Features**: Download content in multiple formats (TXT, JSON)

## 📋 Requirements

- Python 3.8+
- OpenAI API Key
- SerpAPI Key (for web research)

## 🚀 Quick Start

### 1. Installation

```bash
# Clone or download the project files
cd Module7

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit .env file with your API keys
OPENAI_API_KEY=your_openai_api_key_here
SERPAPI_API_KEY=your_serpapi_api_key_here
```

### 3. Run the Application

**Option A: Quick Start (Recommended)**
```bash
python run_app.py
```

**Option B: Direct Streamlit**
```bash
streamlit run streamlit_app.py
```

The application will open in your browser at `http://localhost:8501`

## 🎮 Usage Guide

### Main Interface
1. **Topic Input**: Enter your content topic or use suggested topics
2. **Workflow Selection**: Choose between CrewAI or LangGraph workflows
3. **Content Type**: Select blog post, social media, or website copy
4. **Generate**: Click the generate button and watch the AI agents work
5. **Review**: Examine generated content, quality scores, and analytics
6. **Export**: Download content in your preferred format

### Dashboard Analytics
- View content generation metrics
- Compare workflow performance
- Track quality scores over time
- Monitor content type distribution

### Settings Configuration
- Manage API keys
- Adjust content parameters (word count, quality thresholds)
- Configure workflow settings
- Set target keywords and industry focus

## 🏗️ System Architecture

```
┌─────────────────┐    ┌─────────────────┐
│   Streamlit UI  │    │  Configuration  │
└─────────┬───────┘    └─────────┬───────┘
          │                      │
          ▼                      ▼
┌─────────────────────────────────────────┐
│           Workflow Manager              │
├─────────────────┬───────────────────────┤
│    CrewAI       │      LangGraph        │
│   Sequential    │    State-Based        │
└─────────┬───────┴───────────┬───────────┘
          │                   │
          ▼                   ▼
┌─────────────────────────────────────────┐
│              AI Agents                  │
├─────────┬─────────┬─────────┬───────────┤
│Research │ Writer  │   SEO   │    QA     │
│ Agent   │ Agent   │ Agent   │  Agent    │
└─────────┴─────────┴─────────┴───────────┘
          │
          ▼
┌─────────────────────────────────────────┐
│              Tools Layer                │
├─────────┬─────────┬─────────┬───────────┤
│SerpAPI  │OpenAI   │SEO Tool │QA Tool    │
│Research │Content  │Optimizer│Validator  │
└─────────┴─────────┴─────────┴───────────┘
```

## 📂 Project Structure

```
Module7/
├── streamlit_app.py          # Main Streamlit application
├── main.py                   # CrewAI workflow implementation
├── langgraph_workflow.py     # LangGraph workflow implementation
├── config.py                 # Configuration management
├── run_app.py               # Startup script
├── demo.py                  # Command-line demo
├── requirements.txt         # Python dependencies
├── .env.example            # Environment template
├── pages/
│   ├── dashboard.py        # Analytics dashboard
│   └── settings.py         # Settings configuration
└── tools/
    ├── research_tool.py    # Web research tool
    ├── writing_tool.py     # Content generation tool
    └── SEO_tool.py        # SEO optimization tool
```

## 🔧 Configuration Options

### Content Settings
- **Word Count**: Min/max/target word counts
- **Quality Thresholds**: Minimum quality scores
- **Content Types**: Blog posts, social media, website copy

### Workflow Settings
- **CrewAI**: Memory, verbosity, process type
- **LangGraph**: Iterations, feedback loops, parallel execution

### SEO Settings
- **Target Keywords**: Industry-specific keyword lists
- **Focus Areas**: Technology sectors and specializations

## 📊 Quality Metrics

The system evaluates content across multiple dimensions:

- **Word Count Compliance**: Meets minimum/maximum requirements
- **Grammar Quality**: Sentence structure and completeness
- **Keyword Integration**: Relevant tech/industry keywords
- **Readability**: Appropriate for target audience
- **Brand Consistency**: Maintains professional tone

Quality scores range from 0-100, with 80+ considered excellent.

## 🛠️ Troubleshooting

### Common Issues

**API Key Errors**
```bash
# Verify .env file exists and contains valid keys
cat .env
```

**Package Installation Issues**
```bash
# Upgrade pip and reinstall
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

**Streamlit Won't Start**
```bash
# Check if port 8501 is available
streamlit run streamlit_app.py --server.port 8502
```

### Debug Mode
Enable verbose logging by setting environment variable:
```bash
export STREAMLIT_LOGGER_LEVEL=debug
```

## 🔮 Future Enhancements

- **Multi-language Support**: Content generation in multiple languages
- **Template Library**: Pre-built content templates for different industries
- **Collaboration Features**: Team workflows and content approval processes
- **Integration APIs**: Connect with CMS platforms and social media schedulers
- **Advanced Analytics**: A/B testing and performance tracking
- **Custom Models**: Fine-tuned models for specific client needs

## 🤝 Contributing

This system is designed for Innovate Marketing Solutions' specific needs but can be extended for other use cases:

1. **Custom Agents**: Add specialized agents for specific content types
2. **New Workflows**: Implement alternative orchestration patterns
3. **Tool Integration**: Connect additional APIs and services
4. **UI Enhancements**: Expand Streamlit interface capabilities

## 📄 License

This project is developed for educational and business purposes. Please ensure compliance with API terms of service for OpenAI and SerpAPI.

## 📞 Support

For technical issues or questions about implementation:
- Check the troubleshooting section above
- Review console logs for error messages
- Verify API key configuration in .env file

---

**🚀 Innovate Marketing Solutions** - Powered by AI Multi-Agent Technology