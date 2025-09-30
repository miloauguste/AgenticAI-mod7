"""
Workflow Visualization for LangGraph Content Creation System
"""
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import networkx as nx
from typing import Dict, List, Any
import pandas as pd

class WorkflowVisualizer:
    """
    Visualize the LangGraph workflow states and transitions
    """
    
    def __init__(self):
        self.workflow_graph = self._create_workflow_graph()
        
    def _create_workflow_graph(self) -> nx.DiGraph:
        """Create NetworkX graph representing the workflow"""
        G = nx.DiGraph()
        
        # Define all workflow nodes (states)
        nodes = [
            ("initialize_workflow", {"agent": "System Coordinator", "type": "start", "color": "#2E8B57"}),
            ("research_agent", {"agent": "Research Specialist", "type": "agent", "color": "#4169E1"}),
            ("analyze_research", {"agent": "Research Analyst", "type": "analysis", "color": "#FF6347"}),
            ("content_planning", {"agent": "Content Strategist", "type": "agent", "color": "#4169E1"}),
            ("content_writing", {"agent": "Content Writer", "type": "agent", "color": "#4169E1"}),
            ("content_review", {"agent": "Content Editor", "type": "analysis", "color": "#FF6347"}),
            ("seo_optimization", {"agent": "SEO Specialist", "type": "agent", "color": "#4169E1"}),
            ("quality_assurance", {"agent": "QA Specialist", "type": "analysis", "color": "#FF6347"}),
            ("revision_planning", {"agent": "Revision Planner", "type": "planning", "color": "#FFD700"}),
            ("content_revision", {"agent": "Content Revisor", "type": "agent", "color": "#4169E1"}),
            ("final_assembly", {"agent": "Content Assembler", "type": "processing", "color": "#9370DB"}),
            ("workflow_completion", {"agent": "Workflow Manager", "type": "end", "color": "#228B22"}),
            ("error_handling", {"agent": "Error Handler", "type": "error", "color": "#DC143C"})
        ]
        
        # Add nodes to graph
        for node_id, attributes in nodes:
            G.add_node(node_id, **attributes)
        
        # Define edges (transitions)
        edges = [
            # Main workflow path
            ("initialize_workflow", "research_agent", {"type": "sequential", "label": "Start Research"}),
            ("research_agent", "analyze_research", {"type": "sequential", "label": "Analyze Results"}),
            ("content_planning", "content_writing", {"type": "sequential", "label": "Write Content"}),
            ("content_writing", "content_review", {"type": "sequential", "label": "Review Content"}),
            ("seo_optimization", "quality_assurance", {"type": "sequential", "label": "Quality Check"}),
            ("revision_planning", "content_revision", {"type": "sequential", "label": "Revise Content"}),
            ("content_revision", "content_review", {"type": "loop", "label": "Re-review"}),
            ("final_assembly", "workflow_completion", {"type": "sequential", "label": "Complete"}),
            
            # Conditional edges
            ("analyze_research", "content_planning", {"type": "conditional", "label": "Research OK"}),
            ("analyze_research", "research_agent", {"type": "conditional", "label": "Retry Research"}),
            ("analyze_research", "error_handling", {"type": "conditional", "label": "Research Failed"}),
            
            ("content_review", "seo_optimization", {"type": "conditional", "label": "Content OK"}),
            ("content_review", "content_revision", {"type": "conditional", "label": "Needs Revision"}),
            ("content_review", "error_handling", {"type": "conditional", "label": "Content Failed"}),
            
            ("quality_assurance", "final_assembly", {"type": "conditional", "label": "Quality OK"}),
            ("quality_assurance", "revision_planning", {"type": "conditional", "label": "Needs Improvement"}),
            ("quality_assurance", "error_handling", {"type": "conditional", "label": "Quality Failed"}),
        ]
        
        # Add edges to graph
        for source, target, attributes in edges:
            G.add_edge(source, target, **attributes)
        
        return G
    
    def create_workflow_diagram(self) -> go.Figure:
        """Create interactive workflow diagram using Plotly"""
        
        # Use hierarchical layout for better visualization
        pos = nx.spring_layout(self.workflow_graph, k=3, iterations=50, seed=42)
        
        # Extract node information
        node_x = []
        node_y = []
        node_text = []
        node_colors = []
        node_sizes = []
        
        for node in self.workflow_graph.nodes():
            x, y = pos[node]
            node_x.append(x)
            node_y.append(y)
            
            # Create hover text
            attrs = self.workflow_graph.nodes[node]
            hover_text = f"<b>{node.replace('_', ' ').title()}</b><br>"
            hover_text += f"Agent: {attrs['agent']}<br>"
            hover_text += f"Type: {attrs['type'].title()}"
            node_text.append(hover_text)
            
            node_colors.append(attrs['color'])
            
            # Size based on node type
            if attrs['type'] in ['start', 'end']:
                node_sizes.append(30)
            elif attrs['type'] == 'agent':
                node_sizes.append(25)
            elif attrs['type'] == 'error':
                node_sizes.append(20)
            else:
                node_sizes.append(22)
        
        # Create edge traces
        edge_x = []
        edge_y = []
        edge_info = []
        
        for edge in self.workflow_graph.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_x.extend([x0, x1, None])
            edge_y.extend([y0, y1, None])
            
            attrs = self.workflow_graph.edges[edge]
            edge_info.append(f"{edge[0]} → {edge[1]}: {attrs.get('label', '')}")
        
        # Create the plot
        fig = go.Figure()
        
        # Add edges
        fig.add_trace(go.Scatter(
            x=edge_x, y=edge_y,
            line=dict(width=2, color='#888'),
            hoverinfo='none',
            mode='lines',
            name='Transitions'
        ))
        
        # Add nodes
        fig.add_trace(go.Scatter(
            x=node_x, y=node_y,
            mode='markers+text',
            hoverinfo='text',
            hovertext=node_text,
            text=[node.replace('_', '<br>').title() for node in self.workflow_graph.nodes()],
            textposition="middle center",
            textfont=dict(size=10, color='white'),
            marker=dict(
                size=node_sizes,
                color=node_colors,
                line=dict(width=2, color='white'),
                opacity=0.9
            ),
            name='Workflow States'
        ))
        
        # Update layout
        fig.update_layout(
            title={
                'text': "🔄 LangGraph Content Creation Workflow",
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 20}
            },
            showlegend=False,
            hovermode='closest',
            margin=dict(b=20,l=5,r=5,t=40),
            annotations=[
                dict(
                    text="Click nodes to see agent details • Hover for information",
                    showarrow=False,
                    xref="paper", yref="paper",
                    x=0.005, y=-0.002,
                    xanchor='left', yanchor='bottom',
                    font=dict(color='gray', size=12)
                )
            ],
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            height=600,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        return fig
    
    def create_agent_breakdown_chart(self) -> go.Figure:
        """Create chart showing agent types and responsibilities"""
        
        # Extract agent information
        agents_data = []
        for node, attrs in self.workflow_graph.nodes(data=True):
            agents_data.append({
                'state': node.replace('_', ' ').title(),
                'agent': attrs['agent'],
                'type': attrs['type'].title(),
                'color': attrs['color']
            })
        
        df = pd.DataFrame(agents_data)
        
        # Count by agent type
        type_counts = df['type'].value_counts()
        
        # Create pie chart
        fig = go.Figure(data=[go.Pie(
            labels=type_counts.index,
            values=type_counts.values,
            hole=.3,
            marker_colors=['#4169E1', '#FF6347', '#FFD700', '#9370DB', '#2E8B57', '#DC143C']
        )])
        
        fig.update_layout(
            title={
                'text': "🎭 Agent Types Distribution",
                'x': 0.5,
                'xanchor': 'center'
            },
            font=dict(size=12),
            height=400
        )
        
        return fig
    
    def create_workflow_metrics_dashboard(self, workflow_result: Dict[str, Any] = None) -> go.Figure:
        """Create dashboard showing workflow execution metrics"""
        
        if not workflow_result or not workflow_result.get('success'):
            # Create placeholder metrics
            processing_times = {
                'Research': 2.3,
                'Writing': 3.1,
                'SEO': 1.2,
                'Quality Check': 0.8,
                'Assembly': 0.5
            }
        else:
            # Use actual metrics from workflow result
            analytics = workflow_result.get('workflow_analytics', {})
            processing_times = analytics.get('processing_time', {})
        
        # Create subplots
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Processing Time by Stage', 'Quality Metrics', 
                          'Agent Iterations', 'Workflow Performance'),
            specs=[[{"type": "bar"}, {"type": "indicator"}],
                   [{"type": "bar"}, {"type": "scatter"}]]
        )
        
        # Processing time chart
        stages = list(processing_times.keys())
        times = list(processing_times.values())
        
        fig.add_trace(
            go.Bar(x=stages, y=times, marker_color='#4169E1', name='Processing Time'),
            row=1, col=1
        )
        
        # Quality indicator
        quality_score = workflow_result.get('quality_score', 85) if workflow_result else 85
        fig.add_trace(
            go.Indicator(
                mode = "gauge+number+delta",
                value = quality_score,
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "Quality Score"},
                delta = {'reference': 80},
                gauge = {
                    'axis': {'range': [None, 100]},
                    'bar': {'color': "darkblue"},
                    'steps': [
                        {'range': [0, 50], 'color': "lightgray"},
                        {'range': [50, 80], 'color': "yellow"},
                        {'range': [80, 100], 'color': "green"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 90
                    }
                }
            ),
            row=1, col=2
        )
        
        # Agent iterations (if available)
        if workflow_result and 'workflow_analytics' in workflow_result:
            iterations = workflow_result['workflow_analytics'].get('agent_iterations', {})
            if iterations:
                fig.add_trace(
                    go.Bar(x=list(iterations.keys()), y=list(iterations.values()), 
                          marker_color='#FF6347', name='Iterations'),
                    row=2, col=1
                )
        
        # Performance timeline (simulated)
        timeline_x = ['Start', 'Research', 'Writing', 'SEO', 'QA', 'Complete']
        timeline_y = [0, 25, 60, 80, 95, 100]
        
        fig.add_trace(
            go.Scatter(x=timeline_x, y=timeline_y, mode='lines+markers',
                      marker_color='#2E8B57', name='Progress'),
            row=2, col=2
        )
        
        fig.update_layout(
            height=600,
            showlegend=False,
            title_text="📊 Workflow Execution Dashboard"
        )
        
        return fig
    
    def display_workflow_legend(self):
        """Display workflow legend and explanation"""
        st.markdown("""
        ### 🗺️ Workflow Legend
        
        **Node Types:**
        - 🟢 **Start/End**: Workflow entry and exit points
        - 🔵 **Agent States**: AI agents performing specific tasks
        - 🟠 **Analysis States**: Decision and evaluation nodes  
        - 🟡 **Planning States**: Strategy and revision planning
        - 🟣 **Processing States**: Data assembly and formatting
        - 🔴 **Error States**: Error handling and recovery
        
        **Transition Types:**
        - ➡️ **Sequential**: Automatic progression to next state
        - 🔀 **Conditional**: Decision-based routing
        - 🔄 **Loop**: Revision and retry cycles
        
        **Key Decision Points:**
        1. **Research Quality**: Determines if research is sufficient or needs retry
        2. **Content Quality**: Routes to SEO optimization or revision
        3. **Final Quality**: Decides between completion or additional improvements
        """)
    
    def display_state_details(self):
        """Display detailed information about each workflow state"""
        st.markdown("""
        ### 📋 Detailed State Descriptions
        """)
        
        states_info = {
            "🚀 Initialize Workflow": {
                "Agent": "System Coordinator",
                "Purpose": "Validate inputs and set up workflow parameters",
                "Duration": "~0.5s",
                "Outputs": "Validated parameters, content type configuration"
            },
            "🔍 Research Agent": {
                "Agent": "Research Specialist", 
                "Purpose": "Conduct comprehensive topic research using SerpAPI",
                "Duration": "~2-3s",
                "Outputs": "Search results, trending topics, keyword extraction"
            },
            "📊 Analyze Research": {
                "Agent": "Research Analyst",
                "Purpose": "Evaluate research quality and determine next steps", 
                "Duration": "~0.8s",
                "Outputs": "Quality assessment, confidence score, trending topics"
            },
            "📋 Content Planning": {
                "Agent": "Content Strategist",
                "Purpose": "Create content outline and structure based on research",
                "Duration": "~1s", 
                "Outputs": "Content outline, sections, primary keywords"
            },
            "✍️ Content Writing": {
                "Agent": "Content Writer",
                "Purpose": "Generate content using OpenAI based on plan and research",
                "Duration": "~3-4s",
                "Outputs": "Draft content, word count, structured sections"
            },
            "📖 Content Review": {
                "Agent": "Content Editor",
                "Purpose": "Initial quality check and structure validation",
                "Duration": "~0.8s",
                "Outputs": "Basic quality score, structure assessment"
            },
            "🔍 SEO Optimization": {
                "Agent": "SEO Specialist", 
                "Purpose": "Optimize content for search engines and keywords",
                "Duration": "~1.2s",
                "Outputs": "Optimized content, meta description, title suggestions, SEO score"
            },
            "✅ Quality Assurance": {
                "Agent": "QA Specialist",
                "Purpose": "Comprehensive quality evaluation and scoring",
                "Duration": "~0.8s", 
                "Outputs": "Quality score, feedback list, revision requirements"
            },
            "🔄 Revision Planning": {
                "Agent": "Revision Planner",
                "Purpose": "Plan content improvements based on quality feedback",
                "Duration": "~0.5s",
                "Outputs": "Revision strategy, improvement targets"
            },
            "✏️ Content Revision": {
                "Agent": "Content Revisor", 
                "Purpose": "Implement planned improvements to content",
                "Duration": "~2-3s",
                "Outputs": "Revised content, updated word count"
            },
            "📦 Final Assembly": {
                "Agent": "Content Assembler",
                "Purpose": "Prepare final content package with comprehensive metadata",
                "Duration": "~0.5s",
                "Outputs": "Final content, complete metadata, performance metrics"
            },
            "🎉 Workflow Completion": {
                "Agent": "Workflow Manager",
                "Purpose": "Finalize workflow and prepare output",
                "Duration": "~0.2s",
                "Outputs": "Completion timestamp, success confirmation, final metrics"
            }
        }
        
        # Display in columns
        col1, col2 = st.columns(2)
        
        states_list = list(states_info.items())
        mid_point = len(states_list) // 2
        
        with col1:
            for state, info in states_list[:mid_point]:
                with st.expander(state):
                    st.write(f"**Agent:** {info['Agent']}")
                    st.write(f"**Purpose:** {info['Purpose']}")
                    st.write(f"**Typical Duration:** {info['Duration']}")
                    st.write(f"**Key Outputs:** {info['Outputs']}")
        
        with col2:
            for state, info in states_list[mid_point:]:
                with st.expander(state):
                    st.write(f"**Agent:** {info['Agent']}")
                    st.write(f"**Purpose:** {info['Purpose']}")
                    st.write(f"**Typical Duration:** {info['Duration']}")
                    st.write(f"**Key Outputs:** {info['Outputs']}")

