"""
LangGraph-based Content Creation Workflow for Innovate Marketing Solutions
"""
import os
from typing import Dict, Any, List
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain.schema import BaseMessage, HumanMessage, AIMessage
from dotenv import load_dotenv
from research_tool import research_tool
from writing_tool import writing_tool
from SEO_tool import seo_tool

load_dotenv()

class ContentCreationState:
    """State management for the content creation workflow"""
    def __init__(self):
        self.topic: str = ""
        self.research_data: Dict[str, Any] = {}
        self.content: str = ""
        self.seo_optimized_content: str = ""
        self.quality_score: float = 0.0
        self.feedback: List[str] = []
        self.final_content: str = ""
        self.metadata: Dict[str, Any] = {}

def research_node(state: ContentCreationState) -> ContentCreationState:
    """Research trending topics and gather relevant information"""
    print("🔍 Starting research phase...")
    
    try:
        # Use the research tool to gather information
        search_query = f"{state.topic} technology startups digital marketing trends"
        research_results = research_tool.run(search_query)
        
        state.research_data = {
            "search_results": research_results,
            "topic": state.topic,
            "keywords": ["AI", "automation", "startups", "digital marketing", "technology"],
            "content_angles": [
                "Benefits for small businesses",
                "Implementation challenges",
                "Cost-effectiveness",
                "Future trends"
            ]
        }
        
        print(f"✅ Research completed. Found {len(research_results) if isinstance(research_results, list) else 1} sources")
        
    except Exception as e:
        print(f"❌ Research error: {e}")
        state.research_data = {"error": str(e)}
    
    return state

def content_creation_node(state: ContentCreationState) -> ContentCreationState:
    """Generate content based on research findings"""
    print("✍️ Starting content creation phase...")
    
    try:
        # Prepare research data for content creation
        research_summary = str(state.research_data)
        
        # Use the writing tool to generate content
        content = writing_tool.run(research_summary)
        
        state.content = content
        state.metadata.update({
            "word_count": len(content.split()) if isinstance(content, str) else 0,
            "creation_timestamp": "2024-01-01"  # Would use actual timestamp
        })
        
        print(f"✅ Content created. Word count: {state.metadata.get('word_count', 0)}")
        
    except Exception as e:
        print(f"❌ Content creation error: {e}")
        state.content = f"Error generating content: {e}"
    
    return state

def seo_optimization_node(state: ContentCreationState) -> ContentCreationState:
    """Optimize content for search engines"""
    print("🔍 Starting SEO optimization phase...")
    
    try:
        # Extract keywords from research data
        keywords = ", ".join(state.research_data.get("keywords", []))
        
        # Use SEO tool to optimize content
        optimized_content = seo_tool.run(state.content, keywords)
        
        state.seo_optimized_content = optimized_content
        state.metadata.update({
            "seo_keywords": keywords,
            "optimization_applied": True
        })
        
        print("✅ SEO optimization completed")
        
    except Exception as e:
        print(f"❌ SEO optimization error: {e}")
        state.seo_optimized_content = state.content
    
    return state

def quality_assurance_node(state: ContentCreationState) -> ContentCreationState:
    """Review and assess content quality"""
    print("✅ Starting quality assurance phase...")
    
    try:
        content_to_review = state.seo_optimized_content or state.content
        
        # Quality checks
        quality_issues = []
        
        # Check word count
        word_count = len(content_to_review.split())
        if word_count < 300:
            quality_issues.append("Content is too short")
        
        # Check for complete sentences
        if content_to_review.count('.') < 3:
            quality_issues.append("Needs more complete sentences")
        
        # Check for tech keywords
        tech_keywords = ['ai', 'technology', 'digital', 'startup', 'automation']
        if not any(keyword in content_to_review.lower() for keyword in tech_keywords):
            quality_issues.append("Missing relevant tech keywords")
        
        # Calculate quality score
        max_score = 100
        deductions = len(quality_issues) * 20
        quality_score = max(0, max_score - deductions)
        
        state.quality_score = quality_score
        state.feedback = quality_issues
        
        if quality_score >= 80:
            state.final_content = content_to_review
            print(f"✅ Quality check passed with score: {quality_score}/100")
        else:
            print(f"⚠️ Quality issues found. Score: {quality_score}/100")
            print(f"Issues: {'; '.join(quality_issues)}")
        
        state.metadata.update({
            "quality_score": quality_score,
            "quality_issues": quality_issues
        })
        
    except Exception as e:
        print(f"❌ Quality assurance error: {e}")
        state.quality_score = 0
        state.feedback = [f"QA error: {e}"]
    
    return state

