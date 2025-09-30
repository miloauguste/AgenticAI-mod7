"""
Dashboard page for content analytics and metrics
"""
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime, timedelta
import json

def load_dashboard_data():
    """Load and prepare data for dashboard visualizations"""
    # Sample data - in production this would come from a database
    if 'content_history' in st.session_state and st.session_state.content_history:
        history = st.session_state.content_history
    else:
        # Sample data for demonstration
        history = [
            {
                "workflow": "CrewAI",
                "metadata": {
                    "topic": "AI automation for small businesses",
                    "timestamp": "2024-01-01T10:00:00",
                    "content_type": "blog_post"
                },
                "content": "Sample content about AI automation..." * 50,
                "quality_score": 85
            },
            {
                "workflow": "LangGraph", 
                "metadata": {
                    "topic": "Blockchain technology trends",
                    "timestamp": "2024-01-02T14:30:00",
                    "content_type": "social_media"
                },
                "content": "Blockchain is revolutionizing..." * 30,
                "quality_score": 92
            },
            {
                "workflow": "CrewAI",
                "metadata": {
                    "topic": "Remote work productivity tools",
                    "timestamp": "2024-01-03T09:15:00", 
                    "content_type": "website_copy"
                },
                "content": "Remote work has become..." * 40,
                "quality_score": 78
            }
        ]
    
    # Convert to DataFrame for analysis
    data = []
    for item in history:
        metadata = item.get("metadata", {})
        data.append({
            "workflow": item.get("workflow", "Unknown"),
            "topic": metadata.get("topic", "Unknown"),
            "content_type": metadata.get("content_type", "blog_post"),
            "timestamp": metadata.get("timestamp", datetime.now().isoformat()),
            "word_count": len(item.get("content", "").split()),
            "quality_score": item.get("quality_score", 0),
            "character_count": len(item.get("content", ""))
        })
    
    return pd.DataFrame(data)

def display_overview_metrics(df):
    """Display overview metrics"""
    st.header("📊 Content Analytics Dashboard")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_content = len(df)
        st.metric("Total Content Pieces", total_content, delta=f"+{min(3, total_content)} this week")
    
    with col2:
        avg_quality = df['quality_score'].mean() if not df.empty else 0
        st.metric("Average Quality Score", f"{avg_quality:.1f}/100", delta="+5.2")
    
    with col3:
        total_words = df['word_count'].sum() if not df.empty else 0
        st.metric("Total Words Generated", f"{total_words:,}", delta="+2,400")
    
    with col4:
        avg_words = df['word_count'].mean() if not df.empty else 0
        st.metric("Avg Words per Content", f"{avg_words:.0f}", delta="+50")

def display_workflow_comparison(df):
    """Display workflow performance comparison"""
    st.subheader("🔄 Workflow Performance Comparison")
    
    if df.empty:
        st.info("No data available for workflow comparison")
        return
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Quality score by workflow
        workflow_quality = df.groupby('workflow')['quality_score'].mean().reset_index()
        fig_quality = px.bar(
            workflow_quality, 
            x='workflow', 
            y='quality_score',
            title="Average Quality Score by Workflow",
            color='quality_score',
            color_continuous_scale='viridis'
        )
        fig_quality.update_layout(height=400)
        st.plotly_chart(fig_quality, use_container_width=True)
    
    with col2:
        # Content count by workflow
        workflow_counts = df['workflow'].value_counts().reset_index()
        workflow_counts.columns = ['workflow', 'count']
        fig_count = px.pie(
            workflow_counts,
            values='count',
            names='workflow', 
            title="Content Distribution by Workflow"
        )
        fig_count.update_layout(height=400)
        st.plotly_chart(fig_count, use_container_width=True)

