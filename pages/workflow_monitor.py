"""
Workflow Monitoring Page for LangGraph System
Real-time monitoring and visualization of workflow execution
"""
import streamlit as st
import time
from datetime import datetime
import json
from workflow_visualizer import display_workflow_visualization
from advanced_langgraph_workflow import run_advanced_langgraph_workflow

def initialize_monitoring_state():
    """Initialize session state for workflow monitoring"""
    if 'workflow_executions' not in st.session_state:
        st.session_state.workflow_executions = []
    if 'current_execution' not in st.session_state:
        st.session_state.current_execution = None
    if 'monitoring_active' not in st.session_state:
        st.session_state.monitoring_active = False

def display_workflow_controls():
    """Display workflow execution controls"""
    st.header("🎛️ Workflow Control Panel")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("⚙️ Execution Parameters")
        
        # Input parameters
        topic = st.text_input(
            "Content Topic:",
            value="AI automation for small businesses",
            help="The main topic for content generation"
        )
        
        col_a, col_b = st.columns(2)
        with col_a:
            content_type = st.selectbox(
                "Content Type:",
                ["blog_post", "social_media", "website_copy"],
                help="Type of content to generate"
            )
        
        with col_b:
            target_audience = st.text_input(
                "Target Audience:",
                value="small business owners",
                help="Specific audience for the content"
            )
        
        keywords = st.text_area(
            "Additional Keywords:",
            placeholder="automation, efficiency, productivity",
            help="Comma-separated keywords to include"
        ).split(',') if st.text_area(
            "Additional Keywords:",
            placeholder="automation, efficiency, productivity",
            help="Comma-separated keywords to include"
        ) else []
        
        keywords = [k.strip() for k in keywords if k.strip()]
    
    with col2:
        st.subheader("🚀 Execution")
        
        # Execution button
        if st.button("▶️ Start Workflow", type="primary", use_container_width=True):
            if topic:
                st.session_state.monitoring_active = True
                execute_monitored_workflow(topic, content_type, target_audience, keywords)
            else:
                st.error("Please enter a topic")
        
        # Stop button
        if st.session_state.monitoring_active:
            if st.button("⏹️ Stop Monitoring", type="secondary", use_container_width=True):
                st.session_state.monitoring_active = False
                st.rerun()
        
        # Clear history
        if st.button("🗑️ Clear History", use_container_width=True):
            st.session_state.workflow_executions = []
            st.session_state.current_execution = None
            st.success("History cleared!")

def execute_monitored_workflow(topic: str, content_type: str, target_audience: str, keywords: list):
    """Execute workflow with real-time monitoring"""
    
    # Create execution record
    execution_id = f"exec_{int(datetime.now().timestamp())}"
    execution_record = {
        "id": execution_id,
        "topic": topic,
        "content_type": content_type,
        "target_audience": target_audience,
        "keywords": keywords,
        "start_time": datetime.now().isoformat(),
        "status": "running",
        "result": None
    }
    
    st.session_state.workflow_executions.append(execution_record)
    st.session_state.current_execution = execution_record
    
    # Display real-time monitoring
    display_real_time_monitoring(execution_record)
    
    # Execute the workflow
    with st.spinner("🔄 Executing Advanced LangGraph Workflow..."):
        try:
            result = run_advanced_langgraph_workflow(
                topic=topic,
                content_type=content_type,
                target_audience=target_audience,
                specific_keywords=keywords
            )
            
            # Update execution record
            execution_record["status"] = "completed" if result.get("success") else "failed"
            execution_record["result"] = result
            execution_record["end_time"] = datetime.now().isoformat()
            
            st.session_state.monitoring_active = False
            st.success("✅ Workflow completed successfully!")
            st.rerun()
            
        except Exception as e:
            execution_record["status"] = "error"
            execution_record["error"] = str(e)
            execution_record["end_time"] = datetime.now().isoformat()
            st.session_state.monitoring_active = False
            st.error(f"❌ Workflow failed: {e}")

