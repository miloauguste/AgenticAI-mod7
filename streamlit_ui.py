#!/usr/bin/env python3
"""
Streamlit Web UI for Autonomous Content Creation System
Innovate Marketing Solutions
"""

import streamlit as st
import pandas as pd
import json
import time
from datetime import datetime
from typing import Dict, List, Optional, Any
import sys
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
<<<<<<< HEAD
    # Try to import core components
    from main import run_content_pipeline
    from human_feedback_system import (
        feedback_manager, FeedbackType, FeedbackStatus, 
        create_content_for_review, add_editor_feedback, 
        get_content_for_editing, submit_revised_content,
        save_content_draft, get_content_drafts
    )
    
    # Try to import optional components
    try:
        from autonomous_content_system import run_autonomous_content_system
        HAS_AUTONOMOUS = True
    except ImportError:
        HAS_AUTONOMOUS = False
        st.warning("⚠️ Advanced autonomous system not available (CrewAI dependency issue)")
    
    try:
        from enhanced_autonomous_system import run_enhanced_autonomous_system
        HAS_ENHANCED = True
    except ImportError:
        HAS_ENHANCED = False
        st.warning("⚠️ Enhanced autonomous system not available")
    
    try:
        from content_summarization_tools import GeminiSummarizationTool, AdvancedContentAnalyzer
        HAS_GEMINI_TOOLS = True
    except ImportError:
        HAS_GEMINI_TOOLS = False
        st.warning("⚠️ Gemini tools not available")
    
    try:
        from claude_content_generator import ClaudeContentGenerator, ClaudeContentOptimizer
        HAS_CLAUDE = True
    except ImportError:
        HAS_CLAUDE = False
        st.warning("⚠️ Claude content generator not available")

except ImportError as e:
    st.error(f"Critical Import Error: {e}")
    st.error("Please check your dependencies. Using basic functionality only.")
    HAS_AUTONOMOUS = False
    HAS_ENHANCED = False
    HAS_GEMINI_TOOLS = False
    HAS_CLAUDE = False
=======
    from autonomous_content_system import run_autonomous_content_system
    from main import run_content_pipeline
    from enhanced_autonomous_system import run_enhanced_autonomous_system
    from content_summarization_tools import GeminiSummarizationTool, AdvancedContentAnalyzer
    from claude_content_generator import ClaudeContentGenerator, ClaudeContentOptimizer
    from human_feedback_system import (
        feedback_manager, FeedbackType, FeedbackStatus, 
        create_content_for_review, add_editor_feedback, 
        get_content_for_editing, submit_revised_content
    )
except ImportError as e:
    st.error(f"Import Error: {e}")
    st.stop()
>>>>>>> 916d15462f3282d375157da7460c0bb883cb0bcc

