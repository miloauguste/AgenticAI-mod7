import os
from typing import Dict, Any, List
from dotenv import load_dotenv
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from typing_extensions import TypedDict
from research_tool import research_tool
from writing_tool import writing_tool
from SEO_tool import seo_tool

load_dotenv()

class ContentState(TypedDict):
    topic: str
    content_type: str
    research_data: str
    content: str
    seo_optimized_content: str
    quality_report: str
    final_output: str

class QualityAssuranceTool:
    def __init__(self):
        self.criteria = [
            "content_quality",
            "grammar_check", 
            "brand_consistency",
            "seo_compliance",
            "readability"
        ]
    
    def run(self, content: str) -> str:
        try:
            issues = []
            
            word_count = len(content.split())
            if word_count < 300:
                issues.append("Content is too short (minimum 300 words)")
            
            if content.count('.') < 3:
                issues.append("Content needs more complete sentences")
            
            if not any(keyword in content.lower() for keyword in ['ai', 'technology', 'digital', 'startup']):
                issues.append("Content lacks relevant keywords for tech startups")
            
            if not issues:
                return "Quality check passed: Content meets all basic criteria"
            else:
                return f"Quality issues found: {'; '.join(issues)}"
                
        except Exception as e:
            return f"Error during quality check: {e}"

qa_tool = QualityAssuranceTool()

def research_node(state: ContentState) -> ContentState:
    """Research trending topics and gather relevant information."""
    print("Starting research phase...")
    
    topic = state.get("topic", "AI automation for small businesses")
    
    # Create more varied and comprehensive research queries
    import random
    import datetime
    
    current_year = datetime.datetime.now().year
    query_templates = [
        f"{topic} market trends {current_year} analysis",
        f"latest developments {topic} industry insights",
        f"{topic} best practices implementation guide {current_year}",
        f"{topic} technology innovation trends future outlook",
        f"comprehensive {topic} research market opportunities",
        f"{topic} case studies success stories {current_year}",
        f"{topic} competitive analysis market landscape",
        f"emerging {topic} solutions technology advancement"
    ]
    
    # Select a random query template for uniqueness
    research_query = random.choice(query_templates)
    
    try:
        print(f"Research query: {research_query}")
        research_data = research_tool._run(research_query)
        print(f"Research completed for: {topic}")
        return {**state, "research_data": research_data}
    except Exception as e:
        print(f"Research failed: {e}")
        return {**state, "research_data": f"Enhanced research data for {topic} - {research_query}"}

def writing_node(state: ContentState) -> ContentState:
    """Generate content based on research data."""
    print("Starting content writing phase...")
    
    research_data = state.get("research_data", "")
    
    try:
        content = writing_tool._run(research_data)
        print("Content writing completed")
        return {**state, "content": content}
    except Exception as e:
        print(f"Content writing failed: {e}")
        return {**state, "content": f"Mock content based on research: {research_data[:100]}..."}

def seo_optimization_node(state: ContentState) -> ContentState:
    """Optimize content for SEO."""
    print("Starting SEO optimization phase...")
    
    content = state.get("content", "")
    
    try:
        seo_content = seo_tool._run(content)
        print("SEO optimization completed")
        return {**state, "seo_optimized_content": seo_content}
    except Exception as e:
        print(f"SEO optimization failed: {e}")
        return {**state, "seo_optimized_content": content}

def quality_assurance_node(state: ContentState) -> ContentState:
    """Perform quality assurance on the content."""
    print("Starting quality assurance phase...")
    
    seo_content = state.get("seo_optimized_content", "")
    
    try:
        quality_report = qa_tool.run(seo_content)
        print("Quality assurance completed")
        
        final_output = f"""
=== CONTENT CREATION PIPELINE RESULTS ===

TOPIC: {state.get('topic', 'N/A')}
CONTENT TYPE: {state.get('content_type', 'N/A')}

FINAL CONTENT:
{seo_content}

QUALITY REPORT:
{quality_report}

=== END RESULTS ===
"""
        
        return {**state, "quality_report": quality_report, "final_output": final_output}
    except Exception as e:
        print(f"Quality assurance failed: {e}")
        return {**state, "quality_report": f"QA Error: {e}", "final_output": seo_content}

def create_content_workflow():
    """Create the LangGraph workflow for content creation."""
    
    workflow = StateGraph(ContentState)
    
    # Add nodes
    workflow.add_node("research", research_node)
    workflow.add_node("writing", writing_node)
    workflow.add_node("seo_optimization", seo_optimization_node)
    workflow.add_node("quality_assurance", quality_assurance_node)
    
    # Define the flow
    workflow.set_entry_point("research")
    workflow.add_edge("research", "writing")
    workflow.add_edge("writing", "seo_optimization")
    workflow.add_edge("seo_optimization", "quality_assurance")
    workflow.add_edge("quality_assurance", END)
    
    # Compile with memory
    memory = MemorySaver()
    app = workflow.compile(checkpointer=memory)
    
    return app

def run_content_pipeline(topic=None, content_type="blog_post"):
    """
    Run the content creation pipeline using LangGraph
    
    Args:
        topic: Optional specific topic to research
        content_type: Type of content to create (blog_post, social_media, website_copy)
    """
    print("Starting LangGraph Content Creation Pipeline...")
    print(f"Content Type: {content_type}")
    if topic:
        print(f"Specific Topic: {topic}")
    
    try:
        # Create the workflow
        app = create_content_workflow()
        
        # Initial state
        initial_state = {
            "topic": topic or "AI automation for small businesses",
            "content_type": content_type,
            "research_data": "",
            "content": "",
            "seo_optimized_content": "",
            "quality_report": "",
            "final_output": ""
        }
        
        # Run the workflow with unique thread ID to prevent caching
        import uuid
        unique_thread_id = f"content_session_{uuid.uuid4().hex[:8]}"
        config = {"configurable": {"thread_id": unique_thread_id}}
        result = app.invoke(initial_state, config)
        
        print("\n" + "="*60)
        print("LANGGRAPH CONTENT CREATION PIPELINE COMPLETED")
        print("="*60)
        print(result["final_output"])
        
        return result
        
    except Exception as e:
        print(f"Error in content creation pipeline: {e}")
        return None

if __name__ == "__main__":
    # Example usage
    result = run_content_pipeline(
        topic="AI automation for small businesses",
        content_type="blog_post"
    )