def display_real_time_monitoring(execution_record: dict):
    """Display real-time workflow monitoring"""
    
    st.subheader("📊 Real-Time Workflow Monitoring")
    
    # Progress tracking
    progress_container = st.container()
    
    with progress_container:
        # Workflow stages
        stages = [
            ("🚀 Initialize", "Setting up workflow parameters"),
            ("🔍 Research", "Conducting topic research and analysis"),
            ("📋 Plan", "Creating content structure and outline"),
            ("✍️ Write", "Generating content based on research"),
            ("📖 Review", "Reviewing content quality and structure"),
            ("🔍 SEO", "Optimizing for search engines"),
            ("✅ Quality", "Final quality assurance check"),
            ("📦 Assembly", "Preparing final content package"),
            ("🎉 Complete", "Workflow execution finished")
        ]
        
        # Create progress visualization
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown("**Execution Status:**")
            st.info(f"🆔 ID: {execution_record['id']}")
            st.info(f"📝 Topic: {execution_record['topic']}")
            st.info(f"⏰ Started: {execution_record['start_time'].split('T')[1][:8]}")
        
        with col2:
            st.markdown("**Progress Stages:**")
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Simulate workflow progression
            for i, (stage_icon, stage_desc) in enumerate(stages):
                progress = (i + 1) / len(stages)
                progress_bar.progress(progress)
                status_text.text(f"{stage_icon} {stage_desc}")
                
                if st.session_state.monitoring_active:
                    time.sleep(0.8)  # Simulate processing time
                else:
                    break
            
            if st.session_state.monitoring_active:
                status_text.text("🎉 Workflow completed successfully!")

def display_execution_history():
    """Display workflow execution history"""
    
    if not st.session_state.workflow_executions:
        st.info("No workflow executions yet. Start a workflow to see monitoring data.")
        return
    
    st.subheader("📚 Execution History")
    
    # Display executions in reverse chronological order
    for execution in reversed(st.session_state.workflow_executions):
        with st.expander(f"🔄 {execution['topic']} - {execution['status'].upper()}"):
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("**Execution Details:**")
                st.write(f"**ID:** {execution['id']}")
                st.write(f"**Topic:** {execution['topic']}")
                st.write(f"**Type:** {execution['content_type']}")
                st.write(f"**Audience:** {execution['target_audience']}")
                if execution.get('keywords'):
                    st.write(f"**Keywords:** {', '.join(execution['keywords'])}")
            
            with col2:
                st.markdown("**Timing:**")
                st.write(f"**Started:** {execution['start_time']}")
                if execution.get('end_time'):
                    st.write(f"**Completed:** {execution['end_time']}")
                    
                    # Calculate duration
                    start = datetime.fromisoformat(execution['start_time'])
                    end = datetime.fromisoformat(execution['end_time'])
                    duration = (end - start).total_seconds()
                    st.write(f"**Duration:** {duration:.2f}s")
            
            with col3:
                st.markdown("**Results:**")
                
                if execution['status'] == 'completed' and execution.get('result'):
                    result = execution['result']
                    if result.get('success'):
                        quality_score = result.get('quality_score', 0)
                        word_count = result.get('metadata', {}).get('final_word_count', 0)
                        
                        st.metric("Quality Score", f"{quality_score:.1f}/100")
                        st.metric("Word Count", word_count)
                        
                        # Action buttons
                        if st.button(f"📄 View Content", key=f"view_{execution['id']}"):
                            st.session_state.selected_execution = execution
                        
                        if st.button(f"📊 View Analysis", key=f"analyze_{execution['id']}"):
                            display_execution_analysis(execution)
                    
                elif execution['status'] == 'failed':
                    st.error("❌ Execution failed")
                    if execution.get('error'):
                        st.code(execution['error'])
                
                elif execution['status'] == 'running':
                    st.warning("⏳ Still running...")