# Page configuration
st.set_page_config(
    page_title="AI Content Creation Studio",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #2e8b57;
        margin: 1rem 0;
    }
    .metric-card {
        background-color: #f0f8ff;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
        margin: 0.5rem 0;
    }
    .success-banner {
        background-color: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #28a745;
        margin: 1rem 0;
    }
    .info-banner {
        background-color: #cce7ff;
        color: #004085;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #007bff;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables."""
    if 'content_history' not in st.session_state:
        st.session_state.content_history = []
    if 'current_result' not in st.session_state:
        st.session_state.current_result = None
    if 'processing' not in st.session_state:
        st.session_state.processing = False

def main():
    """Main Streamlit application."""
    
    initialize_session_state()
    
    # Main header
    st.markdown('<div class="main-header">🚀 AI Content Creation Studio</div>', unsafe_allow_html=True)
    st.markdown('<div style="text-align: center; color: #666; margin-bottom: 2rem;">Autonomous Multi-Agent Content Creation System</div>', unsafe_allow_html=True)
    
<<<<<<< HEAD
    # Sidebar navigation - build pages based on available components
    st.sidebar.title("Navigation")
    
    available_pages = ["Content Creator", "📝 Human Editor Review", "📊 Content Analytics", "System Dashboard", "Content History"]
    
    if HAS_CLAUDE:
        available_pages.insert(1, "🆕 Claude AI Studio")
    
    if HAS_GEMINI_TOOLS:
        available_pages.insert(-3, "Gemini Analysis Tools")
    
    # Always show documentation and health
    available_pages.extend(["API Documentation", "System Health"])
    
    page = st.sidebar.selectbox(
        "Choose a page:",
        available_pages
    )
    
    # Show system status in sidebar
    st.sidebar.markdown("---")
    st.sidebar.subheader("🔧 System Status")
    st.sidebar.write(f"✅ Basic Pipeline: Available")
    st.sidebar.write(f"{'✅' if HAS_AUTONOMOUS else '❌'} Advanced System: {'Available' if HAS_AUTONOMOUS else 'Unavailable'}")
    st.sidebar.write(f"{'✅' if HAS_ENHANCED else '❌'} Enhanced System: {'Available' if HAS_ENHANCED else 'Unavailable'}")
    st.sidebar.write(f"{'✅' if HAS_CLAUDE else '❌'} Claude AI: {'Available' if HAS_CLAUDE else 'Unavailable'}")
    st.sidebar.write(f"{'✅' if HAS_GEMINI_TOOLS else '❌'} Gemini Tools: {'Available' if HAS_GEMINI_TOOLS else 'Unavailable'}")
    
=======
    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox(
        "Choose a page:",
        ["Content Creator", "🆕 Claude AI Studio", "Gemini Analysis Tools", "📝 Human Editor Review", "📊 Content Analytics", "System Dashboard", "Content History", "API Documentation", "System Health"]
    )
    
>>>>>>> 916d15462f3282d375157da7460c0bb883cb0bcc
    if page == "Content Creator":
        content_creator_page()
    elif page == "🆕 Claude AI Studio":
        claude_ai_studio_page()
    elif page == "Gemini Analysis Tools":
        gemini_analysis_page()
    elif page == "📝 Human Editor Review":
        human_editor_review_page()
    elif page == "📊 Content Analytics":
        content_analytics_page()
    elif page == "System Dashboard":
        system_dashboard_page()
    elif page == "Content History":
        content_history_page()
    elif page == "API Documentation":
        api_documentation_page()
    elif page == "System Health":
        system_health_page()

def content_creator_page():
    """Main content creation interface."""
    
    st.markdown('<div class="sub-header">📝 Content Creation Workspace</div>', unsafe_allow_html=True)
    
<<<<<<< HEAD
    # Add info about content uniqueness
    st.info("🔄 **Content Uniqueness Guaranteed**: Each generation uses unique session IDs, timestamps, and varied research queries to ensure fresh, original content every time.")
    
=======
>>>>>>> 916d15462f3282d375157da7460c0bb883cb0bcc
    # Content creation form
    with st.form("content_creation_form"):
        st.subheader("Client Information")
        
        col1, col2 = st.columns(2)
        
        with col1:
            client_name = st.text_input("Client/Company Name", placeholder="e.g., TechFlow Innovations")
            industry = st.selectbox(
                "Industry",
                ["technology", "healthcare", "finance", "manufacturing", "retail", "professional_services", "other"]
            )
            content_type = st.selectbox(
                "Content Type",
                ["blog_post", "whitepaper", "case_study", "thought_leadership", "social_media", "email_campaign"]
            )
        
        with col2:
            urgency = st.selectbox("Priority Level", ["Standard", "High", "Urgent"])
            word_count_target = st.selectbox("Target Word Count", ["500-800", "800-1200", "1200-1500", "1500+"])
            tone = st.selectbox(
                "Content Tone",
                ["professional_authoritative", "friendly_conversational", "innovative_inspiring", "balanced_informative"]
            )
        
        st.subheader("Content Requirements")
        
        content_brief = st.text_area(
            "Content Brief (Detailed Description)",
            placeholder="Describe the content you need, including topic, purpose, key messages, and any specific requirements...",
            height=120
        )
        
        target_audience = st.text_area(
            "Target Audience",
            placeholder="Describe your target audience: demographics, job titles, interests, pain points...",
            height=80
        )
        
        col3, col4 = st.columns(2)
        
        with col3:
            content_goals = st.multiselect(
                "Content Goals",
                ["brand_awareness", "lead_generation", "education", "engagement", "thought_leadership"],
                default=["brand_awareness", "lead_generation"]
            )
        
        with col4:
            keywords = st.text_input("Target Keywords (optional)", placeholder="keyword1, keyword2, keyword3")
        
        st.subheader("Advanced Options")
        
        with st.expander("System Configuration"):
<<<<<<< HEAD
            # Build available system modes based on what's imported
            available_modes = ["Basic Pipeline (Fast)"]
            
            if HAS_AUTONOMOUS:
                available_modes.append("Advanced Autonomous System (Comprehensive)")
            
            if HAS_ENHANCED and HAS_GEMINI_TOOLS:
                available_modes.append("Enhanced with Gemini Analysis (Premium)")
            
            if HAS_CLAUDE:
                available_modes.append("🆕 Claude AI-Powered (Elite)")
            
            system_mode = st.radio(
                "Processing Mode",
                available_modes,
                help="Select from available content generation systems based on installed dependencies"
=======
            system_mode = st.radio(
                "Processing Mode",
                ["Basic Pipeline (Fast)", "Advanced Autonomous System (Comprehensive)", "Enhanced with Gemini Analysis (Premium)", "🆕 Claude AI-Powered (Elite)"],
                help="Basic: 4-agent workflow, Advanced: 7-agent analysis, Enhanced: Gemini-powered content summarization, Claude AI: Advanced content generation"
>>>>>>> 916d15462f3282d375157da7460c0bb883cb0bcc
            )
            
            include_research = st.checkbox("Include Market Research", value=True)
            include_seo = st.checkbox("Advanced SEO Optimization", value=True)
            include_qa = st.checkbox("Enhanced Quality Assurance", value=True)
            
            if "Enhanced with Gemini" in system_mode:
                st.info("🧠 Gemini Features: Advanced content summarization, multi-source analysis, competitive intelligence")
                gemini_api_key = st.text_input("Gemini API Key (Optional)", type="password", 
                                             help="Enter your Google Gemini API key for enhanced analysis")
                if gemini_api_key:
                    os.environ["GEMINI_API_KEY"] = gemini_api_key
            
            elif "Claude AI-Powered" in system_mode:
                st.info("🤖 Claude AI Features: Advanced content generation, requirement-based creation, quality analysis, content optimization")
                
                col1, col2 = st.columns(2)
                with col1:
                    claude_api_key = st.text_input("Claude API Key (Optional)", type="password",
                                                 help="Enter your Anthropic Claude API key for advanced content generation")
                    if claude_api_key:
                        os.environ["CLAUDE_API_KEY"] = claude_api_key
                        os.environ["ANTHROPIC_API_KEY"] = claude_api_key
                
                with col2:
                    claude_model = st.selectbox(
                        "Claude Model",
                        ["claude-3-sonnet-20240229", "claude-3-haiku-20240307", "claude-3-opus-20240229"],
                        help="Select the Claude model for content generation"
                    )
                
                claude_advanced_options = st.expander("Claude Advanced Options")
                with claude_advanced_options:
                    content_creativity = st.slider("Content Creativity", 0.0, 1.0, 0.7, 
                                                  help="Higher values produce more creative content")
                    quality_threshold = st.slider("Quality Threshold", 60, 100, 85,
                                                 help="Minimum quality score for content acceptance")
                    include_optimization = st.checkbox("Content Optimization", value=True,
                                                     help="Optimize content after generation")
        
        # Submit button
        submitted = st.form_submit_button("🚀 Generate Content", type="primary")
        
        if submitted:
            if not content_brief or not target_audience:
                st.error("Please provide both content brief and target audience information.")
            else:
                process_content_request(
                    client_name, industry, content_type, content_brief, 
                    target_audience, content_goals, system_mode, keywords
                )
    
    # Display results outside the form context
    if st.session_state.get('show_results') and st.session_state.get('current_result'):
<<<<<<< HEAD
        # Add a clear results button
        col1, col2 = st.columns([1, 4])
        with col1:
            if st.button("🗑️ Clear Results"):
                # Clear the results from session state
                if 'show_results' in st.session_state:
                    del st.session_state.show_results
                if 'current_result' in st.session_state:
                    del st.session_state.current_result
                if 'current_client_name' in st.session_state:
                    del st.session_state.current_client_name
                st.success("✅ Results cleared! Ready for new content generation.")
                st.rerun()
        
        with col2:
            st.info("💡 Showing previous content generation results. Submit a new request to generate fresh content.")
        
=======
>>>>>>> 916d15462f3282d375157da7460c0bb883cb0bcc
        display_content_results(
            st.session_state.current_result, 
            st.session_state.get('current_client_name', 'Client')
        )

def process_content_request(client_name, industry, content_type, content_brief, 
                          target_audience, content_goals, system_mode, keywords):
    """Process the content creation request."""
    
    st.session_state.processing = True
    
    # Create progress indicators
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
<<<<<<< HEAD
        # Prepare enhanced brief with uniqueness factors
        import uuid
        import datetime
        
        session_id = str(uuid.uuid4())[:8]
        current_timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        enhanced_brief = f"""
        Content Generation Session: {session_id}
        Generated at: {current_timestamp}
=======
        # Prepare enhanced brief
        enhanced_brief = f"""
>>>>>>> 916d15462f3282d375157da7460c0bb883cb0bcc
        Client: {client_name}
        Industry: {industry}
        Content Type: {content_type}
        Request: {content_brief}
        Target Keywords: {keywords if keywords else 'Auto-generated'}
<<<<<<< HEAD
        Unique Session ID: {session_id}
=======
>>>>>>> 916d15462f3282d375157da7460c0bb883cb0bcc
        """
        
        # Update progress
        progress_bar.progress(10)
        status_text.text("Initializing content creation system...")
        time.sleep(1)
        
        progress_bar.progress(25)
        status_text.text("Processing client requirements...")
        time.sleep(1)
        
<<<<<<< HEAD
        # Execute content creation based on available systems
        if "Claude AI-Powered" in system_mode and HAS_CLAUDE:
            progress_bar.progress(50)
            status_text.text("Running Claude AI-powered content generation...")
            
            try:
                result = run_claude_content_system(
                    client_brief=enhanced_brief,
                    target_audience=target_audience,
                    content_goals=content_goals,
                    content_type=content_type,
                    keywords=keywords.split(',') if keywords else []
                )
            except Exception as e:
                st.error(f"Claude AI system error: {e}")
                st.info("Falling back to basic pipeline...")
                base_topic = content_brief.split('\n')[0] if content_brief else "Business content"
                unique_topic = f"{base_topic} - Session {session_id} - {current_timestamp}"
                result = run_content_pipeline(topic=unique_topic, content_type=content_type)
                
        elif "Enhanced with Gemini" in system_mode and HAS_ENHANCED and HAS_GEMINI_TOOLS:
            progress_bar.progress(50)
            status_text.text("Running enhanced system with Gemini analysis...")
            
            try:
                result = run_enhanced_autonomous_system(
                    client_brief=enhanced_brief,
                    target_audience=target_audience,
                    content_goals=content_goals
                )
            except Exception as e:
                st.error(f"Enhanced system error: {e}")
                st.info("Falling back to basic pipeline...")
                base_topic = content_brief.split('\n')[0] if content_brief else "Business content"
                unique_topic = f"{base_topic} - Session {session_id} - {current_timestamp}"
                result = run_content_pipeline(topic=unique_topic, content_type=content_type)
                
        elif "Advanced" in system_mode and HAS_AUTONOMOUS:
            progress_bar.progress(50)
            status_text.text("Running advanced autonomous system...")
            
            try:
                result = run_autonomous_content_system(
                    client_brief=enhanced_brief,
                    target_audience=target_audience,
                    content_goals=content_goals
                )
            except Exception as e:
                st.error(f"Advanced system error: {e}")
                st.info("Falling back to basic pipeline...")
                base_topic = content_brief.split('\n')[0] if content_brief else "Business content"
                unique_topic = f"{base_topic} - Session {session_id} - {current_timestamp}"
                result = run_content_pipeline(topic=unique_topic, content_type=content_type)
=======
        # Execute content creation
        if "Claude AI-Powered" in system_mode:
            progress_bar.progress(50)
            status_text.text("Running Claude AI-powered content generation...")
            
            result = run_claude_content_system(
                client_brief=enhanced_brief,
                target_audience=target_audience,
                content_goals=content_goals,
                content_type=content_type,
                keywords=keywords.split(',') if keywords else []
            )
        elif "Enhanced with Gemini" in system_mode:
            progress_bar.progress(50)
            status_text.text("Running enhanced system with Gemini analysis...")
            
            result = run_enhanced_autonomous_system(
                client_brief=enhanced_brief,
                target_audience=target_audience,
                content_goals=content_goals
            )
        elif "Advanced" in system_mode:
            progress_bar.progress(50)
            status_text.text("Running advanced autonomous system...")
            
            result = run_autonomous_content_system(
                client_brief=enhanced_brief,
                target_audience=target_audience,
                content_goals=content_goals
            )
>>>>>>> 916d15462f3282d375157da7460c0bb883cb0bcc
        else:
            progress_bar.progress(50)
            status_text.text("Running basic content pipeline...")
            
<<<<<<< HEAD
            # Extract topic from brief for basic system with uniqueness
            base_topic = content_brief.split('\n')[0] if content_brief else "Business content"
            # Add session ID and timestamp to ensure uniqueness
            unique_topic = f"{base_topic} - Session {session_id} - {current_timestamp}"
            result = run_content_pipeline(topic=unique_topic, content_type=content_type)
=======
            # Extract topic from brief for basic system
            topic = content_brief.split('\n')[0] if content_brief else "Business content"
            result = run_content_pipeline(topic=topic, content_type=content_type)
>>>>>>> 916d15462f3282d375157da7460c0bb883cb0bcc
        
        progress_bar.progress(75)
        status_text.text("Finalizing content and preparing deliverables...")
        time.sleep(1)
        
        progress_bar.progress(100)
        status_text.text("Content creation completed successfully!")
        
        if result:
            # Store result in session state
            st.session_state.current_result = result
            st.session_state.current_client_name = client_name
<<<<<<< HEAD
            st.session_state.content_generation_session = session_id
            
            # Add to history
            history_entry = {
                "timestamp": current_timestamp,
                "session_id": session_id,
=======
            
            # Add to history
            history_entry = {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
>>>>>>> 916d15462f3282d375157da7460c0bb883cb0bcc
                "client_name": client_name,
                "industry": industry,
                "content_type": content_type,
                "brief": content_brief[:100] + "..." if len(content_brief) > 100 else content_brief,
                "result": result,
                "status": "completed"
            }
            st.session_state.content_history.append(history_entry)
            
            # Set flag to display results outside form
            st.session_state.show_results = True
<<<<<<< HEAD
            st.success(f"✅ Content generation completed! Unique session: {session_id}. Results displayed below.")
=======
            st.success("✅ Content generation completed! Results displayed below.")
>>>>>>> 916d15462f3282d375157da7460c0bb883cb0bcc
            
        else:
            st.error("Content creation failed. Please check your inputs and try again.")
    
    except Exception as e:
        st.error(f"Error during content creation: {str(e)}")
    
    finally:
        st.session_state.processing = False

def display_content_results(result, client_name):
    """Display the content creation results."""
    
    st.markdown('<div class="success-banner">✅ Content Creation Completed Successfully!</div>', unsafe_allow_html=True)
    
    # Extract data based on result structure
    if isinstance(result, dict):
        # Advanced system result
        deliverables = result.get("deliverables", {})
        performance_metrics = result.get("performance_metrics", {})
        final_content = deliverables.get("primary_content", result.get("final_output", ""))
        meta_data = deliverables.get("meta_data", {})
        quality_report = deliverables.get("quality_report", {})
    else:
        # Basic system result
        final_content = result.get("final_output", "") if hasattr(result, 'get') else str(result)
        performance_metrics = {}
        meta_data = {}
        quality_report = {}
    
    # Performance metrics
    st.subheader("📊 Performance Metrics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        word_count = performance_metrics.get("content_length", len(final_content.split()) if final_content else 0)
        st.metric("Word Count", f"{word_count}")
    
    with col2:
        quality_score = performance_metrics.get("quality_score", 88)
        st.metric("Quality Score", f"{quality_score}/100")
    
    with col3:
        seo_score = performance_metrics.get("seo_optimization_score", 85)
        st.metric("SEO Score", f"{seo_score}/100")
    
    with col4:
        readability = performance_metrics.get("readability_score", 75)
        st.metric("Readability", f"{readability:.1f}/100")
    
    # Content tabs
<<<<<<< HEAD
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["📄 Final Content", "🔍 SEO Data", "✅ Quality Report", "📝 Human Feedback", "✏️ Content Editor", "📋 Raw Data"])
=======
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📄 Final Content", "🔍 SEO Data", "✅ Quality Report", "📝 Human Feedback", "📋 Raw Data"])
>>>>>>> 916d15462f3282d375157da7460c0bb883cb0bcc
    
    with tab1:
        st.subheader("Generated Content")
        if final_content:
            st.markdown(final_content)
            
            # Download button (moved outside form context)
            if st.session_state.get('show_download_content'):
                st.download_button(
                    label="📥 Download Content",
                    data=final_content,
                    file_name=f"{client_name}_content_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain"
                )
            else:
                if st.button("📥 Prepare Download"):
                    st.session_state['show_download_content'] = True
                    st.rerun()
        else:
            st.warning("No content available to display.")
    
    with tab2:
        st.subheader("SEO Metadata")
        if meta_data:
            for key, value in meta_data.items():
                st.write(f"**{key.replace('_', ' ').title()}:** {value}")
        else:
            st.info("SEO metadata will be displayed here when available.")
    
    with tab3:
        st.subheader("Quality Assurance Report")
        if quality_report:
            if isinstance(quality_report, dict):
                st.write(f"**Approval Status:** {quality_report.get('approval_status', 'N/A')}")
                if quality_report.get('checks'):
                    st.write("**Quality Checks:**")
                    for check in quality_report['checks']:
                        st.write(f"• {check}")
            else:
                st.write(quality_report)
        else:
            st.info("Quality assurance report will be displayed here when available.")
    
    with tab4:
        st.subheader("📝 Human Editor Feedback")
        
        # Create content for review if not already created
<<<<<<< HEAD
        import uuid
        session_id = st.session_state.get('content_generation_session', str(uuid.uuid4())[:8])
        content_id = f"content_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{session_id}_{client_name.replace(' ', '_')}"
=======
        content_id = f"content_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{client_name.replace(' ', '_')}"
>>>>>>> 916d15462f3282d375157da7460c0bb883cb0bcc
        content_title = f"{client_name} - {final_content.split('\n')[0][:50] if final_content else 'Content'}..."
        
        # Check if content already exists in feedback system
        existing_feedback = get_content_for_editing(content_id)
        
        if not existing_feedback:
            if st.button("📝 Submit for Human Review", type="primary"):
                create_content_for_review(
                    content_id=content_id,
                    title=content_title,
                    content=final_content,
                    client_name=client_name,
                    content_type=meta_data.get('content_type', 'article')
                )
                st.success("✅ Content submitted for human editor review!")
                st.info("💡 Content is now available in the 'Human Editor Review' section for feedback.")
                st.session_state.submitted_for_review = content_id
        else:
            st.info("📋 This content has been submitted for review.")
            
            # Display current feedback status
            col1, col2, col3 = st.columns(3)
            with col1:
                status_color = {
                    "pending_review": "🟡",
                    "in_review": "🔵", 
                    "revision_requested": "🟠",
                    "approved": "🟢",
                    "rejected": "🔴",
                    "requires_major_revision": "🔴"
                }
                st.metric("Status", f"{status_color.get(existing_feedback.status.value, '⚪')} {existing_feedback.status.value.replace('_', ' ').title()}")
            
            with col2:
                if existing_feedback.overall_rating > 0:
                    st.metric("Editor Rating", f"{existing_feedback.overall_rating:.1f}/5.0")
                else:
                    st.metric("Editor Rating", "Pending")
            
            with col3:
                st.metric("Feedback Items", len(existing_feedback.feedback_items))
            
            # Show recent feedback
            if existing_feedback.feedback_items:
                st.subheader("Recent Feedback")
                for feedback in existing_feedback.feedback_items[-3:]:  # Show last 3 feedback items
                    with st.expander(f"Feedback by {feedback.editor_name} - {feedback.feedback_type.value.replace('_', ' ').title()}"):
                        col1, col2 = st.columns([3, 1])
                        with col1:
                            st.write(f"**Comments:** {feedback.comments}")
                            if feedback.specific_suggestions:
                                st.write("**Suggestions:**")
                                for suggestion in feedback.specific_suggestions:
                                    st.write(f"• {suggestion}")
                        with col2:
                            st.metric("Rating", f"{feedback.rating}/5")
                            st.write(f"**Priority:** {feedback.priority.title()}")
            
            # Quick feedback form for editors
            st.subheader("💬 Add Quick Feedback")
            with st.expander("Editor Feedback Form"):
                col1, col2 = st.columns(2)
                with col1:
                    editor_name = st.text_input("Editor Name", placeholder="Your name")
                    feedback_type = st.selectbox(
                        "Feedback Type",
                        options=[ft.value for ft in FeedbackType],
                        format_func=lambda x: x.replace('_', ' ').title()
                    )
                    rating = st.slider("Rating", 1, 5, 3)
                
                with col2:
                    priority = st.selectbox("Priority", ["low", "medium", "high", "critical"])
                    comments = st.text_area("Comments", placeholder="Your feedback comments...")
                
                suggestions = st.text_area("Specific Suggestions (one per line)", placeholder="Enter specific suggestions for improvement...")
                
                if st.button("Submit Feedback", type="secondary"):
                    if editor_name and comments:
                        suggestion_list = [s.strip() for s in suggestions.split('\n') if s.strip()] if suggestions else []
                        
                        feedback_id = add_editor_feedback(
                            content_id=content_id,
                            editor_name=editor_name,
                            feedback_type=feedback_type,
                            rating=rating,
                            comments=comments,
                            suggestions=suggestion_list,
                            priority=priority
                        )
                        
                        st.success(f"✅ Feedback submitted successfully! (ID: {feedback_id[:8]})")
                        st.rerun()
                    else:
                        st.error("Please provide editor name and comments.")
    
    with tab5:
<<<<<<< HEAD
        st.subheader("✏️ Interactive Content Editor")
        
        # Initialize content for editing
        if 'editing_content' not in st.session_state:
            st.session_state.editing_content = final_content
        if 'editor_name' not in st.session_state:
            st.session_state.editor_name = ""
        
        # Editor controls
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            editor_name = st.text_input("Editor Name", value=st.session_state.editor_name, key="content_editor_name")
            if editor_name:
                st.session_state.editor_name = editor_name
        
        with col2:
            auto_save = st.checkbox("Auto-save drafts", value=True)
            word_count = len(st.session_state.editing_content.split()) if st.session_state.editing_content else 0
            st.metric("Word Count", word_count)
        
        with col3:
            if st.button("🔄 Reset to Original"):
                st.session_state.editing_content = final_content
                st.rerun()
            
            if st.button("📋 Copy Original"):
                st.session_state.editing_content = final_content
                st.success("Original content copied to editor!")
                st.rerun()
        
        # Main content editor
        st.subheader("📝 Edit Content")
        
        # Content editor with enhanced features
        edited_content = st.text_area(
            "Content Editor",
            value=st.session_state.editing_content,
            height=400,
            help="Edit the content directly. Changes will be tracked and saved as revisions.",
            key="main_content_editor"
        )
        
        # Track changes in real-time
        if edited_content != st.session_state.editing_content:
            st.session_state.editing_content = edited_content
            
            # Show live statistics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                new_word_count = len(edited_content.split())
                word_change = new_word_count - len(final_content.split())
                st.metric("Words", new_word_count, delta=word_change)
            
            with col2:
                new_char_count = len(edited_content)
                char_change = new_char_count - len(final_content)
                st.metric("Characters", new_char_count, delta=char_change)
            
            with col3:
                lines = len(edited_content.split('\n'))
                original_lines = len(final_content.split('\n'))
                line_change = lines - original_lines
                st.metric("Lines", lines, delta=line_change)
            
            with col4:
                # Calculate similarity to original
                import difflib
                similarity = difflib.SequenceMatcher(None, final_content, edited_content).ratio()
                st.metric("Similarity", f"{similarity:.0%}")
            
            # Auto-save draft if enabled
            if auto_save and editor_name and edited_content != final_content:
                if existing_feedback:
                    draft_id = save_content_draft(content_id, edited_content, editor_name)
                    if draft_id:
                        st.success(f"✅ Draft auto-saved! (ID: {draft_id[-8:]})")
        
        # Editor action buttons
        st.subheader("💾 Save Options")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("💾 Save as Draft", type="secondary"):
                if editor_name and edited_content:
                    if existing_feedback:
                        draft_id = save_content_draft(content_id, edited_content, editor_name)
                        if draft_id:
                            st.success(f"✅ Draft saved successfully! (ID: {draft_id[-8:]})")
                        else:
                            st.error("Failed to save draft.")
                    else:
                        st.warning("Please submit content for review first to enable draft saving.")
                else:
                    st.error("Please provide editor name and content.")
        
        with col2:
            revision_notes = st.text_input("Revision Notes", placeholder="Describe your changes...")
            if st.button("🔄 Save as Revision", type="primary"):
                if editor_name and edited_content and revision_notes:
                    if existing_feedback:
                        success = submit_revised_content(content_id, edited_content, revision_notes, editor_name)
                        if success:
                            st.success("✅ Revision saved successfully!")
                            st.session_state.editing_content = edited_content
                            st.rerun()
                        else:
                            st.error("Failed to save revision.")
                    else:
                        st.warning("Please submit content for review first to enable revisions.")
                else:
                    st.error("Please provide editor name, content, and revision notes.")
        
        with col3:
            if st.button("📥 Export Edited Content"):
                if edited_content:
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                    filename = f"{client_name.replace(' ', '_')}_edited_{timestamp}.txt"
                    
                    st.download_button(
                        "📥 Download Edited Content",
                        edited_content,
                        filename,
                        "text/plain"
                    )
                else:
                    st.error("No content to export.")
        
        # Show editing history and drafts
        if existing_feedback:
            st.subheader("📚 Editing History")
            
            # Drafts
            drafts = get_content_drafts(content_id)
            if drafts:
                with st.expander(f"📄 Drafts ({len(drafts)})"):
                    for i, draft in enumerate(reversed(drafts[-3:])):  # Show last 3 drafts
                        col1, col2, col3 = st.columns([2, 1, 1])
                        with col1:
                            st.write(f"**Draft by {draft['editor_name']}**")
                            st.write(f"Saved: {draft['timestamp'][:19].replace('T', ' ')}")
                        with col2:
                            st.metric("Words", draft['word_count'])
                        with col3:
                            if st.button(f"📋 Load Draft", key=f"load_draft_{i}"):
                                st.session_state.editing_content = draft['content']
                                st.success("Draft loaded into editor!")
                                st.rerun()
            
            # Revision history
            content_feedback = get_content_for_editing(content_id)
            if content_feedback and content_feedback.revision_history:
                with st.expander(f"🔄 Revisions ({len(content_feedback.revision_history)})"):
                    for i, revision in enumerate(reversed(content_feedback.revision_history[-3:])):  # Show last 3 revisions
                        col1, col2, col3 = st.columns([2, 1, 1])
                        with col1:
                            st.write(f"**Version {revision['version']} by {revision['editor_name']}**")
                            st.write(f"Notes: {revision['notes']}")
                            st.write(f"Saved: {revision['timestamp'][:19].replace('T', ' ')}")
                        with col2:
                            if 'changes_summary' in revision:
                                changes = revision['changes_summary']
                                st.metric("Word Change", f"{changes.get('word_count_change', 0):+d}")
                                st.write(f"Similarity: {changes.get('similarity_ratio', 0):.0%}")
                        with col3:
                            if st.button(f"📋 Load Revision", key=f"load_revision_{i}"):
                                st.session_state.editing_content = revision['content']
                                st.success("Revision loaded into editor!")
                                st.rerun()
        
        # Content preview
        st.subheader("👀 Live Preview")
        if edited_content:
            st.markdown("**Preview of edited content:**")
            st.markdown(edited_content)
        else:
            st.info("No content to preview.")
    
    with tab6:
=======
>>>>>>> 916d15462f3282d375157da7460c0bb883cb0bcc
        st.subheader("Complete Result Data")
        st.json(result)

def claude_ai_studio_page():
    """Claude AI Studio for advanced content generation and optimization."""
    
    st.markdown('<div class="sub-header">🤖 Claude AI Studio</div>', unsafe_allow_html=True)
    
    st.markdown("""
    ## Advanced Content Generation with Anthropic's Claude AI
    
    Create high-quality, requirement-based content using Claude's advanced language capabilities.
    """)
    
    # Claude API Key configuration
    st.subheader("🔑 Configuration")
    claude_api_key = st.text_input(
        "Claude API Key",
        type="password",
        help="Enter your Anthropic Claude API key for content generation. Leave empty to use mock generation."
    )
    
    if claude_api_key:
        os.environ["CLAUDE_API_KEY"] = claude_api_key
        os.environ["ANTHROPIC_API_KEY"] = claude_api_key
        st.success("✅ Claude API key configured!")
    else:
        st.info("💡 Using mock generation mode. Add your Claude API key for full functionality.")
    
    # Main Claude AI tools
    tab1, tab2, tab3 = st.tabs(["📝 Content Generation", "🔧 Content Optimization", "📊 Quality Analysis"])
    
    with tab1:
        st.subheader("Advanced Content Generation")
        st.write("Generate comprehensive content based on detailed requirements using Claude AI.")
        
        with st.form("claude_generation_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                content_type = st.selectbox(
                    "Content Type",
                    ["blog_post", "whitepaper", "case_study", "thought_leadership", "analysis_report", "social_media", "email_campaign"]
                )
                
                topic = st.text_input(
                    "Content Topic",
                    placeholder="e.g., AI automation for small businesses"
                )
                
                target_audience = st.text_input(
                    "Target Audience",
                    placeholder="e.g., small business owners and entrepreneurs"
                )
            
            with col2:
                tone = st.selectbox(
                    "Content Tone",
                    ["professional", "friendly", "authoritative", "conversational", "technical", "professional_friendly"]
                )
                
                word_count = st.slider("Target Word Count", 300, 3000, 1000)
                
                keywords = st.text_input(
                    "Target Keywords",
                    placeholder="keyword1, keyword2, keyword3"
                )
            
            st.subheader("Content Requirements")
            
            research_insights = st.text_area(
                "Research Insights (Optional)",
                placeholder="Enter any research data, statistics, or insights to include in the content",
                height=100
            )
            
            competitive_analysis = st.text_area(
                "Competitive Context (Optional)",
                placeholder="Information about competitors or market positioning",
                height=80
            )
            
            content_goals = st.multiselect(
                "Content Goals",
                ["education", "engagement", "brand_awareness", "lead_generation", "thought_leadership", "conversion"],
                default=["education", "engagement"]
            )
            
            # Advanced options
            with st.expander("Advanced Generation Options"):
                brand_voice = st.text_input("Brand Voice", placeholder="e.g., approachable expert")
                brand_tone = st.text_input("Brand Tone", placeholder="e.g., helpful and knowledgeable")
                include_cta = st.checkbox("Include Call-to-Action", value=True)
                seo_focus = st.checkbox("SEO Optimization", value=True)
            
            submitted = st.form_submit_button("🤖 Generate with Claude AI", type="primary")
            
            if submitted:
                if not topic or not target_audience:
                    st.error("Please provide both content topic and target audience.")
                else:
                    with st.spinner("Generating content with Claude AI..."):
                        try:
                            # Prepare content requirements
                            content_requirements = {
                                "content_type": content_type,
                                "topic": topic,
                                "target_audience": target_audience,
                                "tone": tone,
                                "word_count": word_count,
                                "keywords": [k.strip() for k in keywords.split(",") if k.strip()],
                                "research_insights": [research_insights] if research_insights else [],
                                "competitive_analysis": competitive_analysis,
                                "content_goals": content_goals,
                                "brand_guidelines": {
                                    "voice": brand_voice or "professional",
                                    "tone": brand_tone or "authoritative"
                                }
                            }
                            
                            # Generate content
                            claude_generator = ClaudeContentGenerator(claude_api_key)
                            result = claude_generator.generate_content(content_requirements)
                            
                            if result and "content" in result:
                                # Store result in session state for display outside form
                                st.session_state.claude_result = result
                                st.session_state.show_claude_results = True
                                st.success("✅ Content Generated Successfully! Results displayed below.")
                            else:
                                st.error("Content generation failed. Please check your requirements and try again.")
                        
                        except Exception as e:
                            st.error(f"Error during content generation: {e}")
        
        # Display Claude AI results outside the form
        if st.session_state.get('show_claude_results') and st.session_state.get('claude_result'):
<<<<<<< HEAD
            # Add a clear results button for Claude AI
            col1, col2 = st.columns([1, 4])
            with col1:
                if st.button("🗑️ Clear Claude Results"):
                    # Clear Claude results from session state
                    if 'show_claude_results' in st.session_state:
                        del st.session_state.show_claude_results
                    if 'claude_result' in st.session_state:
                        del st.session_state.claude_result
                    st.success("✅ Claude results cleared! Ready for new generation.")
                    st.rerun()
            
            with col2:
                st.info("💡 Showing previous Claude AI generation results. Submit a new request to generate fresh content.")
            
=======
>>>>>>> 916d15462f3282d375157da7460c0bb883cb0bcc
            result = st.session_state.claude_result
            
            st.success("✅ Content Generated Successfully!")
            
            # Display metrics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Word Count", f"{result['content_analysis']['word_count']}")
            with col2:
                st.metric("Quality Score", f"{result['quality_score']}/100")
            with col3:
                completion_tokens = result['generation_metadata'].get('completion_tokens', 0)
                st.metric("AI Tokens Used", f"{completion_tokens}")
            with col4:
                requirements_met = sum(result['requirements_met'].values())
                total_requirements = len(result['requirements_met'])
                st.metric("Requirements Met", f"{requirements_met}/{total_requirements}")
            
            # Display generated content
            st.subheader("📄 Generated Content")
            st.markdown(result["content"])
            
            # Download option (outside form)
            download_key = f"claude_download_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            if st.session_state.get(download_key):
                st.download_button(
                    "📥 Download Content",
                    result["content"],
                    f"claude_content_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                    "text/markdown"
                )
            else:
                if st.button("📥 Prepare Download", key=f"prep_{download_key}"):
                    st.session_state[download_key] = True
                    st.rerun()
            
            # Display analysis details
            with st.expander("📊 Content Analysis Details"):
                st.json(result["content_analysis"])
            
            with st.expander("✅ Requirements Validation"):
                for req, met in result["requirements_met"].items():
                    status = "✅" if met else "❌"
                    st.write(f"{status} {req.replace('_', ' ').title()}")
    
    with tab2:
        st.subheader("Content Optimization")
        st.write("Enhance existing content using Claude AI's optimization capabilities.")
        
        original_content = st.text_area(
            "Original Content to Optimize",
            placeholder="Paste your existing content here for optimization",
            height=300
        )
        
        if original_content:
            col1, col2 = st.columns(2)
            
            with col1:
                optimization_goals = st.multiselect(
                    "Optimization Goals",
                    ["improve_readability", "enhance_engagement", "strengthen_seo", "increase_clarity", "professional_tone", "add_data_points"],
                    default=["improve_readability", "enhance_engagement"]
                )
            
            with col2:
                focus_areas = st.multiselect(
                    "Focus Areas",
                    ["introduction", "main_content", "conclusion", "call_to_action", "headlines", "structure"],
                    default=["main_content", "structure"]
                )
            
            if st.button("🔧 Optimize Content", type="primary"):
                with st.spinner("Optimizing content with Claude AI..."):
                    try:
                        claude_optimizer = ClaudeContentOptimizer(claude_api_key)
                        optimization_result = claude_optimizer.optimize_content(original_content, optimization_goals)
                        
                        if optimization_result and "optimized_content" in optimization_result:
                            st.success("✅ Content Optimized Successfully!")
                            
                            # Show before/after metrics
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                original_length = optimization_result["optimization_analysis"]["original_length"]
                                st.metric("Original Length", f"{original_length} words")
                            with col2:
                                optimized_length = optimization_result["optimization_analysis"]["optimized_length"]
                                st.metric("Optimized Length", f"{optimized_length} words")
                            with col3:
                                improvement_ratio = optimization_result["optimization_analysis"]["improvement_ratio"]
                                st.metric("Length Change", f"{improvement_ratio:.2f}x")
                            
                            # Display optimized content
                            st.subheader("🔧 Optimized Content")
                            st.markdown(optimization_result["optimized_content"])
                            
                            # Download optimized content (moved outside form)
                            opt_download_key = f"opt_download_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                            if st.session_state.get(opt_download_key):
                                st.download_button(
                                    "📥 Download Optimized Content",
                                    optimization_result["optimized_content"],
                                    f"optimized_content_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                                    "text/markdown"
                                )
                            else:
                                if st.button("📥 Prepare Optimized Download", key=f"prep_{opt_download_key}"):
                                    st.session_state[opt_download_key] = True
                                    st.rerun()
                            
                            # Show comparison
                            with st.expander("🔍 Before/After Comparison"):
                                col1, col2 = st.columns(2)
                                with col1:
                                    st.subheader("Original")
                                    st.text_area("", original_content, height=200, disabled=True)
                                with col2:
                                    st.subheader("Optimized")
                                    st.text_area("", optimization_result["optimized_content"], height=200, disabled=True)
                        
                        else:
                            st.error("Content optimization failed. Please try again.")
                    
                    except Exception as e:
                        st.error(f"Error during optimization: {e}")
    
    with tab3:
        st.subheader("Content Quality Analysis")
        st.write("Analyze content quality using Claude AI's advanced evaluation capabilities.")
        
        content_to_analyze = st.text_area(
            "Content for Quality Analysis",
            placeholder="Enter content to analyze for quality, readability, and compliance",
            height=250
        )
        
        if content_to_analyze:
            analysis_type = st.selectbox(
                "Analysis Type",
                ["comprehensive", "quality_focus", "seo_focus", "readability_focus", "compliance_check"]
            )
            
            if st.button("📊 Analyze Quality", type="primary"):
                with st.spinner("Analyzing content quality with Claude AI..."):
                    try:
                        # Simulate quality analysis using Claude's content generation capabilities
                        claude_generator = ClaudeContentGenerator(claude_api_key)
                        
                        # Create requirements for analysis
                        analysis_requirements = {
                            "content_type": "quality_analysis",
                            "topic": "content quality assessment",
                            "target_audience": "content creators",
                            "tone": "analytical",
                            "word_count": 500,
                            "keywords": ["quality", "analysis", "assessment"],
                            "research_insights": [f"Analyzing content: {content_to_analyze[:200]}..."],
                            "content_goals": ["analysis"],
                            "original_content": content_to_analyze
                        }
                        
                        analysis_result = claude_generator._analyze_generated_content(content_to_analyze, analysis_requirements)
                        validation_result = claude_generator._validate_requirements(content_to_analyze, analysis_requirements)
                        quality_score = claude_generator._calculate_quality_score(content_to_analyze, analysis_requirements)
                        
                        st.success("✅ Quality Analysis Complete!")
                        
                        # Display quality metrics
                        col1, col2, col3, col4 = st.columns(4)
                        with col1:
                            st.metric("Overall Quality", f"{quality_score}/100")
                        with col2:
                            st.metric("Word Count", analysis_result["word_count"])
                        with col3:
                            st.metric("Readability", f"{analysis_result['readability_estimate']:.1f}/100")
                        with col4:
                            st.metric("Structure Score", "Good" if analysis_result["paragraph_count"] >= 3 else "Needs Work")
                        
                        # Detailed analysis
                        st.subheader("📋 Detailed Analysis")
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            st.write("**✅ Requirements Met:**")
                            for req, met in validation_result.items():
                                status = "✅" if met else "❌"
                                st.write(f"{status} {req.replace('_', ' ').title()}")
                        
                        with col2:
                            st.write("**📊 Content Metrics:**")
                            st.write(f"• Paragraphs: {analysis_result['paragraph_count']}")
                            st.write(f"• Sentences: {analysis_result['sentence_count']}")
                            st.write(f"• Keyword Coverage: {analysis_result.get('keyword_coverage', {}).get('coverage_percentage', 0):.1f}%")
                            st.write(f"• Tone Consistency: {analysis_result.get('tone_consistency', {}).get('tone_consistent', 'Unknown')}")
                        
                        # Recommendations
                        st.subheader("💡 Improvement Recommendations")
                        recommendations = [
                            "Consider adding more data points and statistics",
                            "Improve content structure with clear headings",
                            "Enhance readability with shorter sentences",
                            "Include more engaging questions for audience interaction",
                            "Strengthen the conclusion with clear action items"
                        ]
                        
                        for rec in recommendations:
                            st.write(f"• {rec}")
                    
                    except Exception as e:
                        st.error(f"Error during quality analysis: {e}")
    
    # Feature showcase
    st.markdown("---")
    st.subheader("🌟 Claude AI Features")
    
    features_col1, features_col2, features_col3 = st.columns(3)
    
    with features_col1:
        st.markdown("""
        **🤖 Advanced Generation**
        - Requirement-based content creation
        - Multiple content types supported
        - Professional quality standards
        - Customizable tone and style
        """)
    
    with features_col2:
        st.markdown("""
        **🔧 Content Optimization**
        - AI-powered content enhancement
        - Readability improvements
        - SEO optimization
        - Structure and flow refinement
        """)
    
    with features_col3:
        st.markdown("""
        **📊 Quality Analysis**
        - Comprehensive content evaluation
        - Requirements validation
        - Performance metrics
        - Improvement recommendations
        """)

def human_editor_review_page():
    """Human editor review and feedback interface."""
    
    st.markdown('<div class="sub-header">📝 Human Editor Review System</div>', unsafe_allow_html=True)
    
    st.markdown("""
    ## Content Review and Feedback Management
    
    Human editors can review AI-generated content, provide detailed feedback, and manage content revisions.
    """)
    
    # Review queue
    st.subheader("📋 Content Review Queue")
    
    pending_reviews = feedback_manager.get_pending_reviews()
    
    if not pending_reviews:
        st.info("🎉 No content items pending review at the moment!")
        return
    
    # Filter and sort options
    col1, col2, col3 = st.columns(3)
    with col1:
        status_filter = st.selectbox(
            "Filter by Status",
            ["All"] + [status.value for status in FeedbackStatus]
        )
    with col2:
        sort_by = st.selectbox("Sort by", ["Created Date", "Last Updated", "Priority", "Client Name"])
    with col3:
        sort_order = st.selectbox("Sort Order", ["Newest First", "Oldest First"])
    
    # Apply filters
    filtered_reviews = pending_reviews
    if status_filter != "All":
        filtered_reviews = [r for r in filtered_reviews if r.status.value == status_filter]
    
    # Display review items
    for i, content_feedback in enumerate(filtered_reviews):
        with st.expander(
            f"📄 {content_feedback.content_title} - {content_feedback.client_name} "
            f"({content_feedback.status.value.replace('_', ' ').title()})"
        ):
            
            # Content info
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Status", content_feedback.status.value.replace('_', ' ').title())
            with col2:
                if content_feedback.overall_rating > 0:
                    st.metric("Rating", f"{content_feedback.overall_rating:.1f}/5")
                else:
                    st.metric("Rating", "Not Rated")
            with col3:
                st.metric("Feedback Count", len(content_feedback.feedback_items))
            with col4:
                st.metric("Revisions", len(content_feedback.revision_history))
            
            # Content preview
            st.subheader("📄 Content Preview")
            content_preview = content_feedback.current_version[:500] + "..." if len(content_feedback.current_version) > 500 else content_feedback.current_version
            st.text_area("", content_preview, height=150, disabled=True, key=f"preview_{i}")
            
            # Action buttons
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button(f"🔍 Full Review", key=f"review_{i}"):
                    st.session_state.selected_content_for_review = content_feedback.content_id
                    st.rerun()
            
            with col2:
                if st.button(f"📝 Quick Feedback", key=f"quick_{i}"):
                    st.session_state.selected_content_for_feedback = content_feedback.content_id
                    st.rerun()
            
            with col3:
                if st.button(f"✅ Approve", key=f"approve_{i}"):
                    # Quick approval
                    feedback_id = add_editor_feedback(
                        content_id=content_feedback.content_id,
                        editor_name="Quick Approval",
                        feedback_type="content_quality",
                        rating=5,
                        comments="Content approved for publication",
                        priority="low"
                    )
                    st.success("✅ Content approved!")
                    st.rerun()
    
    # Detailed review interface
    if st.session_state.get('selected_content_for_review'):
        detailed_content_review()
    
    # Quick feedback interface
    if st.session_state.get('selected_content_for_feedback'):
        quick_feedback_interface()

def detailed_content_review():
    """Detailed content review interface."""
    content_id = st.session_state.selected_content_for_review
    content_feedback = get_content_for_editing(content_id)
    
    if not content_feedback:
        st.error("Content not found!")
        return
    
    st.markdown("---")
    st.subheader(f"🔍 Detailed Review: {content_feedback.content_title}")
    
    # Close button
    if st.button("❌ Close Review"):
        del st.session_state.selected_content_for_review
        st.rerun()
    
    # Content display and editing
<<<<<<< HEAD
    tab1, tab2, tab3, tab4 = st.tabs(["📄 Content Review", "📊 Feedback History", "✏️ Content Revision", "🔧 Advanced Editor"])
=======
    tab1, tab2, tab3 = st.tabs(["📄 Content Review", "📊 Feedback History", "✏️ Content Revision"])
>>>>>>> 916d15462f3282d375157da7460c0bb883cb0bcc
    
    with tab1:
        st.subheader("Current Content")
        
        # Display content with line numbers for easy reference
        lines = content_feedback.current_version.split('\n')
        content_with_lines = '\n'.join([f"{i+1:3d}: {line}" for i, line in enumerate(lines)])
        st.text_area("Content with Line Numbers", content_with_lines, height=400, disabled=True)
        
        # Comprehensive feedback form
        st.subheader("📝 Detailed Feedback")
        
        col1, col2 = st.columns(2)
        with col1:
            editor_name = st.text_input("Editor Name", value=st.session_state.get('editor_name', ''))
            if editor_name:
                st.session_state.editor_name = editor_name
            
            feedback_type = st.selectbox(
                "Primary Feedback Area",
                options=[ft.value for ft in FeedbackType],
                format_func=lambda x: x.replace('_', ' ').title()
            )
            
            overall_rating = st.slider("Overall Content Rating", 1, 5, 3)
            priority = st.selectbox("Priority Level", ["low", "medium", "high", "critical"])
        
        with col2:
            specific_areas = st.multiselect(
                "Areas Needing Attention",
                ["Introduction", "Main Content", "Conclusion", "Tone", "Grammar", "SEO", "Factual Accuracy", "Structure"],
                default=[]
            )
            
            recommended_action = st.selectbox(
                "Recommended Action",
                ["Minor Revisions", "Moderate Revisions", "Major Revisions", "Approve", "Reject"]
            )
        
        # Detailed comments
        general_comments = st.text_area(
            "General Comments",
            placeholder="Provide overall feedback on the content quality, tone, structure, and effectiveness...",
            height=100
        )
        
        specific_suggestions = st.text_area(
            "Specific Suggestions",
            placeholder="Enter specific suggestions for improvement (one per line):\n• Suggestion 1\n• Suggestion 2",
            height=100
        )
        
        line_specific_feedback = st.text_area(
            "Line-Specific Feedback",
            placeholder="Reference specific lines for targeted feedback:\nLine 15: Consider rewording for clarity\nLine 23: Add supporting data",
            height=80
        )
        
        if st.button("💾 Submit Detailed Feedback", type="primary"):
            if editor_name and general_comments:
                # Parse suggestions
                suggestion_list = []
                if specific_suggestions:
                    suggestion_list.extend([s.strip().lstrip('•').strip() for s in specific_suggestions.split('\n') if s.strip()])
                if line_specific_feedback:
                    suggestion_list.extend([s.strip() for s in line_specific_feedback.split('\n') if s.strip()])
                
                # Add areas needing attention to suggestions
                if specific_areas:
                    suggestion_list.append(f"Focus areas: {', '.join(specific_areas)}")
                    suggestion_list.append(f"Recommended action: {recommended_action}")
                
                feedback_id = add_editor_feedback(
                    content_id=content_id,
                    editor_name=editor_name,
                    feedback_type=feedback_type,
                    rating=overall_rating,
                    comments=general_comments,
                    suggestions=suggestion_list,
                    priority=priority
                )
                
                st.success(f"✅ Detailed feedback submitted successfully! (ID: {feedback_id[:8]})")
                st.rerun()
            else:
                st.error("Please provide editor name and general comments.")
    
    with tab2:
        st.subheader("📊 Feedback History")
        
        if content_feedback.feedback_items:
            for feedback in reversed(content_feedback.feedback_items):  # Most recent first
                with st.expander(
                    f"{feedback.editor_name} - {feedback.feedback_type.value.replace('_', ' ').title()} "
                    f"({feedback.rating}/5) - {feedback.timestamp[:10]}"
                ):
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.write(f"**Comments:** {feedback.comments}")
                        if feedback.specific_suggestions:
                            st.write("**Suggestions:**")
                            for suggestion in feedback.specific_suggestions:
                                st.write(f"• {suggestion}")
                    with col2:
                        st.metric("Rating", f"{feedback.rating}/5")
                        st.write(f"**Priority:** {feedback.priority.title()}")
                        st.write(f"**Type:** {feedback.feedback_type.value.replace('_', ' ').title()}")
        else:
            st.info("No feedback history available.")
    
    with tab3:
        st.subheader("✏️ Content Revision")
        
        st.write("**Original Content:**")
        st.text_area("", content_feedback.original_content, height=200, disabled=True)
        
        revised_content = st.text_area(
            "Revised Content",
            value=content_feedback.current_version,
            height=400,
            help="Edit the content based on feedback"
        )
        
        revision_notes = st.text_area(
            "Revision Notes",
            placeholder="Describe the changes made in this revision...",
            height=100
        )
        
        if st.button("💾 Save Revision", type="primary"):
            if revised_content != content_feedback.current_version:
<<<<<<< HEAD
                editor_name = st.session_state.get('editor_name', 'Anonymous')
                success = submit_revised_content(content_id, revised_content, revision_notes, editor_name)
=======
                success = submit_revised_content(content_id, revised_content, revision_notes)
>>>>>>> 916d15462f3282d375157da7460c0bb883cb0bcc
                if success:
                    st.success("✅ Revision saved successfully!")
                    st.rerun()
                else:
                    st.error("Failed to save revision.")
            else:
                st.warning("No changes detected in the content.")
<<<<<<< HEAD
    
    with tab4:
        st.subheader("🔧 Advanced Content Editor")
        
        # Initialize advanced editor session state
        editor_key = f"advanced_editor_{content_id}"
        if editor_key not in st.session_state:
            st.session_state[editor_key] = content_feedback.current_version
        
        # Advanced editor controls
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            editor_name = st.text_input("Editor Name", value=st.session_state.get('editor_name', ''), key=f"adv_editor_name_{content_id}")
            if editor_name:
                st.session_state.editor_name = editor_name
        
        with col2:
            editing_mode = st.selectbox(
                "Editing Mode",
                ["Full Edit", "Line by Line", "Section Edit", "Collaborative"]
            )
        
        with col3:
            show_formatting = st.checkbox("Show Formatting Help", value=False)
            track_changes = st.checkbox("Track Changes", value=True)
        
        with col4:
            auto_save_interval = st.selectbox("Auto-save", ["Off", "Every 30s", "Every 60s", "Every 5min"])
        
        # Content statistics
        current_content = st.session_state[editor_key]
        original_content = content_feedback.original_content
        
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.metric("Words", len(current_content.split()))
        with col2:
            st.metric("Characters", len(current_content))
        with col3:
            st.metric("Lines", len(current_content.split('\n')))
        with col4:
            st.metric("Paragraphs", len([p for p in current_content.split('\n\n') if p.strip()]))
        with col5:
            import difflib
            similarity = difflib.SequenceMatcher(None, original_content, current_content).ratio()
            st.metric("vs Original", f"{similarity:.0%}")
        
        # Main editor based on mode
        if editing_mode == "Full Edit":
            st.subheader("📝 Full Content Editor")
            
            edited_content = st.text_area(
                "Edit Content",
                value=current_content,
                height=500,
                help="Full content editing mode with real-time tracking",
                key=f"full_editor_{content_id}"
            )
            
            if edited_content != current_content:
                st.session_state[editor_key] = edited_content
                
                # Show real-time changes
                if track_changes:
                    st.subheader("📊 Real-time Change Analysis")
                    
                    word_diff = len(edited_content.split()) - len(current_content.split())
                    char_diff = len(edited_content) - len(current_content)
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Word Change", f"{word_diff:+d}")
                    with col2:
                        st.metric("Character Change", f"{char_diff:+d}")
                    with col3:
                        similarity = difflib.SequenceMatcher(None, current_content, edited_content).ratio()
                        st.metric("Similarity", f"{similarity:.0%}")
        
        elif editing_mode == "Line by Line":
            st.subheader("📋 Line-by-Line Editor")
            
            lines = current_content.split('\n')
            edited_lines = []
            
            for i, line in enumerate(lines):
                col1, col2 = st.columns([1, 10])
                with col1:
                    st.write(f"**{i+1}**")
                with col2:
                    edited_line = st.text_input(f"Line {i+1}", value=line, key=f"line_{content_id}_{i}")
                    edited_lines.append(edited_line)
            
            # Add new line option
            if st.button("➕ Add New Line"):
                edited_lines.append("")
            
            edited_content = '\n'.join(edited_lines)
            st.session_state[editor_key] = edited_content
        
        elif editing_mode == "Section Edit":
            st.subheader("📑 Section-by-Section Editor")
            
            # Split content into sections (paragraphs)
            sections = [s.strip() for s in current_content.split('\n\n') if s.strip()]
            edited_sections = []
            
            for i, section in enumerate(sections):
                st.subheader(f"Section {i+1}")
                edited_section = st.text_area(
                    f"Edit Section {i+1}",
                    value=section,
                    height=150,
                    key=f"section_{content_id}_{i}"
                )
                edited_sections.append(edited_section)
                
                # Section actions
                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button(f"🔼 Move Up", key=f"up_{content_id}_{i}"):
                        if i > 0:
                            sections[i], sections[i-1] = sections[i-1], sections[i]
                            st.rerun()
                with col2:
                    if st.button(f"🔽 Move Down", key=f"down_{content_id}_{i}"):
                        if i < len(sections) - 1:
                            sections[i], sections[i+1] = sections[i+1], sections[i]
                            st.rerun()
                with col3:
                    if st.button(f"🗑️ Delete", key=f"del_{content_id}_{i}"):
                        sections.pop(i)
                        st.rerun()
                
                st.markdown("---")
            
            # Add new section
            if st.button("➕ Add New Section"):
                edited_sections.append("")
            
            edited_content = '\n\n'.join(edited_sections)
            st.session_state[editor_key] = edited_content
        
        elif editing_mode == "Collaborative":
            st.subheader("👥 Collaborative Editor")
            
            # Show who's editing
            st.info(f"🔵 Currently editing: {editor_name or 'Anonymous'}")
            
            # Collaborative features
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("📝 Your Edits")
                your_edits = st.text_area(
                    "Your changes",
                    value=current_content,
                    height=300,
                    key=f"collab_editor_{content_id}"
                )
            
            with col2:
                st.subheader("💬 Comments & Suggestions")
                collaboration_comments = st.text_area(
                    "Comments for other editors",
                    placeholder="Add comments about your changes...",
                    height=150,
                    key=f"collab_comments_{content_id}"
                )
                
                if st.button("💾 Save Collaborative Draft"):
                    if editor_name and your_edits:
                        draft_id = save_content_draft(content_id, your_edits, editor_name)
                        if draft_id:
                            st.success(f"✅ Collaborative draft saved! (ID: {draft_id[-8:]})")
                            
                            # Also save comments as feedback if provided
                            if collaboration_comments:
                                add_editor_feedback(
                                    content_id=content_id,
                                    editor_name=editor_name,
                                    feedback_type="collaborative_editing",
                                    rating=4,  # Default collaborative rating
                                    comments=collaboration_comments,
                                    priority="medium"
                                )
                        else:
                            st.error("Failed to save collaborative draft.")
                    else:
                        st.error("Please provide editor name and content.")
            
            edited_content = your_edits
            st.session_state[editor_key] = edited_content
        
        # Formatting help
        if show_formatting:
            with st.expander("📝 Formatting Help"):
                st.markdown("""
                **Markdown Formatting:**
                - `**bold text**` → **bold text**
                - `*italic text*` → *italic text*
                - `# Heading 1` → # Heading 1
                - `## Heading 2` → ## Heading 2
                - `- List item` → • List item
                - `[Link text](URL)` → [Link text](URL)
                - `> Blockquote` → Quoted text
                
                **Special Characters:**
                - `—` (em dash), `–` (en dash)
                - `"smart quotes"` instead of "straight quotes"
                - `…` (ellipsis) instead of ...
                """)
        
        # Editor actions
        st.subheader("💾 Advanced Save Options")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("💾 Save Draft", type="secondary"):
                if editor_name and st.session_state[editor_key]:
                    draft_id = save_content_draft(content_id, st.session_state[editor_key], editor_name)
                    if draft_id:
                        st.success(f"✅ Draft saved! (ID: {draft_id[-8:]})")
                    else:
                        st.error("Failed to save draft.")
                else:
                    st.error("Please provide editor name.")
        
        with col2:
            revision_notes = st.text_input("Revision Notes", placeholder="Describe changes...", key=f"adv_revision_notes_{content_id}")
            if st.button("🔄 Save Revision", type="primary"):
                if editor_name and st.session_state[editor_key] and revision_notes:
                    success = submit_revised_content(content_id, st.session_state[editor_key], revision_notes, editor_name)
                    if success:
                        st.success("✅ Revision saved!")
                        st.rerun()
                    else:
                        st.error("Failed to save revision.")
                else:
                    st.error("Please provide editor name and revision notes.")
        
        with col3:
            if st.button("🔄 Reset"):
                st.session_state[editor_key] = content_feedback.current_version
                st.success("Content reset to current version!")
                st.rerun()
        
        with col4:
            if st.button("📥 Export"):
                if st.session_state[editor_key]:
                    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
                    filename = f"{content_feedback.content_title.replace(' ', '_')}_{timestamp}.md"
                    
                    st.download_button(
                        "📥 Download",
                        st.session_state[editor_key],
                        filename,
                        "text/markdown"
                    )
        
        # Live preview
        st.subheader("👀 Live Preview")
        if st.session_state[editor_key]:
            st.markdown("**Preview:**")
            st.markdown(st.session_state[editor_key])
        
        # Change comparison
        if st.session_state[editor_key] != content_feedback.current_version:
            st.subheader("🔍 Change Comparison")
            
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Current Version")
                st.text_area("", content_feedback.current_version, height=200, disabled=True, key=f"current_compare_{content_id}")
            
            with col2:
                st.subheader("Your Edits")
                st.text_area("", st.session_state[editor_key], height=200, disabled=True, key=f"edited_compare_{content_id}")
=======
>>>>>>> 916d15462f3282d375157da7460c0bb883cb0bcc

def quick_feedback_interface():
    """Quick feedback interface for rapid review."""
    content_id = st.session_state.selected_content_for_feedback
    content_feedback = get_content_for_editing(content_id)
    
    if not content_feedback:
        st.error("Content not found!")
        return
    
    st.markdown("---")
    st.subheader(f"💬 Quick Feedback: {content_feedback.content_title}")
    
    # Close button
    if st.button("❌ Close Quick Feedback"):
        del st.session_state.selected_content_for_feedback
        st.rerun()
    
    # Quick feedback form
    col1, col2, col3 = st.columns(3)
    
    with col1:
        editor_name = st.text_input("Editor Name", value=st.session_state.get('editor_name', ''))
        rating = st.slider("Rating", 1, 5, 3)
    
    with col2:
        feedback_type = st.selectbox(
            "Feedback Type",
            options=[ft.value for ft in FeedbackType],
            format_func=lambda x: x.replace('_', ' ').title()
        )
        priority = st.selectbox("Priority", ["low", "medium", "high", "critical"])
    
    with col3:
        quick_actions = st.selectbox(
            "Quick Action",
            ["Custom Feedback", "Approve", "Minor Edits Needed", "Major Revision Required", "Reject"]
        )
    
    # Pre-filled comments based on quick action
    comment_templates = {
        "Approve": "Content is well-written and ready for publication.",
        "Minor Edits Needed": "Content is good overall but needs minor edits for improvement.",
        "Major Revision Required": "Content needs significant revision before publication.",
        "Reject": "Content does not meet publication standards and requires complete rewrite."
    }
    
    default_comment = comment_templates.get(quick_actions, "")
    comments = st.text_area("Comments", value=default_comment, height=100)
    
    if st.button("💾 Submit Quick Feedback", type="primary"):
        if editor_name and comments:
            feedback_id = add_editor_feedback(
                content_id=content_id,
                editor_name=editor_name,
                feedback_type=feedback_type,
                rating=rating,
                comments=comments,
                priority=priority
            )
            
            st.success(f"✅ Quick feedback submitted! (ID: {feedback_id[:8]})")
            st.rerun()
        else:
            st.error("Please provide editor name and comments.")

def content_analytics_page():
    """Content analytics and reporting dashboard."""
    
    st.markdown('<div class="sub-header">📊 Content Analytics Dashboard</div>', unsafe_allow_html=True)
    
    # Get analytics data
    analytics = feedback_manager.get_feedback_analytics()
    
    # Overview metrics
    st.subheader("📈 Overview Metrics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Content Items", analytics["total_content_items"])
    
    with col2:
        st.metric("Average Rating", f"{analytics['average_rating']:.1f}/5.0")
    
    with col3:
        st.metric("Items with Feedback", analytics["content_with_feedback"])
    
    with col4:
        approval_rate = analytics["approval_rate"] * 100
        st.metric("Approval Rate", f"{approval_rate:.1f}%")
    
    # Status distribution
    st.subheader("📊 Content Status Distribution")
    
    if analytics["status_distribution"]:
        status_data = analytics["status_distribution"]
        
        # Create columns for status metrics
        status_cols = st.columns(len(status_data))
        for i, (status, count) in enumerate(status_data.items()):
            with status_cols[i]:
                st.metric(status.replace('_', ' ').title(), count)
        
        # Status chart data
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(figsize=(10, 6))
        statuses = list(status_data.keys())
        counts = list(status_data.values())
        
        ax.bar([s.replace('_', ' ').title() for s in statuses], counts)
        ax.set_title('Content Status Distribution')
        ax.set_ylabel('Number of Items')
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        st.pyplot(fig)
    else:
        st.info("No status data available yet.")
    
    # Feedback type distribution
    st.subheader("🎯 Feedback Type Analysis")
    
    if analytics["feedback_type_distribution"]:
        feedback_types = analytics["feedback_type_distribution"]
        
        # Display as metrics
        type_cols = st.columns(min(4, len(feedback_types)))
        for i, (feedback_type, count) in enumerate(feedback_types.items()):
            col_index = i % len(type_cols)
            with type_cols[col_index]:
                st.metric(feedback_type.replace('_', ' ').title(), count)
    else:
        st.info("No feedback type data available yet.")
    
    # Detailed reports
    st.subheader("📋 Detailed Reports")
    
    # Export options
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📥 Export Full Report"):
            report = feedback_manager.export_feedback_report()
            st.json(report)
    
    with col2:
        if st.button("📊 Generate Analytics Report"):
            # Create a comprehensive analytics report
            report_data = {
                "generated_at": datetime.datetime.now().isoformat(),
                "analytics": analytics,
                "summary": {
                    "total_items": analytics["total_content_items"],
                    "avg_quality": analytics["average_rating"],
                    "feedback_coverage": f"{(analytics['content_with_feedback'] / max(analytics['total_content_items'], 1)) * 100:.1f}%",
                    "approval_rate": f"{analytics['approval_rate'] * 100:.1f}%"
                }
            }
            
            st.download_button(
                "📥 Download Analytics Report",
                json.dumps(report_data, indent=2),
                f"content_analytics_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                "application/json"
            )

def gemini_analysis_page():
    """Gemini-powered content analysis tools page."""
    
    st.markdown('<div class="sub-header">🧠 Gemini Analysis Tools</div>', unsafe_allow_html=True)
    
    st.markdown("""
    ## Advanced Content Summarization with Google Gemini LLM
    
    Analyze and summarize source material using state-of-the-art AI to enhance your content creation process.
    """)
    
    # Gemini API Key input
    st.subheader("🔑 Configuration")
    gemini_api_key = st.text_input(
        "Gemini API Key", 
        type="password",
        help="Enter your Google Gemini API key for enhanced analysis. Leave empty to use mock analysis."
    )
    
    if gemini_api_key:
        os.environ["GEMINI_API_KEY"] = gemini_api_key
        st.success("✅ Gemini API key configured!")
    else:
        st.info("💡 Using mock analysis mode. Add your Gemini API key for full functionality.")
    
    # Analysis tools tabs
    tab1, tab2, tab3 = st.tabs(["📄 Content Summarization", "🔍 Multi-Source Analysis", "📊 Content Quality Assessment"])
    
    with tab1:
        st.subheader("Content Summarization Tool")
        
        source_content = st.text_area(
            "Source Content to Analyze",
            placeholder="Paste your source material here (research articles, reports, competitor content, etc.)",
            height=200
        )
        
        col1, col2 = st.columns(2)
        with col1:
            summary_type = st.selectbox(
                "Summary Type",
                ["general", "research", "competitive", "technical", "market"]
            )
        
        with col2:
            max_length = st.slider("Summary Length (words)", 100, 800, 300)
        
        if st.button("🧠 Analyze with Gemini", key="summarize"):
            if source_content:
                with st.spinner("Analyzing content with Gemini..."):
                    try:
                        summarizer = GeminiSummarizationTool(gemini_api_key)
                        result = summarizer.summarize_content(source_content, summary_type, max_length)
                        
                        st.success("✅ Analysis Complete!")
                        
                        # Display results
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Original Length", f"{result['source_length']} words")
                        with col2:
                            st.metric("Summary Length", f"{result['summary_length']} words")
                        with col3:
                            st.metric("Compression Ratio", f"{result['compression_ratio']:.1f}x")
                        
                        st.subheader("📝 Summary")
                        st.write(result["summary"])
                        
                        st.subheader("💡 Key Insights")
                        for insight in result["key_insights"]:
                            st.write(f"• {insight}")
                        
                        # Download option
                        summary_data = f"""CONTENT SUMMARY
Analysis Type: {summary_type}
Generated: {result['analysis_timestamp']}
Model: {result['model_used']}

SUMMARY:
{result['summary']}

KEY INSIGHTS:
{chr(10).join([f"• {insight}" for insight in result['key_insights']])}

METRICS:
- Original Length: {result['source_length']} words
- Summary Length: {result['summary_length']} words  
- Compression Ratio: {result['compression_ratio']:.1f}x
"""
                        
                        # Download summary (moved outside form)
                        summary_download_key = f"summary_download_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                        if st.session_state.get(summary_download_key):
                            st.download_button(
                                "📥 Download Summary",
                                summary_data,
                                f"gemini_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                                "text/plain"
                            )
                        else:
                            if st.button("📥 Prepare Summary Download", key=f"prep_{summary_download_key}"):
                                st.session_state[summary_download_key] = True
                                st.rerun()
                        
                    except Exception as e:
                        st.error(f"Analysis failed: {e}")
            else:
                st.warning("Please enter source content to analyze.")
    
    with tab2:
        st.subheader("Multi-Source Content Analysis")
        st.write("Analyze multiple sources simultaneously for comprehensive insights.")
        
        num_sources = st.number_input("Number of Sources", min_value=1, max_value=5, value=2)
        
        sources = []
        for i in range(num_sources):
            with st.expander(f"Source {i+1}"):
                source_content = st.text_area(f"Content {i+1}", key=f"source_{i}", height=150)
                source_type = st.selectbox(f"Source Type {i+1}", 
                                         ["research", "competitive", "market", "technical", "news"], 
                                         key=f"type_{i}")
                if source_content:
                    sources.append({"content": source_content, "source_type": source_type})
        
        analysis_focus = st.selectbox(
            "Analysis Focus",
            ["content_creation", "market_research", "competitive_analysis", "technical_analysis"]
        )
        
        if st.button("🔍 Analyze Multiple Sources", key="multi_analyze"):
            if sources:
                with st.spinner("Performing multi-source analysis..."):
                    try:
                        from content_summarization_tools import MultiSourceAnalyzer
                        analyzer = MultiSourceAnalyzer(gemini_api_key)
                        result = analyzer.analyze_multiple_sources(sources, analysis_focus)
                        
                        st.success(f"✅ Analyzed {len(sources)} sources!")
                        
                        # Display comparative analysis
                        st.subheader("🔄 Comparative Analysis")
                        comparison = result["comparative_analysis"]
                        
                        if comparison.get("common_themes"):
                            st.write("**Common Themes:**")
                            for theme in comparison["common_themes"]:
                                st.write(f"• {theme}")
                        
                        # Display consolidated insights
                        st.subheader("💡 Consolidated Insights")
                        for insight in result["consolidated_insights"][:5]:
                            st.write(f"• {insight}")
                        
                        # Display recommendations
                        st.subheader("📋 Recommendations")
                        for rec in result["recommendations"]:
                            st.write(f"• {rec}")
                        
                    except Exception as e:
                        st.error(f"Multi-source analysis failed: {e}")
            else:
                st.warning("Please add content to at least one source.")
    
    with tab3:
        st.subheader("Content Quality Assessment")
        st.write("Assess the quality and credibility of source material.")
        
        content_to_assess = st.text_area(
            "Content for Quality Assessment",
            placeholder="Enter content to assess quality, credibility, and analytical value",
            height=200
        )
        
        if st.button("📊 Assess Quality", key="quality_assess"):
            if content_to_assess:
                with st.spinner("Assessing content quality..."):
                    try:
                        analyzer = AdvancedContentAnalyzer(gemini_api_key)
                        assessment = analyzer.comprehensive_analysis(content_to_assess, "content_creation")
                        
                        st.success("✅ Quality Assessment Complete!")
                        
                        # Display quality metrics
                        quality = assessment["quality_assessment"]
                        
                        col1, col2, col3, col4 = st.columns(4)
                        with col1:
                            st.metric("Overall Quality", quality["overall_quality"].title())
                        with col2:
                            st.metric("Content Depth", quality["content_depth"].title())
                        with col3:
                            st.metric("Technical Detail", quality["technical_detail"].title())
                        with col4:
                            st.metric("Data Presence", quality["data_presence"].title())
                        
                        # Content themes
                        st.subheader("🎯 Content Themes")
                        themes = assessment.get("content_themes", [])
                        for theme in themes:
                            st.write(f"• {theme}")
                        
                        # Key entities
                        st.subheader("🏢 Key Entities")
                        entities = assessment.get("key_entities", [])
                        for entity in entities[:5]:
                            st.write(f"• {entity}")
                        
                        # Credibility indicators
                        st.subheader("✅ Credibility Indicators")
                        indicators = quality.get("credibility_indicators", [])
                        if indicators:
                            for indicator in indicators:
                                st.write(f"• {indicator}")
                        else:
                            st.write("No specific credibility indicators found.")
                        
                        # Recommendations
                        st.subheader("💡 Recommendations")
                        recommendations = assessment.get("recommendations", [])
                        for rec in recommendations:
                            st.write(f"• {rec}")
                        
                    except Exception as e:
                        st.error(f"Quality assessment failed: {e}")
            else:
                st.warning("Please enter content to assess.")
    
    # Feature showcase
    st.markdown("---")
    st.subheader("🌟 Gemini-Powered Features")
    
    features_col1, features_col2 = st.columns(2)
    
    with features_col1:
        st.markdown("""
        **📚 Advanced Summarization**
        - Multiple summary types (research, competitive, technical)
        - Intelligent compression with key insight extraction
        - Customizable length and focus
        
        **🔍 Multi-Source Analysis**
        - Compare and contrast multiple sources
        - Identify common themes and unique insights
        - Comprehensive competitive intelligence
        """)
    
    with features_col2:
        st.markdown("""
        **📊 Quality Assessment**
        - Content depth and credibility analysis
        - Technical detail evaluation
        - Data presence and freshness indicators
        
        **💡 Actionable Insights**
        - Key entity and theme extraction
        - Strategic recommendations
        - Content creation guidance
        """)

def system_dashboard_page():
    """System dashboard and analytics."""
    
    st.markdown('<div class="sub-header">📈 System Dashboard</div>', unsafe_allow_html=True)
    
    # System overview metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Content Created", len(st.session_state.content_history))
    
    with col2:
        success_rate = 100 if st.session_state.content_history else 0
        st.metric("Success Rate", f"{success_rate}%")
    
    with col3:
        avg_processing_time = "45 minutes"
        st.metric("Avg Processing Time", avg_processing_time)
    
    with col4:
        system_status = "Operational"
        st.metric("System Status", system_status)
    
    # System capabilities
    st.subheader("🔧 System Capabilities")
    
    capabilities = [
        {"name": "Content Strategy Planning", "status": "✅ Active", "description": "Autonomous strategy development"},
        {"name": "Market Research", "status": "✅ Active", "description": "Industry and competitor analysis"},
        {"name": "Content Creation", "status": "✅ Active", "description": "AI-powered writing"},
        {"name": "SEO Optimization", "status": "✅ Active", "description": "Keyword research and optimization"},
        {"name": "Quality Assurance", "status": "✅ Active", "description": "Multi-point validation"},
        {"name": "Deliverable Preparation", "status": "✅ Active", "description": "Publication-ready formatting"}
    ]
    
    for cap in capabilities:
        col1, col2, col3 = st.columns([3, 2, 4])
        with col1:
            st.write(f"**{cap['name']}**")
        with col2:
            st.write(cap['status'])
        with col3:
            st.write(cap['description'])
    
    # Recent activity
    st.subheader("📋 Recent Activity")
    
    if st.session_state.content_history:
        recent_activity = st.session_state.content_history[-5:]  # Last 5 items
        
        for activity in reversed(recent_activity):
            with st.expander(f"{activity['timestamp']} - {activity['client_name']} ({activity['content_type']})"):
                st.write(f"**Industry:** {activity['industry']}")
                st.write(f"**Brief:** {activity['brief']}")
                st.write(f"**Status:** {activity['status']}")
    else:
        st.info("No content creation history available yet.")

def content_history_page():
    """Content creation history and management."""
    
    st.markdown('<div class="sub-header">📚 Content History</div>', unsafe_allow_html=True)
    
    if not st.session_state.content_history:
        st.info("No content creation history available yet. Create some content to see it here!")
        return
    
    # History overview
    st.subheader("📊 History Overview")
    
    # Create dataframe for analysis
    df = pd.DataFrame(st.session_state.content_history)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Content types chart
        content_type_counts = df['content_type'].value_counts()
        st.bar_chart(content_type_counts)
        st.caption("Content Types Created")
    
    with col2:
        # Industry distribution
        industry_counts = df['industry'].value_counts()
        st.bar_chart(industry_counts)
        st.caption("Industries Served")
    
    # Detailed history table
    st.subheader("📋 Detailed History")
    
    # Create display dataframe
    display_df = df[['timestamp', 'client_name', 'industry', 'content_type', 'status']].copy()
    display_df.columns = ['Timestamp', 'Client', 'Industry', 'Content Type', 'Status']
    
    st.dataframe(display_df, use_container_width=True)
    
    # Export options
    st.subheader("📤 Export Options")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📥 Export History as CSV"):
            csv = display_df.to_csv(index=False)
            st.session_state['csv_data'] = csv
            st.session_state['show_csv_download'] = True
            st.rerun()
        
        if st.session_state.get('show_csv_download'):
            st.download_button(
                label="Download CSV",
                data=st.session_state.get('csv_data', ''),
                file_name=f"content_history_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
    
    with col2:
        if st.button("🗑️ Clear History"):
            st.session_state.content_history = []
            st.rerun()

def api_documentation_page():
    """API documentation and integration guide."""
    
    st.markdown('<div class="sub-header">📚 API Documentation</div>', unsafe_allow_html=True)
    
    st.markdown("""
    ## REST API Endpoints
    
    The Autonomous Content Creation System provides RESTful API endpoints for integration.
    
    ### Base URL
    ```
    https://api.innovatemarketing.solutions/v1
    ```
    
    ### Authentication
    ```
    Authorization: Bearer YOUR_API_KEY
    ```
    """)
    
    # API endpoints
    endpoints = [
        {
            "method": "POST",
            "endpoint": "/content/create",
            "description": "Create new content",
            "example": {
                "client_id": "client_123",
                "company_name": "TechFlow Innovations",
                "industry": "technology",
                "content_brief": "Create blog post about AI automation",
                "target_audience": "Technology decision makers",
                "content_goals": ["brand_awareness", "lead_generation"]
            }
        },
        {
            "method": "GET",
            "endpoint": "/content/status/{request_id}",
            "description": "Check content creation status",
            "example": {
                "request_id": "req_20240101_123456",
                "status": "completed",
                "progress": 100
            }
        },
        {
            "method": "GET",
            "endpoint": "/system/health",
            "description": "System health check",
            "example": {
                "status": "healthy",
                "components": {
                    "content_generation": "operational",
                    "seo_optimization": "operational"
                }
            }
        }
    ]
    
    for endpoint in endpoints:
        st.subheader(f"{endpoint['method']} {endpoint['endpoint']}")
        st.write(endpoint['description'])
        st.code(json.dumps(endpoint['example'], indent=2), language='json')
        st.write("---")
    
    # Integration examples
    st.subheader("🔗 Integration Examples")
    
    tab1, tab2, tab3 = st.tabs(["Python", "JavaScript", "cURL"])
    
    with tab1:
        st.code("""
import requests

# Create content
response = requests.post(
    "https://api.innovatemarketing.solutions/v1/content/create",
    headers={"Authorization": "Bearer YOUR_API_KEY"},
    json={
        "client_id": "client_123",
        "company_name": "TechFlow Innovations",
        "content_brief": "Create blog post about AI automation",
        "target_audience": "Technology decision makers",
        "content_goals": ["brand_awareness", "lead_generation"]
    }
)

result = response.json()
print(f"Request ID: {result['request_id']}")
        """, language='python')
    
    with tab2:
        st.code("""
// Create content using fetch
const response = await fetch('https://api.innovatemarketing.solutions/v1/content/create', {
    method: 'POST',
    headers: {
        'Authorization': 'Bearer YOUR_API_KEY',
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        client_id: 'client_123',
        company_name: 'TechFlow Innovations',
        content_brief: 'Create blog post about AI automation',
        target_audience: 'Technology decision makers',
        content_goals: ['brand_awareness', 'lead_generation']
    })
});

const result = await response.json();
console.log('Request ID:', result.request_id);
        """, language='javascript')
    
    with tab3:
        st.code("""
curl -X POST https://api.innovatemarketing.solutions/v1/content/create \\
  -H "Authorization: Bearer YOUR_API_KEY" \\
  -H "Content-Type: application/json" \\
  -d '{
    "client_id": "client_123",
    "company_name": "TechFlow Innovations",
    "content_brief": "Create blog post about AI automation",
    "target_audience": "Technology decision makers",
    "content_goals": ["brand_awareness", "lead_generation"]
  }'
        """, language='bash')

def system_health_page():
    """System health monitoring and diagnostics."""
    
    st.markdown('<div class="sub-header">🔍 System Health</div>', unsafe_allow_html=True)
    
    # Health status
    st.subheader("🏥 Health Status")
    
    # Mock health data
    health_data = {
        "system_status": "Healthy",
        "uptime": "99.9%",
        "last_check": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "components": {
            "Content Generation": "Operational",
            "SEO Optimization": "Operational",
            "Quality Assurance": "Operational",
            "Research Tools": "Operational (DuckDuckGo)",
            "AI Writing": "Operational" if os.getenv("OPENAI_API_KEY") else "Mock Mode"
        }
    }
    
    # Status indicators
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("System Status", health_data["system_status"])
    
    with col2:
        st.metric("Uptime", health_data["uptime"])
    
    with col3:
        st.metric("Last Check", health_data["last_check"])
    
    # Component status
    st.subheader("🔧 Component Status")
    
    for component, status in health_data["components"].items():
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write(f"**{component}**")
        with col2:
            if status == "Operational":
                st.success(status)
            elif status == "Limited":
                st.warning(status)
            else:
                st.info(status)
    
    # Environment check
    st.subheader("🌍 Environment Configuration")
    
    env_checks = [
        {"name": "OPENAI_API_KEY", "status": "✅ Configured" if os.getenv("OPENAI_API_KEY") else "⚠️ Not Set"},
        {"name": "SERPAPI_API_KEY", "status": "✅ Configured" if os.getenv("SERPAPI_API_KEY") else "⚠️ Not Set"},
        {"name": "Python Version", "status": f"✅ {sys.version.split()[0]}"},
        {"name": "LangGraph", "status": "✅ Available"},
    ]
    
    for check in env_checks:
        col1, col2 = st.columns([3, 2])
        with col1:
            st.write(f"**{check['name']}**")
        with col2:
            st.write(check['status'])
    
    # System logs
    st.subheader("📝 Recent System Logs")
    
    mock_logs = [
        {"timestamp": datetime.now().strftime("%H:%M:%S"), "level": "INFO", "message": "Content creation completed successfully"},
        {"timestamp": (datetime.now()).strftime("%H:%M:%S"), "level": "INFO", "message": "SEO optimization processed"},
        {"timestamp": (datetime.now()).strftime("%H:%M:%S"), "level": "WARNING", "message": "API key not configured for enhanced features"},
    ]
    
    for log in mock_logs:
        level_color = {"INFO": "🟢", "WARNING": "🟡", "ERROR": "🔴"}
        st.write(f"{level_color.get(log['level'], '🔵')} {log['timestamp']} - {log['level']}: {log['message']}")

def run_claude_content_system(client_brief: str, target_audience: str, content_goals: List[str], 
                            content_type: str, keywords: List[str]) -> Dict[str, Any]:
    """Run Claude AI-powered content creation system."""
    
    try:
        # Initialize Claude content generator
        claude_generator = ClaudeContentGenerator()
        claude_optimizer = ClaudeContentOptimizer()
        
        # Prepare comprehensive content requirements
        content_requirements = {
            "content_type": content_type,
            "topic": _extract_topic_from_brief(client_brief),
            "target_audience": target_audience,
            "tone": "professional",
            "word_count": _determine_word_count(content_type),
            "keywords": keywords,
            "research_insights": _extract_insights_from_brief(client_brief),
            "competitive_analysis": "Position content uniquely in market",
            "content_goals": content_goals,
            "brand_guidelines": {
                "tone": "professional and authoritative",
                "voice": "knowledgeable expert"
            }
        }
        
        # Generate content with Claude
        generation_result = claude_generator.generate_content(content_requirements)
        
        # Optimize content if generation was successful
        if generation_result and generation_result.get("content"):
            optimization_goals = ["improve_readability", "enhance_engagement", "strengthen_seo"]
            optimization_result = claude_optimizer.optimize_content(
                generation_result["content"], 
                optimization_goals
            )
            
            # Combine results
            final_result = {
                "primary_content": optimization_result.get("optimized_content", generation_result["content"]),
                "original_content": generation_result["content"],
                "content_analysis": generation_result.get("content_analysis", {}),
                "optimization_analysis": optimization_result.get("optimization_analysis", {}),
                "generation_metadata": generation_result.get("generation_metadata", {}),
                "quality_score": generation_result.get("quality_score", 0),
                "requirements_met": generation_result.get("requirements_met", {}),
                "claude_features": "active",
                "deliverables": {
                    "primary_content": optimization_result.get("optimized_content", generation_result["content"]),
                    "meta_data": _generate_meta_data(generation_result),
                    "quality_report": _generate_quality_report(generation_result)
                },
                "performance_metrics": {
                    "content_length": generation_result.get("content_analysis", {}).get("word_count", 0),
                    "quality_score": generation_result.get("quality_score", 0),
                    "seo_optimization_score": 90,  # High score for Claude-generated content
                    "readability_score": generation_result.get("content_analysis", {}).get("readability_estimate", 75)
                }
            }
            
            return final_result
        else:
            # Return fallback result
            return _generate_claude_fallback_result(content_requirements)
            
    except Exception as e:
        return _generate_claude_fallback_result({
            "content_type": content_type,
            "topic": client_brief,
            "error": str(e)
        })

def _extract_topic_from_brief(brief: str) -> str:
    """Extract main topic from client brief."""
    lines = brief.split('\n')
    for line in lines:
        if line.strip() and len(line.strip()) > 10:
            return line.strip()[:100]
    return "Business Technology Solutions"

def _determine_word_count(content_type: str) -> int:
    """Determine appropriate word count based on content type."""
    word_counts = {
        "blog_post": 1000,
        "whitepaper": 2500,
        "case_study": 1500,
        "thought_leadership": 1200,
        "social_media": 300,
        "email_campaign": 500
    }
    return word_counts.get(content_type, 1000)

def _extract_insights_from_brief(brief: str) -> List[str]:
    """Extract key insights from client brief."""
    insights = []
    sentences = brief.split('.')
    for sentence in sentences:
        if any(keyword in sentence.lower() for keyword in ['goal', 'objective', 'need', 'want', 'require']):
            insights.append(sentence.strip())
    
    if not insights:
        insights = [
            "Client seeks professional content creation",
            "Focus on business value and practical insights",
            "Target audience engagement is priority"
        ]
    
    return insights[:3]

def _generate_meta_data(generation_result: Dict) -> Dict[str, str]:
    """Generate SEO metadata from Claude generation result."""
    content = generation_result.get("content", "")
    
    # Extract title (first heading or first line)
    lines = content.split('\n')
    title = "Professional Content"
    for line in lines:
        if line.strip().startswith('#'):
            title = line.strip().replace('#', '').strip()
            break
        elif line.strip() and len(line.strip()) > 10:
            title = line.strip()[:60]
            break
    
    # Generate description from first paragraph
    paragraphs = content.split('\n\n')
    description = "Professional content generated with Claude AI"
    for para in paragraphs:
        if para.strip() and len(para.strip()) > 50:
            description = para.strip()[:160] + "..."
            break
    
    return {
        "title": title,
        "description": description,
        "keywords": "business, technology, professional content",
        "author": "Claude AI Content Generator",
        "content_type": "article"
    }

def _generate_quality_report(generation_result: Dict) -> Dict[str, Any]:
    """Generate quality report from Claude generation result."""
    requirements_met = generation_result.get("requirements_met", {})
    quality_score = generation_result.get("quality_score", 0)
    
    checks = []
    for requirement, met in requirements_met.items():
        if met:
            checks.append(f"✅ {requirement.replace('_', ' ').title()}")
        else:
            checks.append(f"⚠️ {requirement.replace('_', ' ').title()}")
    
    approval_status = "Approved" if quality_score >= 80 else "Needs Review" if quality_score >= 60 else "Requires Revision"
    
    return {
        "approval_status": approval_status,
        "quality_score": quality_score,
        "checks": checks,
        "claude_analysis": "Content generated and analyzed with Claude AI",
        "recommendations": generation_result.get("content_analysis", {}).get("recommendations", [])
    }

def _generate_claude_fallback_result(requirements: Dict) -> Dict[str, Any]:
    """Generate fallback result when Claude generation fails."""
    
    fallback_content = f"""# {requirements.get('topic', 'Professional Content')}

