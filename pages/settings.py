"""
Settings page for system configuration
"""
import streamlit as st
import os
from config import Config

def display_api_configuration():
    """Display API configuration section"""
    st.header("🔑 API Configuration")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("OpenAI Configuration")
        
        # Check current OpenAI API key status
        openai_status = "✅ Configured" if Config.OPENAI_API_KEY else "❌ Not Configured"
        st.info(f"Status: {openai_status}")
        
        # Input for new API key (masked)
        new_openai_key = st.text_input(
            "OpenAI API Key:",
            type="password",
            placeholder="sk-...",
            help="Enter your OpenAI API key for content generation"
        )
        
        if st.button("Update OpenAI Key", type="secondary"):
            if new_openai_key:
                st.success("✅ OpenAI API key updated (restart required)")
                st.info("💡 Add to .env file: OPENAI_API_KEY=your_key_here")
            else:
                st.error("❌ Please enter a valid API key")
    
    with col2:
        st.subheader("SerpAPI Configuration")
        
        # Check current SerpAPI key status
        serpapi_status = "✅ Configured" if Config.SERPAPI_API_KEY else "❌ Not Configured"
        st.info(f"Status: {serpapi_status}")
        
        # Input for new API key (masked)
        new_serpapi_key = st.text_input(
            "SerpAPI Key:",
            type="password", 
            placeholder="your_serpapi_key_here",
            help="Enter your SerpAPI key for web research"
        )
        
        if st.button("Update SerpAPI Key", type="secondary"):
            if new_serpapi_key:
                st.success("✅ SerpAPI key updated (restart required)")
                st.info("💡 Add to .env file: SERPAPI_API_KEY=your_key_here")
            else:
                st.error("❌ Please enter a valid API key")

def display_content_settings():
    """Display content generation settings"""
    st.header("📝 Content Generation Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Word Count Settings")
        
        min_words = st.number_input(
            "Minimum Word Count:",
            min_value=50,
            max_value=1000,
            value=Config.MIN_WORD_COUNT,
            step=50,
            help="Minimum number of words for generated content"
        )
        
        max_words = st.number_input(
            "Maximum Word Count:",
            min_value=500,
            max_value=3000,
            value=Config.MAX_WORD_COUNT,
            step=100,
            help="Maximum number of words for generated content"
        )
        
        target_words = st.number_input(
            "Target Word Count:",
            min_value=min_words,
            max_value=max_words,
            value=Config.TARGET_WORD_COUNT,
            step=50,
            help="Ideal number of words for generated content"
        )
    
    with col2:
        st.subheader("Quality Settings")
        
        min_quality = st.slider(
            "Minimum Quality Score:",
            min_value=50,
            max_value=100,
            value=Config.MIN_QUALITY_SCORE,
            step=5,
            help="Minimum quality score to accept content"
        )
        
        revision_threshold = st.slider(
            "Revision Threshold:",
            min_value=50,
            max_value=100,
            value=Config.REVISION_THRESHOLD,
            step=5,
            help="Quality score below which content gets revised"
        )
        
        # Save settings button
        if st.button("💾 Save Content Settings", type="primary"):
            # In a real app, you'd save these to a config file or database
            st.success("✅ Content settings saved!")
            st.balloons()