def display_workflow_visualization(workflow_result: Dict[str, Any] = None):
    """Main function to display workflow visualization in Streamlit"""
    
    st.header("🔄 LangGraph Workflow Visualization")
    
    visualizer = WorkflowVisualizer()
    
    # Create tabs for different views
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Workflow Diagram", "📈 Execution Metrics", "🎭 Agent Breakdown", "📋 State Details"])
    
    with tab1:
        st.plotly_chart(visualizer.create_workflow_diagram(), use_container_width=True)
        visualizer.display_workflow_legend()
    
    with tab2:
        st.plotly_chart(visualizer.create_workflow_metrics_dashboard(workflow_result), use_container_width=True)
        
        if workflow_result and workflow_result.get('success'):
            st.subheader("📊 Actual Workflow Results")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                quality_score = workflow_result.get('quality_score', 0)
                st.metric("Quality Score", f"{quality_score:.1f}/100")
            
            with col2:
                word_count = workflow_result.get('metadata', {}).get('final_word_count', 0)
                st.metric("Final Word Count", word_count)
            
            with col3:
                total_time = workflow_result.get('metadata', {}).get('total_processing_time', 0)
                st.metric("Processing Time", f"{total_time:.2f}s")
    
    with tab3:
        st.plotly_chart(visualizer.create_agent_breakdown_chart(), use_container_width=True)
        
        st.subheader("👥 Agent Responsibilities")
        st.markdown("""
        **🔵 Agent States (6)**: Core AI agents performing content tasks
        - Research Specialist, Content Writer, SEO Specialist, etc.
        
        **🟠 Analysis States (3)**: Decision and evaluation nodes  
        - Research Analyst, Content Editor, QA Specialist
        
        **🟡 Planning States (1)**: Strategy formulation
        - Revision Planner for improvement strategies
        
        **🟣 Processing States (1)**: Data assembly
        - Content Assembler for final packaging
        
        **🟢 Control States (2)**: Workflow management
        - System Coordinator and Workflow Manager
        
        **🔴 Error States (1)**: Exception handling
        - Error Handler for graceful failure recovery
        """)
    
    with tab4:
        visualizer.display_state_details()

if __name__ == "__main__":
    # For testing
    display_workflow_visualization()