def should_revise(state: ContentCreationState) -> str:
    """Determine if content needs revision based on quality score"""
    if state.quality_score >= 80:
        return "finalize"
    else:
        return "revise"

def revision_node(state: ContentCreationState) -> ContentCreationState:
    """Revise content based on quality feedback"""
    print("🔄 Starting content revision...")
    
    try:
        # Create revision prompt based on feedback
        revision_prompt = f"""
        Please revise the following content based on these quality issues:
        {'; '.join(state.feedback)}
        
        Original content:
        {state.content}
        
        Please address the issues and improve the content quality.
        """
        
        # Use writing tool for revision
        revised_content = writing_tool.run(revision_prompt)
        state.content = revised_content
        
        print("✅ Content revision completed")
        
    except Exception as e:
        print(f"❌ Revision error: {e}")
    
    return state

def finalize_node(state: ContentCreationState) -> ContentCreationState:
    """Finalize the content creation process"""
    print("🎯 Finalizing content...")
    
    state.final_content = state.seo_optimized_content or state.content
    state.metadata.update({
        "status": "completed",
        "final_word_count": len(state.final_content.split()),
        "quality_score": state.quality_score
    })
    
    print("✅ Content creation workflow completed!")
    return state

def create_content_workflow():
    """Create the LangGraph workflow for content creation"""
    workflow = StateGraph(ContentCreationState)
    
    # Add nodes
    workflow.add_node("research", research_node)
    workflow.add_node("content_creation", content_creation_node)
    workflow.add_node("seo_optimization", seo_optimization_node)
    workflow.add_node("quality_assurance", quality_assurance_node)
    workflow.add_node("revision", revision_node)
    workflow.add_node("finalize", finalize_node)
    
    # Define edges
    workflow.set_entry_point("research")
    workflow.add_edge("research", "content_creation")
    workflow.add_edge("content_creation", "seo_optimization")
    workflow.add_edge("seo_optimization", "quality_assurance")
    
    # Conditional edge based on quality score
    workflow.add_conditional_edges(
        "quality_assurance",
        should_revise,
        {
            "revise": "revision",
            "finalize": "finalize"
        }
    )
    
    # After revision, go back to SEO optimization
    workflow.add_edge("revision", "seo_optimization")
    workflow.add_edge("finalize", END)
    
    return workflow.compile()

def run_langgraph_pipeline(topic: str = "AI automation for small businesses") -> Dict[str, Any]:
    """
    Run the LangGraph content creation pipeline
    
    Args:
        topic: The topic to create content about
        
    Returns:
        Dictionary containing the final content and metadata
    """
    print("🚀 Starting LangGraph Content Creation Pipeline...")
    print(f"Topic: {topic}")
    print("="*60)
    
    # Initialize state
    initial_state = ContentCreationState()
    initial_state.topic = topic
    
    # Create and run workflow
    workflow = create_content_workflow()
    
    try:
        # Execute the workflow
        final_state = workflow.invoke(initial_state)
        
        print("\n" + "="*60)
        print("✅ LANGGRAPH PIPELINE COMPLETED")
        print("="*60)
        
        return {
            "final_content": final_state.final_content,
            "metadata": final_state.metadata,
            "quality_score": final_state.quality_score,
            "feedback": final_state.feedback
        }
        
    except Exception as e:
        print(f"❌ Pipeline error: {e}")
        return {"error": str(e)}

if __name__ == "__main__":
    # Example usage
    result = run_langgraph_pipeline("AI automation for small businesses")
    
    if "error" not in result:
        print(f"\nFinal Content:\n{result['final_content']}")
        print(f"\nQuality Score: {result['quality_score']}/100")
        print(f"Word Count: {result['metadata'].get('final_word_count', 0)}")