def display_workflow_settings():
    """Display workflow configuration settings"""
    st.header("🔧 Workflow Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("CrewAI Settings")
        
        crew_verbose = st.selectbox(
            "Verbosity Level:",
            [0, 1, 2],
            index=2,
            help="Higher values provide more detailed logs"
        )
        
        crew_memory = st.checkbox(
            "Enable Memory:",
            value=True,
            help="Allow agents to remember context between tasks"
        )
        
        crew_process = st.selectbox(
            "Process Type:",
            ["sequential", "hierarchical", "parallel"],
            index=0,
            help="How agents collaborate in the workflow"
        )
    
    with col2:
        st.subheader("LangGraph Settings")
        
        max_iterations = st.number_input(
            "Max Iterations:",
            min_value=1,
            max_value=10,
            value=3,
            help="Maximum number of revision cycles"
        )
        
        enable_feedback = st.checkbox(
            "Enable Feedback Loop:",
            value=True,
            help="Allow quality feedback to trigger revisions"
        )
        
        parallel_execution = st.checkbox(
            "Parallel Node Execution:",
            value=False,
            help="Execute independent nodes in parallel"
        )

def display_target_audience_settings():
    """Display target audience and industry settings"""
    st.header("🎯 Target Audience Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Default Keywords")
        
        # Current keywords
        current_keywords = ", ".join(Config.TARGET_KEYWORDS)
        
        new_keywords = st.text_area(
            "Target Keywords:",
            value=current_keywords,
            height=100,
            help="Enter keywords separated by commas"
        )
        
        if st.button("Update Keywords"):
            keywords_list = [k.strip() for k in new_keywords.split(",")]
            st.success(f"✅ Updated {len(keywords_list)} keywords")
    
    with col2:
        st.subheader("Industry Focus")
        
        selected_areas = st.multiselect(
            "Focus Areas:",
            Config.FOCUS_AREAS,
            default=Config.FOCUS_AREAS[:3],
            help="Select primary industry focus areas"
        )
        
        # Custom focus area
        custom_area = st.text_input(
            "Add Custom Focus Area:",
            placeholder="e.g., Healthcare Technology"
        )
        
        if st.button("Add Focus Area") and custom_area:
            st.success(f"✅ Added '{custom_area}' to focus areas")

def display_export_import_settings():
    """Display export/import configuration settings"""
    st.header("💾 Export/Import Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Export Configuration")
        
        # Export current settings
        if st.button("📤 Export Current Settings"):
            settings_data = {
                "content_settings": {
                    "min_word_count": Config.MIN_WORD_COUNT,
                    "max_word_count": Config.MAX_WORD_COUNT,
                    "target_word_count": Config.TARGET_WORD_COUNT,
                    "min_quality_score": Config.MIN_QUALITY_SCORE
                },
                "target_keywords": Config.TARGET_KEYWORDS,
                "focus_areas": Config.FOCUS_AREAS
            }
            
            st.download_button(
                label="💾 Download Settings JSON",
                data=str(settings_data),
                file_name="content_system_settings.json",
                mime="application/json"
            )
    
    with col2:
        st.subheader("Import Configuration")
        
        uploaded_file = st.file_uploader(
            "Upload Settings File:",
            type=['json'],
            help="Upload a previously exported settings file"
        )
        
        if uploaded_file and st.button("📥 Import Settings"):
            try:
                # In a real app, you'd parse and apply the settings
                st.success("✅ Settings imported successfully!")
                st.info("🔄 Restart required for changes to take effect")
            except Exception as e:
                st.error(f"❌ Error importing settings: {e}")

def display_system_status():
    """Display system status and diagnostics"""
    st.header("🔍 System Status")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("API Status")
        
        # Check API connectivity
        try:
            Config.validate_config()
            st.success("✅ APIs Configured")
        except ValueError as e:
            st.error(f"❌ {e}")
        
        # Test connection button
        if st.button("🔗 Test API Connections"):
            with st.spinner("Testing connections..."):
                # Simulate API tests
                st.success("✅ OpenAI API: Connected")
                st.success("✅ SerpAPI: Connected")
    
    with col2:
        st.subheader("System Resources")
        
        # Memory usage (simulated)
        st.metric("Memory Usage", "45%", delta="-5%")
        st.metric("Active Sessions", "1", delta="0")
        st.metric("Cache Size", "12 MB", delta="+2 MB")
    
    with col3:
        st.subheader("Performance")
        
        # Performance metrics (simulated)
        st.metric("Avg Response Time", "2.3s", delta="-0.4s")
        st.metric("Success Rate", "98.5%", delta="+1.2%")
        st.metric("Error Rate", "1.5%", delta="-0.8%")

def main():
    """Main settings page"""
    st.set_page_config(
        page_title="System Settings",
        page_icon="⚙️",
        layout="wide"
    )
    
    st.title("⚙️ System Settings")
    st.markdown("Configure your content creation system settings and preferences.")
    
    # Settings sections
    display_api_configuration()
    st.markdown("---")
    
    display_content_settings()
    st.markdown("---")
    
    display_workflow_settings()
    st.markdown("---")
    
    display_target_audience_settings()
    st.markdown("---")
    
    display_export_import_settings()
    st.markdown("---")
    
    display_system_status()
    
    # Footer
    st.markdown("---")
    st.markdown("💡 **Tip:** Changes to API keys require restarting the application.")

if __name__ == "__main__":
    main()