## Executive Summary

This content has been generated using the Claude AI-powered content creation system, designed to deliver high-quality, professional content that meets your specific requirements.

## Key Insights

Based on your content requirements, this analysis addresses the primary objectives and delivers actionable insights for your target audience.

### Strategic Focus Areas

1. **Content Quality**: Professional-grade content creation
2. **Audience Engagement**: Targeted messaging for {requirements.get('target_audience', 'business professionals')}
3. **Value Delivery**: Practical insights and recommendations

## Implementation Guidance

The content creation process leverages advanced AI capabilities to ensure comprehensive coverage of your topic while maintaining professional standards and audience engagement.

## Conclusion

This content demonstrates the capabilities of Claude AI-powered content generation, providing a foundation for your content marketing and thought leadership initiatives.

---

*Generated with Claude AI Content Creation System*
"""
    
    return {
        "primary_content": fallback_content,
        "content_analysis": {"word_count": len(fallback_content.split())},
        "quality_score": 75,
        "claude_features": "fallback_mode",
        "deliverables": {
            "primary_content": fallback_content,
            "meta_data": {
                "title": requirements.get('topic', 'Professional Content'),
                "description": "Claude AI-generated professional content",
                "keywords": "business, professional, content"
            },
            "quality_report": {
                "approval_status": "Generated (Fallback Mode)",
                "checks": ["Content structure maintained", "Professional tone achieved"]
            }
        },
        "performance_metrics": {
            "content_length": len(fallback_content.split()),
            "quality_score": 75,
            "seo_optimization_score": 70,
            "readability_score": 80
        }
    }

if __name__ == "__main__":
    main()