def display_execution_analysis(execution: dict):
    """Display detailed analysis of a workflow execution"""
    
    st.subheader(f"📊 Execution Analysis: {execution['topic']}")
    
    if not execution.get('result') or not execution['result'].get('success'):
        st.error("No analysis available for failed executions")
        return
    
    result = execution['result']
    
    # Display workflow visualization with actual results
    display_workflow_visualization(result)
    
    # Detailed metrics
    st.subheader("📈 Performance Metrics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        quality_score = result.get('quality_score', 0)
        st.metric("Quality Score", f"{quality_score:.1f}/100")
    
    with col2:
        seo_score = result.get('seo_data', {}).get('seo_score', 0)
        st.metric("SEO Score", f"{seo_score:.1f}/100")
    
    with col3:
        word_count = result.get('metadata', {}).get('final_word_count', 0)
        st.metric("Word Count", word_count)
    
    with col4:
        total_time = result.get('metadata', {}).get('total_processing_time', 0)
        st.metric("Processing Time", f"{total_time:.2f}s")
    
    # Content preview
    with st.expander("📄 Generated Content Preview"):
        content = result.get('final_content', 'No content available')
        st.text_area("Content:", content, height=300)
    
    # SEO data
    with st.expander("🔍 SEO Analysis"):
        seo_data = result.get('seo_data', {})
        
        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown("**Meta Description:**")
            st.write(seo_data.get('meta_description', 'Not available'))
            
            st.markdown("**Primary Keywords:**")
            keywords = seo_data.get('primary_keywords', [])
            if keywords:
                st.write(", ".join(keywords))
            else:
                st.write("No keywords identified")
        
        with col_b:
            st.markdown("**Title Suggestions:**")
            titles = seo_data.get('title_suggestions', [])
            for i, title in enumerate(titles, 1):
                st.write(f"{i}. {title}")
    
    # Workflow analytics
    with st.expander("🔧 Workflow Analytics"):
        analytics = result.get('workflow_analytics', {})
        
        if analytics.get('processing_time'):
            st.markdown("**Processing Time by Stage:**")
            for stage, time_taken in analytics['processing_time'].items():
                st.write(f"• {stage.replace('_', ' ').title()}: {time_taken:.2f}s")
        
        if analytics.get('agent_iterations'):
            st.markdown("**Agent Iterations:**")
            for agent, iterations in analytics['agent_iterations'].items():
                st.write(f"• {agent.title()}: {iterations} iteration(s)")
        
        revision_count = analytics.get('revision_count', 0)
        if revision_count > 0:
            st.warning(f"⚠️ Content required {revision_count} revision(s)")

def main():
    """Main workflow monitoring page"""
    st.set_page_config(
        page_title="Workflow Monitor",
        page_icon="📊",
        layout="wide"
    )
    
    st.title("📊 LangGraph Workflow Monitor")
    st.markdown("Real-time monitoring and analysis of content creation workflows")
    
    # Initialize state
    initialize_monitoring_state()
    
    # Create tabs
    tab1, tab2, tab3 = st.tabs(["🎛️ Control Panel", "📚 Execution History", "🔄 Workflow Diagram"])
    
    with tab1:
        display_workflow_controls()
        
        # Show current execution if running
        if st.session_state.current_execution and st.session_state.monitoring_active:
            st.markdown("---")
            display_real_time_monitoring(st.session_state.current_execution)
    
    with tab2:
        display_execution_history()
        
        # Show selected execution details
        if hasattr(st.session_state, 'selected_execution'):
            st.markdown("---")
            display_execution_analysis(st.session_state.selected_execution)
    
    with tab3:
        # Show workflow diagram with latest results if available
        latest_result = None
        if st.session_state.workflow_executions:
            latest_execution = st.session_state.workflow_executions[-1]
            if latest_execution.get('result') and latest_execution['result'].get('success'):
                latest_result = latest_execution['result']
        
        display_workflow_visualization(latest_result)

if __name__ == "__main__":
    main()