"""
Streamlit UI for Innovate Marketing Solutions Multi-Agent Content Creation System
"""
import streamlit as st
import time
import json
from datetime import datetime
from config import Config
from main import run_content_pipeline
from langgraph_workflow import run_langgraph_pipeline

# Page configuration
st.set_page_config(
    page_title="Innovate Marketing Solutions - Content Creator",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

def initialize_session_state():
    """Initialize session state variables"""
    if 'content_history' not in st.session_state:
        st.session_state.content_history = []
    if 'current_result' not in st.session_state:
        st.session_state.current_result = None
    if 'generation_in_progress' not in st.session_state:
        st.session_state.generation_in_progress = False

def display_header():
    """Display the application header"""
    st.title("🚀 Innovate Marketing Solutions")
    st.subheader("Multi-Agent Content Creation System")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Content Types", "3", help="Blog Posts, Social Media, Website Copy")
    with col2:
        st.metric("AI Agents", "4", help="Research, Writing, SEO, Quality Assurance")
    with col3:
        st.metric("Workflows", "2", help="CrewAI and LangGraph implementations")

def sidebar_configuration():
    """Configure sidebar with settings and options"""
    st.sidebar.header("⚙️ Configuration")
    
    # API Key status
    st.sidebar.subheader("🔑 API Status")
    try:
        Config.validate_config()
        st.sidebar.success("✅ API Keys Configured")
    except ValueError as e:
        st.sidebar.error(f"❌ {e}")
        st.sidebar.info("💡 Add API keys to .env file")
    
    # Workflow selection
    st.sidebar.subheader("🔧 Workflow Selection")
    workflow = st.sidebar.radio(
        "Choose workflow type:",
        ["CrewAI (Sequential Agents)", "LangGraph (State-Based)"],
        help="CrewAI uses sequential agent collaboration, LangGraph uses state-based workflows"
    )
    
    # Content type selection
    st.sidebar.subheader("📝 Content Settings")
    content_type = st.sidebar.selectbox(
        "Content Type:",
        ["blog_post", "social_media", "website_copy"],
        help="Select the type of content to generate"
    )
    
    # Advanced settings
    with st.sidebar.expander("🔬 Advanced Settings"):
        min_words = st.number_input("Minimum Words", value=300, min_value=50, max_value=2000)
        max_words = st.number_input("Maximum Words", value=1200, min_value=100, max_value=3000)
        quality_threshold = st.slider("Quality Threshold", min_value=50, max_value=100, value=80)
    
    return {
        "workflow": workflow,
        "content_type": content_type,
        "min_words": min_words,
        "max_words": max_words,
        "quality_threshold": quality_threshold
    }

def content_input_section():
    """Content input section"""
    st.header("💭 Content Creation")
    
    # Topic input
    col1, col2 = st.columns([3, 1])
    
    with col1:
        topic = st.text_input(
            "Enter your topic:",
            placeholder="e.g., AI automation for small businesses",
            help="Describe the topic you want to create content about"
        )
    
    with col2:
        use_suggested = st.button("💡 Use Suggested Topic")
    
    # Suggested topics
    if use_suggested:
        suggested_topics = [
            "AI-powered customer service automation",
            "Blockchain technology for small businesses",
            "Remote work productivity tools for startups",
            "Machine learning for marketing optimization",
            "Cybersecurity essentials for tech startups",
            "Digital transformation strategies",
            "SaaS solutions for enterprise growth",
            "Fintech innovation trends"
        ]
        topic = st.selectbox("Select a suggested topic:", suggested_topics)
    
    # Additional context
    with st.expander("📋 Additional Context (Optional)"):
        target_audience = st.text_input("Target Audience:", placeholder="e.g., Technology professionals, startup founders")
        industry_focus = st.multiselect(
            "Industry Focus:",
            Config.FOCUS_AREAS,
            help="Select relevant industry areas"
        )
        specific_keywords = st.text_area(
            "Specific Keywords:",
            placeholder="Enter keywords separated by commas",
            help="Additional keywords to include in the content"
        )
    
    return {
        "topic": topic,
        "target_audience": target_audience,
        "industry_focus": industry_focus,
        "specific_keywords": specific_keywords
    }

def display_progress_tracker():
    """Display progress tracking for content generation"""
    if st.session_state.generation_in_progress:
        st.header("⏳ Generation Progress")
        
        progress_container = st.container()
        
        with progress_container:
            # Progress bar
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Simulate progress steps
            steps = [
                ("🔍 Researching trending topics...", 25),
                ("✍️ Generating content...", 50),
                ("🔍 Optimizing for SEO...", 75),
                ("✅ Quality assurance check...", 100)
            ]
            
            for step_text, progress in steps:
                status_text.text(step_text)
                progress_bar.progress(progress)
                time.sleep(1)  # Simulate processing time
            
            status_text.text("🎉 Content generation completed!")

def run_content_generation(settings, content_input):
    """Run the content generation process"""
    if not content_input["topic"]:
        st.error("❌ Please enter a topic for content generation")
        return None
    
    try:
        # Validate configuration
        Config.validate_config()
    except ValueError as e:
        st.error(f"❌ Configuration error: {e}")
        return None
    
    st.session_state.generation_in_progress = True
    
    # Display progress
    with st.spinner("🚀 Generating content..."):
        try:
            if "CrewAI" in settings["workflow"]:
                # Run CrewAI workflow
                result = run_content_pipeline(
                    topic=content_input["topic"],
                    content_type=settings["content_type"]
                )
                
                # Format result for display
                formatted_result = {
                    "workflow": "CrewAI",
                    "content": str(result) if result else "Generation failed",
                    "metadata": {
                        "timestamp": datetime.now().isoformat(),
                        "topic": content_input["topic"],
                        "content_type": settings["content_type"]
                    }
                }
                
            else:
                # Run LangGraph workflow
                result = run_langgraph_pipeline(content_input["topic"])
                
                formatted_result = {
                    "workflow": "LangGraph",
                    "content": result.get("final_content", "Generation failed"),
                    "quality_score": result.get("quality_score", 0),
                    "metadata": result.get("metadata", {}),
                    "feedback": result.get("feedback", [])
                }
            
            st.session_state.generation_in_progress = False
            return formatted_result
            
        except Exception as e:
            st.session_state.generation_in_progress = False
            st.error(f"❌ Error during content generation: {e}")
            return None

def display_results(result):
    """Display the generated content results"""
    if not result:
        return
    
    st.header("📄 Generated Content")
    
    # Result tabs
    tab1, tab2, tab3 = st.tabs(["📝 Content", "📊 Analytics", "💾 Export"])
    
    with tab1:
        # Content display
        st.subheader("Generated Content")
        content = result.get("content", "No content generated")
        st.text_area("Content:", content, height=400)
        
        # Quality metrics (for LangGraph)
        if "quality_score" in result:
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Quality Score", f"{result['quality_score']}/100")
            with col2:
                word_count = len(content.split()) if content != "No content generated" else 0
                st.metric("Word Count", word_count)
            
            if result.get("feedback"):
                st.subheader("📋 Quality Feedback")
                for feedback in result["feedback"]:
                    st.info(f"💡 {feedback}")
    
    with tab2:
        # Analytics
        st.subheader("📊 Content Analytics")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Workflow Used", result.get("workflow", "Unknown"))
        
        with col2:
            content_length = len(result.get("content", ""))
            st.metric("Character Count", content_length)
        
        with col3:
            timestamp = result.get("metadata", {}).get("timestamp", "Unknown")
            st.metric("Generated At", timestamp.split("T")[0] if "T" in timestamp else timestamp)
        
        # Metadata display
        if result.get("metadata"):
            st.subheader("📋 Metadata")
            metadata_json = json.dumps(result["metadata"], indent=2)
            st.code(metadata_json, language="json")
    
    with tab3:
        # Export options
        st.subheader("💾 Export Content")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Download as text
            if st.download_button(
                label="📄 Download as TXT",
                data=result.get("content", ""),
                file_name=f"content_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain"
            ):
                st.success("✅ Content downloaded!")
        
        with col2:
            # Download as JSON
            json_data = json.dumps(result, indent=2)
            if st.download_button(
                label="📊 Download as JSON",
                data=json_data,
                file_name=f"content_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            ):
                st.success("✅ Data downloaded!")

def content_history_section():
    """Display content generation history"""
    if st.session_state.content_history:
        st.header("📚 Content History")
        
        for i, item in enumerate(reversed(st.session_state.content_history[-5:])):  # Show last 5
            with st.expander(f"📝 {item.get('metadata', {}).get('topic', 'Unknown Topic')} - {item.get('workflow', 'Unknown')}"):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    preview = item.get('content', '')[:200] + "..." if len(item.get('content', '')) > 200 else item.get('content', '')
                    st.text(preview)
                
                with col2:
                    if st.button(f"🔄 Reload", key=f"reload_{i}"):
                        st.session_state.current_result = item
                        st.experimental_rerun()

def main():
    """Main Streamlit application"""
    initialize_session_state()
    display_header()
    
    # Sidebar configuration
    settings = sidebar_configuration()
    
    # Main content area
    content_input = content_input_section()
    
    # Generation button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Generate Content", type="primary", use_container_width=True):
            result = run_content_generation(settings, content_input)
            if result:
                st.session_state.current_result = result
                st.session_state.content_history.append(result)
                st.experimental_rerun()
    
    # Display results
    if st.session_state.current_result:
        display_results(st.session_state.current_result)
    
    # Content history
    content_history_section()
    
    # Footer
    st.markdown("---")
    st.markdown("🚀 **Innovate Marketing Solutions** - Powered by AI Multi-Agent Technology")

if __name__ == "__main__":
    main()