def display_content_type_analysis(df):
    """Display content type analysis"""
    st.subheader("📝 Content Type Analysis")
    
    if df.empty:
        st.info("No data available for content type analysis")
        return
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Word count by content type
        type_words = df.groupby('content_type')['word_count'].mean().reset_index()
        fig_words = px.bar(
            type_words,
            x='content_type',
            y='word_count',
            title="Average Word Count by Content Type",
            color='word_count',
            color_continuous_scale='blues'
        )
        fig_words.update_layout(height=400)
        st.plotly_chart(fig_words, use_container_width=True)
    
    with col2:
        # Quality distribution
        fig_quality_dist = px.histogram(
            df,
            x='quality_score',
            nbins=10,
            title="Quality Score Distribution",
            color_discrete_sequence=['#1f77b4']
        )
        fig_quality_dist.update_layout(height=400)
        st.plotly_chart(fig_quality_dist, use_container_width=True)

def display_timeline_analysis(df):
    """Display timeline analysis"""
    st.subheader("📅 Content Generation Timeline")
    
    if df.empty:
        st.info("No data available for timeline analysis")
        return
    
    # Convert timestamp to datetime
    df['date'] = pd.to_datetime(df['timestamp']).dt.date
    daily_counts = df.groupby('date').size().reset_index(name='count')
    
    fig_timeline = px.line(
        daily_counts,
        x='date',
        y='count',
        title="Daily Content Generation",
        markers=True
    )
    fig_timeline.update_layout(height=400)
    st.plotly_chart(fig_timeline, use_container_width=True)

def display_performance_insights(df):
    """Display performance insights and recommendations"""
    st.subheader("💡 Performance Insights")
    
    if df.empty:
        st.info("Generate some content to see performance insights!")
        return
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🎯 Key Insights")
        
        # Best performing workflow
        if not df.empty:
            best_workflow = df.groupby('workflow')['quality_score'].mean().idxmax()
            st.success(f"**Best Workflow:** {best_workflow}")
            
            # Most productive content type
            most_words = df.groupby('content_type')['word_count'].mean().idxmax()
            st.info(f"**Most Detailed Content:** {most_words}")
            
            # Quality trend
            avg_quality = df['quality_score'].mean()
            if avg_quality >= 85:
                st.success(f"**Quality Status:** Excellent ({avg_quality:.1f}/100)")
            elif avg_quality >= 75:
                st.warning(f"**Quality Status:** Good ({avg_quality:.1f}/100)")
            else:
                st.error(f"**Quality Status:** Needs Improvement ({avg_quality:.1f}/100)")
    
    with col2:
        st.markdown("### 📈 Recommendations")
        
        recommendations = []
        
        if not df.empty:
            avg_quality = df['quality_score'].mean()
            if avg_quality < 80:
                recommendations.append("🔧 Consider adjusting quality thresholds")
            
            avg_words = df['word_count'].mean()
            if avg_words < 300:
                recommendations.append("📝 Increase minimum word count for better content depth")
            
            workflow_counts = df['workflow'].value_counts()
            if len(workflow_counts) == 1:
                recommendations.append("🔄 Try both CrewAI and LangGraph workflows for comparison")
            
            if len(recommendations) == 0:
                recommendations.append("✅ System performing optimally!")
        else:
            recommendations.append("📊 Generate content to receive personalized recommendations")
        
        for rec in recommendations:
            st.markdown(f"• {rec}")

def main():
    """Main dashboard page"""
    st.set_page_config(
        page_title="Analytics Dashboard",
        page_icon="📊",
        layout="wide"
    )
    
    # Load data
    df = load_dashboard_data()
    
    # Display components
    display_overview_metrics(df)
    
    st.markdown("---")
    
    # Workflow and content analysis
    col1, col2 = st.columns(2)
    with col1:
        display_workflow_comparison(df)
    with col2:
        display_content_type_analysis(df)
    
    st.markdown("---")
    
    # Timeline analysis
    display_timeline_analysis(df)
    
    st.markdown("---")
    
    # Performance insights
    display_performance_insights(df)
    
    # Raw data table
    with st.expander("📋 Raw Data Table"):
        if not df.empty:
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No content generated yet. Use the main app to create content!")

if __name__ == "__main__":
    main()