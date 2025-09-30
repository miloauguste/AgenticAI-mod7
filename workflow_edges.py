"""
Minimal Edge Specification for LangGraph Content Creation Workflow
"""

from langgraph.graph import StateGraph, END

def add_workflow_edges(workflow: StateGraph):
    """
    Define minimal directional flow edges for the workflow
    """
    
    # =============================================================================
    # SEQUENTIAL EDGES (Direct transitions)
    # =============================================================================
    
    workflow.add_edge("initialize_workflow", "research_agent")
    workflow.add_edge("research_agent", "analyze_research")
    workflow.add_edge("content_planning", "content_writing")
    workflow.add_edge("content_writing", "content_review")
    workflow.add_edge("seo_optimization", "quality_assurance")
    workflow.add_edge("revision_planning", "content_revision")
    workflow.add_edge("content_revision", "content_review")
    workflow.add_edge("final_assembly", "workflow_completion")
    workflow.add_edge("workflow_completion", END)
    workflow.add_edge("error_handling", END)
    
    # =============================================================================
    # CONDITIONAL EDGES (Decision-based routing)
    # =============================================================================
    
    # Research Analysis Decision Point
    workflow.add_conditional_edges(
        "analyze_research",
        decide_research_next,
        {
            "proceed": "content_planning",
            "retry": "research_agent", 
            "error": "error_handling"
        }
    )
    
    # Content Review Decision Point
    workflow.add_conditional_edges(
        "content_review",
        decide_content_next,
        {
            "seo": "seo_optimization",
            "revise": "content_revision",
            "error": "error_handling"
        }
    )
    
    # Quality Assurance Decision Point
    workflow.add_conditional_edges(
        "quality_assurance",
        decide_quality_next,
        {
            "finalize": "final_assembly",
            "revise": "revision_planning",
            "error": "error_handling"
        }
    )

# =============================================================================
# DECISION FUNCTIONS
# =============================================================================

def decide_research_next(state) -> str:
    """Research routing decision"""
    if state.error_messages:
        return "error"
    elif state.research_confidence >= 0.3 and state.agent_iterations.get("research", 0) < 2:
        return "proceed" if state.research_confidence >= 0.6 else "retry"
    else:
        return "error"

def decide_content_next(state) -> str:
    """Content routing decision"""
    if state.error_messages or not state.draft_content:
        return "error"
    elif state.word_count >= 200:
        return "seo"
    elif state.revision_count < 2:
        return "revise"
    else:
        return "error"

def decide_quality_next(state) -> str:
    """Quality routing decision"""
    if state.error_messages:
        return "error"
    elif state.quality_score >= 80:
        return "finalize"
    elif state.quality_score >= 60 and state.revision_count < 2:
        return "revise"
    else:
        return "error"

# =============================================================================
# WORKFLOW GRAPH STRUCTURE
# =============================================================================

"""
Directional Flow:

START
  ↓
initialize_workflow
  ↓
research_agent
  ↓
analyze_research
  ↓ (conditional)
  ├─→ content_planning (if research_confidence >= 0.6)
  ├─→ research_agent (if 0.3 <= confidence < 0.6, iterations < 2)
  └─→ error_handling (if confidence < 0.3 or max iterations)
      ↓
content_writing
  ↓
content_review
  ↓ (conditional)
  ├─→ seo_optimization (if content ok)
  ├─→ content_revision (if needs revision, revisions < 2)
  └─→ error_handling (if failed or max revisions)
      ↓
      └─→ content_review (revision loop)
          ↓
quality_assurance
  ↓ (conditional)
  ├─→ final_assembly (if quality >= 80)
  ├─→ revision_planning (if 60 <= quality < 80, revisions < 2)
  └─→ error_handling (if quality < 60 or max revisions)
      ↓
      └─→ content_revision → content_review (revision cycle)
          ↓
workflow_completion
  ↓
END

Error paths: Any node → error_handling → END
"""