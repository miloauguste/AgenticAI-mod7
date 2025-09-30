"""
Enhanced Workflow Integration with State Handoff Management
Complete integration of LangGraph workflow with comprehensive state management
"""

import os
import json
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
from dataclasses import dataclass, field

from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from langchain_openai import ChatOpenAI

from state_handoff_manager import StateHandoffManager, HandoffStatus, StateHandoffRecord
from enhanced_agents import AdvancedContentAgents
from enhanced_agents_part2 import AdvancedContentAgentsPart2
from enhanced_agents_part3 import AdvancedContentAgentsPart3
from config import Config

# Enhanced State Class with comprehensive tracking
@dataclass
class EnhancedContentCreationState:
    """
    Enhanced state management with comprehensive tracking and validation
    """
    # Input Parameters
    topic: str = ""
    content_type: str = "blog_post"
    target_audience: str = ""
    specific_keywords: List[str] = field(default_factory=list)
    
    # Research Phase Data
    research_query: str = ""
    search_results: List[Dict[str, Any]] = field(default_factory=list)
    trending_topics: List[str] = field(default_factory=list)
    extracted_keywords: List[str] = field(default_factory=list)
    research_summary: str = ""
    research_confidence: float = 0.0
    
    # Content Creation Data
    content_outline: str = ""
    draft_content: str = ""
    content_sections: List[Dict[str, str]] = field(default_factory=list)
    writing_style: str = "professional"
    word_count: int = 0
    
    # SEO Optimization Data
    primary_keywords: List[str] = field(default_factory=list)
    meta_description: str = ""
    title_suggestions: List[str] = field(default_factory=list)
    seo_score: float = 0.0
    optimized_content: str = ""
    
    # Quality Assurance Data
    quality_checks: Dict[str, bool] = field(default_factory=dict)
    quality_score: float = 0.0
    quality_feedback: List[str] = field(default_factory=list)
    revision_needed: bool = False
    revision_count: int = 0
    
    # Final Output
    final_content: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    # Workflow Control and Monitoring
    current_agent: str = ""
    workflow_stage: str = "initialized"
    error_messages: List[str] = field(default_factory=list)
    completion_timestamp: Optional[str] = None
    
    # Performance Metrics
    processing_time: Dict[str, float] = field(default_factory=dict)
    agent_iterations: Dict[str, int] = field(default_factory=dict)
    
    # State Handoff Tracking
    handoff_history: List[Dict[str, Any]] = field(default_factory=list)
    state_checksums: Dict[str, str] = field(default_factory=dict)
    validation_results: Dict[str, Any] = field(default_factory=dict)
    
    # Recovery and Rollback Data
    state_snapshots: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    rollback_points: List[str] = field(default_factory=list)

class EnhancedWorkflowOrchestrator:
    """
    Enhanced workflow orchestrator with comprehensive state handoff management
    """
    
    def __init__(self):
        self.llm = ChatOpenAI(temperature=0.7, model="gpt-3.5-turbo")
        self.memory = MemorySaver()
        
        # Initialize agent implementations
        self.agents_part1 = AdvancedContentAgents()
        self.agents_part2 = AdvancedContentAgentsPart2() 
        self.agents_part3 = AdvancedContentAgentsPart3()
        
        # Initialize state handoff manager
        self.handoff_manager = StateHandoffManager()
        
        # Build the enhanced workflow graph
        self.graph = self._build_enhanced_workflow_graph()
        
        # Performance monitoring
        self.workflow_metrics = {
            "total_executions": 0,
            "successful_executions": 0,
            "average_processing_time": 0.0,
            "error_rate": 0.0
        }
    
    def _build_enhanced_workflow_graph(self) -> StateGraph:
        """Build the enhanced workflow graph with state handoff management"""
        
        workflow = StateGraph(EnhancedContentCreationState)
        
        # Add all workflow nodes with enhanced handoff management
        workflow.add_node("initialize_workflow", self._enhanced_initialize_workflow)
        workflow.add_node("research_agent", self._enhanced_research_agent)
        workflow.add_node("analyze_research", self._enhanced_analyze_research)
        workflow.add_node("content_planning", self._enhanced_content_planning)
        workflow.add_node("content_writing", self._enhanced_content_writing)
        workflow.add_node("content_review", self._enhanced_content_review)
        workflow.add_node("seo_optimization", self._enhanced_seo_optimization)
        workflow.add_node("quality_assurance", self._enhanced_quality_assurance)
        workflow.add_node("revision_planning", self._enhanced_revision_planning)
        workflow.add_node("content_revision", self._enhanced_content_revision)
        workflow.add_node("final_assembly", self._enhanced_final_assembly)
        workflow.add_node("workflow_completion", self._enhanced_workflow_completion)
        workflow.add_node("error_handling", self._enhanced_error_handling)
        
        # Define enhanced workflow transitions with handoff management
        self._add_enhanced_workflow_transitions(workflow)
        
        # Set entry point
        workflow.set_entry_point("initialize_workflow")
        
        return workflow.compile(checkpointer=self.memory)
    
    def _add_enhanced_workflow_transitions(self, workflow: StateGraph) -> None:
        """Add workflow transitions with enhanced handoff management"""
        
        # Sequential workflow transitions
        workflow.add_edge("initialize_workflow", "research_agent")
        workflow.add_edge("research_agent", "analyze_research")
        
        # Conditional transition from research analysis
        workflow.add_conditional_edges(
            "analyze_research",
            self._enhanced_decide_research_next_step,
            {
                "proceed_to_planning": "content_planning",
                "retry_research": "research_agent",
                "handle_error": "error_handling"
            }
        )
        
        workflow.add_edge("content_planning", "content_writing")
        workflow.add_edge("content_writing", "content_review")
        
        # Conditional transition from content review
        workflow.add_conditional_edges(
            "content_review",
            self._enhanced_decide_content_next_step,
            {
                "proceed_to_seo": "seo_optimization",
                "revise_content": "content_revision",
                "handle_error": "error_handling"
            }
        )
        
        workflow.add_edge("content_revision", "content_review")
        workflow.add_edge("seo_optimization", "quality_assurance")
        
        # Conditional transition from quality assurance
        workflow.add_conditional_edges(
            "quality_assurance",
            self._enhanced_decide_quality_next_step,
            {
                "finalize_content": "final_assembly",
                "plan_revision": "revision_planning",
                "handle_error": "error_handling"
            }
        )
        
        workflow.add_edge("revision_planning", "content_revision")
        workflow.add_edge("final_assembly", "workflow_completion")
        workflow.add_edge("workflow_completion", END)
        workflow.add_edge("error_handling", END)

    # =============================================================================
    # ENHANCED NODE IMPLEMENTATIONS WITH HANDOFF MANAGEMENT
    # =============================================================================
    
    def _enhanced_initialize_workflow(self, state: EnhancedContentCreationState) -> EnhancedContentCreationState:
        """Enhanced initialize workflow with state handoff management"""
        
        print("🚀 ENHANCED INITIALIZE WORKFLOW WITH HANDOFF MANAGEMENT")
        
        # Create rollback point
        self._create_rollback_point(state, "pre_initialization")
        
        # Execute the initialization with handoff management
        try:
            # Run the enhanced initialization
            enhanced_state = self.agents_part1.initialize_workflow_enhanced(state)
            
            # Record successful initialization
            enhanced_state.workflow_stage = "initialization_complete"
            enhanced_state.rollback_points.append("initialization_complete")
            
            print("✅ Enhanced initialization completed successfully")
            return enhanced_state
            
        except Exception as e:
            print(f"❌ Enhanced initialization failed: {e}")
            state.error_messages.append(f"Initialization error: {e}")
            return self._handle_node_failure(state, "initialize_workflow", e)
    
    def _enhanced_research_agent(self, state: EnhancedContentCreationState) -> EnhancedContentCreationState:
        """Enhanced research agent with state handoff management"""
        
        print("🔍 ENHANCED RESEARCH AGENT WITH HANDOFF MANAGEMENT")
        
        # Execute handoff from previous node
        state, handoff_record = self.handoff_manager.execute_handoff(
            state, "initialize_workflow", "research_agent"
        )
        
        if handoff_record.status == HandoffStatus.FAILURE:
            return self._handle_handoff_failure(state, handoff_record)
        
        # Create rollback point
        self._create_rollback_point(state, "pre_research")
        
        try:
            # Execute enhanced research
            enhanced_state = self.agents_part1.research_agent_enhanced(state)
            
            # Validate research results
            if self._validate_research_results(enhanced_state):
                enhanced_state.rollback_points.append("research_complete")
                print("✅ Enhanced research completed successfully")
                return enhanced_state
            else:
                print("⚠️ Research validation failed, attempting recovery")
                return self._attempt_research_recovery(enhanced_state)
                
        except Exception as e:
            print(f"❌ Enhanced research failed: {e}")
            return self._handle_node_failure(state, "research_agent", e)
    
    def _enhanced_analyze_research(self, state: EnhancedContentCreationState) -> EnhancedContentCreationState:
        """Enhanced analyze research with state handoff management"""
        
        print("📊 ENHANCED ANALYZE RESEARCH WITH HANDOFF MANAGEMENT")
        
        # Execute handoff from research agent
        state, handoff_record = self.handoff_manager.execute_handoff(
            state, "research_agent", "analyze_research"
        )
        
        if handoff_record.status == HandoffStatus.FAILURE:
            return self._handle_handoff_failure(state, handoff_record)
        
        try:
            # Execute enhanced analysis
            enhanced_state = self.agents_part1.analyze_research_enhanced(state)
            
            # Validate analysis results
            if self._validate_analysis_results(enhanced_state):
                enhanced_state.rollback_points.append("analysis_complete")
                print("✅ Enhanced research analysis completed successfully")
                return enhanced_state
            else:
                print("⚠️ Analysis validation failed")
                enhanced_state.error_messages.append("Research analysis validation failed")
                return enhanced_state
                
        except Exception as e:
            print(f"❌ Enhanced analysis failed: {e}")
            return self._handle_node_failure(state, "analyze_research", e)
    
    def _enhanced_content_planning(self, state: EnhancedContentCreationState) -> EnhancedContentCreationState:
        """Enhanced content planning with state handoff management"""
        
        print("📋 ENHANCED CONTENT PLANNING WITH HANDOFF MANAGEMENT")
        
        # Execute handoff from analyze research
        state, handoff_record = self.handoff_manager.execute_handoff(
            state, "analyze_research", "content_planning"
        )
        
        if handoff_record.status == HandoffStatus.FAILURE:
            return self._handle_handoff_failure(state, handoff_record)
        
        try:
            # Execute enhanced planning
            enhanced_state = self.agents_part1.content_planning_enhanced(state)
            
            # Validate planning results
            if self._validate_planning_results(enhanced_state):
                enhanced_state.rollback_points.append("planning_complete")
                print("✅ Enhanced content planning completed successfully")
                return enhanced_state
            else:
                print("⚠️ Planning validation failed")
                enhanced_state.error_messages.append("Content planning validation failed")
                return enhanced_state
                
        except Exception as e:
            print(f"❌ Enhanced planning failed: {e}")
            return self._handle_node_failure(state, "content_planning", e)
    
    def _enhanced_content_writing(self, state: EnhancedContentCreationState) -> EnhancedContentCreationState:
        """Enhanced content writing with state handoff management"""
        
        print("✍️ ENHANCED CONTENT WRITING WITH HANDOFF MANAGEMENT")
        
        # Execute handoff from content planning
        state, handoff_record = self.handoff_manager.execute_handoff(
            state, "content_planning", "content_writing"
        )
        
        if handoff_record.status == HandoffStatus.FAILURE:
            return self._handle_handoff_failure(state, handoff_record)
        
        # Create rollback point before intensive operation
        self._create_rollback_point(state, "pre_writing")
        
        try:
            # Execute enhanced writing
            enhanced_state = self.agents_part2.content_writing_enhanced(state)
            
            # Validate writing results
            if self._validate_writing_results(enhanced_state):
                enhanced_state.rollback_points.append("writing_complete")
                print("✅ Enhanced content writing completed successfully")
                return enhanced_state
            else:
                print("⚠️ Writing validation failed, attempting recovery")
                return self._attempt_writing_recovery(enhanced_state)
                
        except Exception as e:
            print(f"❌ Enhanced writing failed: {e}")
            return self._handle_node_failure(state, "content_writing", e)
    
    def _enhanced_content_review(self, state: EnhancedContentCreationState) -> EnhancedContentCreationState:
        """Enhanced content review with state handoff management"""
        
        print("📖 ENHANCED CONTENT REVIEW WITH HANDOFF MANAGEMENT")
        
        # Execute handoff from content writing or content revision
        source_node = "content_revision" if state.revision_count > 0 else "content_writing"
        state, handoff_record = self.handoff_manager.execute_handoff(
            state, source_node, "content_review"
        )
        
        if handoff_record.status == HandoffStatus.FAILURE:
            return self._handle_handoff_failure(state, handoff_record)
        
        try:
            # Execute enhanced review
            enhanced_state = self.agents_part2.content_review_enhanced(state)
            
            # Validate review results
            if self._validate_review_results(enhanced_state):
                enhanced_state.rollback_points.append("review_complete")
                print("✅ Enhanced content review completed successfully")
                return enhanced_state
            else:
                print("⚠️ Review validation failed")
                enhanced_state.error_messages.append("Content review validation failed")
                return enhanced_state
                
        except Exception as e:
            print(f"❌ Enhanced review failed: {e}")
            return self._handle_node_failure(state, "content_review", e)
    
    def _enhanced_seo_optimization(self, state: EnhancedContentCreationState) -> EnhancedContentCreationState:
        """Enhanced SEO optimization with state handoff management"""
        
        print("🔍 ENHANCED SEO OPTIMIZATION WITH HANDOFF MANAGEMENT")
        
        # Execute handoff from content review
        state, handoff_record = self.handoff_manager.execute_handoff(
            state, "content_review", "seo_optimization"
        )
        
        if handoff_record.status == HandoffStatus.FAILURE:
            return self._handle_handoff_failure(state, handoff_record)
        
        try:
            # Execute enhanced SEO optimization
            enhanced_state = self.agents_part3.seo_optimization_enhanced(state)
            
            # Validate SEO results
            if self._validate_seo_results(enhanced_state):
                enhanced_state.rollback_points.append("seo_complete")
                print("✅ Enhanced SEO optimization completed successfully")
                return enhanced_state
            else:
                print("⚠️ SEO validation failed")
                enhanced_state.error_messages.append("SEO optimization validation failed")
                return enhanced_state
                
        except Exception as e:
            print(f"❌ Enhanced SEO optimization failed: {e}")
            return self._handle_node_failure(state, "seo_optimization", e)
    
    def _enhanced_quality_assurance(self, state: EnhancedContentCreationState) -> EnhancedContentCreationState:
        """Enhanced quality assurance with state handoff management"""
        
        print("✅ ENHANCED QUALITY ASSURANCE WITH HANDOFF MANAGEMENT")
        
        # Execute handoff from SEO optimization
        state, handoff_record = self.handoff_manager.execute_handoff(
            state, "seo_optimization", "quality_assurance"
        )
        
        if handoff_record.status == HandoffStatus.FAILURE:
            return self._handle_handoff_failure(state, handoff_record)
        
        try:
            # Execute enhanced quality assurance (implement this method in part 3)
            # For now, use a simplified QA approach
            enhanced_state = self._execute_enhanced_quality_assurance(state)
            
            # Validate QA results
            if self._validate_qa_results(enhanced_state):
                enhanced_state.rollback_points.append("qa_complete")
                print("✅ Enhanced quality assurance completed successfully")
                return enhanced_state
            else:
                print("⚠️ QA validation failed")
                enhanced_state.error_messages.append("Quality assurance validation failed")
                return enhanced_state
                
        except Exception as e:
            print(f"❌ Enhanced quality assurance failed: {e}")
            return self._handle_node_failure(state, "quality_assurance", e)
    
    def _enhanced_revision_planning(self, state: EnhancedContentCreationState) -> EnhancedContentCreationState:
        """Enhanced revision planning with state handoff management"""
        
        print("🔄 ENHANCED REVISION PLANNING WITH HANDOFF MANAGEMENT")
        
        # Execute handoff from quality assurance
        state, handoff_record = self.handoff_manager.execute_handoff(
            state, "quality_assurance", "revision_planning"
        )
        
        if handoff_record.status == HandoffStatus.FAILURE:
            return self._handle_handoff_failure(state, handoff_record)
        
        try:
            # Execute enhanced revision planning
            enhanced_state = self._execute_enhanced_revision_planning(state)
            
            enhanced_state.rollback_points.append("revision_planning_complete")
            print("✅ Enhanced revision planning completed successfully")
            return enhanced_state
            
        except Exception as e:
            print(f"❌ Enhanced revision planning failed: {e}")
            return self._handle_node_failure(state, "revision_planning", e)
    
    def _enhanced_content_revision(self, state: EnhancedContentCreationState) -> EnhancedContentCreationState:
        """Enhanced content revision with state handoff management"""
        
        print("✏️ ENHANCED CONTENT REVISION WITH HANDOFF MANAGEMENT")
        
        # Execute handoff from revision planning
        state, handoff_record = self.handoff_manager.execute_handoff(
            state, "revision_planning", "content_revision"
        )
        
        if handoff_record.status == HandoffStatus.FAILURE:
            return self._handle_handoff_failure(state, handoff_record)
        
        try:
            # Execute enhanced content revision
            enhanced_state = self._execute_enhanced_content_revision(state)
            
            enhanced_state.rollback_points.append("revision_complete")
            print("✅ Enhanced content revision completed successfully")
            return enhanced_state
            
        except Exception as e:
            print(f"❌ Enhanced content revision failed: {e}")
            return self._handle_node_failure(state, "content_revision", e)
    
    def _enhanced_final_assembly(self, state: EnhancedContentCreationState) -> EnhancedContentCreationState:
        """Enhanced final assembly with state handoff management"""
        
        print("📦 ENHANCED FINAL ASSEMBLY WITH HANDOFF MANAGEMENT")
        
        # Execute handoff from quality assurance
        state, handoff_record = self.handoff_manager.execute_handoff(
            state, "quality_assurance", "final_assembly"
        )
        
        if handoff_record.status == HandoffStatus.FAILURE:
            return self._handle_handoff_failure(state, handoff_record)
        
        try:
            # Execute enhanced final assembly
            enhanced_state = self._execute_enhanced_final_assembly(state)
            
            enhanced_state.rollback_points.append("assembly_complete")
            print("✅ Enhanced final assembly completed successfully")
            return enhanced_state
            
        except Exception as e:
            print(f"❌ Enhanced final assembly failed: {e}")
            return self._handle_node_failure(state, "final_assembly", e)
    
    def _enhanced_workflow_completion(self, state: EnhancedContentCreationState) -> EnhancedContentCreationState:
        """Enhanced workflow completion with state handoff management"""
        
        print("🎉 ENHANCED WORKFLOW COMPLETION WITH HANDOFF MANAGEMENT")
        
        # Execute handoff from final assembly
        state, handoff_record = self.handoff_manager.execute_handoff(
            state, "final_assembly", "workflow_completion"
        )
        
        if handoff_record.status == HandoffStatus.FAILURE:
            return self._handle_handoff_failure(state, handoff_record)
        
        try:
            # Execute enhanced workflow completion
            enhanced_state = self._execute_enhanced_workflow_completion(state)
            
            # Update workflow metrics
            self._update_workflow_metrics(enhanced_state, success=True)
            
            print("✅ Enhanced workflow completion finished successfully")
            return enhanced_state
            
        except Exception as e:
            print(f"❌ Enhanced workflow completion failed: {e}")
            return self._handle_node_failure(state, "workflow_completion", e)
    
    def _enhanced_error_handling(self, state: EnhancedContentCreationState) -> EnhancedContentCreationState:
        """Enhanced error handling with state handoff management"""
        
        print("❌ ENHANCED ERROR HANDLING WITH HANDOFF MANAGEMENT")
        
        try:
            # Execute enhanced error handling
            enhanced_state = self._execute_enhanced_error_handling(state)
            
            # Update workflow metrics
            self._update_workflow_metrics(enhanced_state, success=False)
            
            print("✅ Enhanced error handling completed")
            return enhanced_state
            
        except Exception as e:
            print(f"❌ Error handling itself failed: {e}")
            state.error_messages.append(f"Error handling failure: {e}")
            return state

    # =============================================================================
    # ENHANCED CONDITIONAL DECISION FUNCTIONS
    # =============================================================================
    
    def _enhanced_decide_research_next_step(self, state: EnhancedContentCreationState) -> str:
        """Enhanced decision function for research workflow"""
        
        # Check for critical errors first
        if state.error_messages:
            return "handle_error"
        
        # Check research quality with enhanced criteria
        research_confidence = getattr(state, 'research_confidence', 0.0)
        research_iterations = state.agent_iterations.get("research", 0)
        
        # More sophisticated decision logic
        if research_confidence >= 0.7:
            return "proceed_to_planning"
        elif research_confidence >= 0.4 and research_iterations < 2:
            print(f"🔄 Research confidence {research_confidence:.2f} below optimal, retrying...")
            return "retry_research"
        elif research_confidence >= 0.3:
            print(f"⚠️ Research confidence {research_confidence:.2f} marginal, proceeding with caution...")
            return "proceed_to_planning"
        else:
            print(f"❌ Research confidence {research_confidence:.2f} too low, handling as error")
            return "handle_error"
    
    def _enhanced_decide_content_next_step(self, state: EnhancedContentCreationState) -> str:
        """Enhanced decision function for content workflow"""
        
        # Check for critical errors
        if state.error_messages:
            return "handle_error"
        
        # Enhanced content quality assessment
        word_count = getattr(state, 'word_count', 0)
        content_quality = self._assess_content_quality(state)
        
        if word_count >= 200 and content_quality >= 0.7:
            return "proceed_to_seo"
        elif content_quality >= 0.5 and state.revision_count < 2:
            print(f"🔄 Content quality {content_quality:.2f} needs improvement, revising...")
            return "revise_content"
        else:
            print(f"❌ Content quality {content_quality:.2f} insufficient, handling as error")
            return "handle_error"
    
    def _enhanced_decide_quality_next_step(self, state: EnhancedContentCreationState) -> str:
        """Enhanced decision function for quality assurance workflow"""
        
        # Check for critical errors
        if state.error_messages:
            return "handle_error"
        
        # Enhanced quality decision logic
        quality_score = getattr(state, 'quality_score', 0.0)
        revision_count = getattr(state, 'revision_count', 0)
        seo_score = getattr(state, 'seo_score', 0.0)
        
        # Comprehensive quality assessment
        overall_readiness = (quality_score * 0.6) + (seo_score * 0.4)
        
        if overall_readiness >= 80.0:
            return "finalize_content"
        elif overall_readiness >= 60.0 and revision_count < 2:
            print(f"🔄 Overall readiness {overall_readiness:.1f} needs improvement, planning revision...")
            return "plan_revision"
        else:
            print(f"❌ Overall readiness {overall_readiness:.1f} insufficient after {revision_count} revisions")
            return "handle_error"

    # =============================================================================
    # VALIDATION AND RECOVERY METHODS
    # =============================================================================
    
    def _validate_research_results(self, state: EnhancedContentCreationState) -> bool:
        """Validate research results"""
        return (
            hasattr(state, 'research_confidence') and state.research_confidence > 0.0 and
            hasattr(state, 'search_results') and len(state.search_results) > 0 and
            hasattr(state, 'extracted_keywords') and len(state.extracted_keywords) > 0
        )
    
    def _validate_analysis_results(self, state: EnhancedContentCreationState) -> bool:
        """Validate analysis results"""
        return (
            hasattr(state, 'trending_topics') and
            state.metadata and 
            "research_assessment" in state.metadata
        )
    
    def _validate_planning_results(self, state: EnhancedContentCreationState) -> bool:
        """Validate planning results"""
        return (
            hasattr(state, 'content_outline') and len(state.content_outline) > 50 and
            hasattr(state, 'content_sections') and len(state.content_sections) > 0 and
            hasattr(state, 'primary_keywords') and len(state.primary_keywords) > 0
        )
    
    def _validate_writing_results(self, state: EnhancedContentCreationState) -> bool:
        """Validate writing results"""
        return (
            hasattr(state, 'draft_content') and len(state.draft_content) > 100 and
            hasattr(state, 'word_count') and state.word_count > 50
        )
    
    def _validate_review_results(self, state: EnhancedContentCreationState) -> bool:
        """Validate review results"""
        return (
            state.metadata and 
            "content_analysis" in state.metadata
        )
    
    def _validate_seo_results(self, state: EnhancedContentCreationState) -> bool:
        """Validate SEO results"""
        return (
            hasattr(state, 'seo_score') and state.seo_score > 0 and
            hasattr(state, 'meta_description') and len(state.meta_description) > 100
        )
    
    def _validate_qa_results(self, state: EnhancedContentCreationState) -> bool:
        """Validate QA results"""
        return (
            hasattr(state, 'quality_score') and state.quality_score > 0 and
            hasattr(state, 'quality_checks')
        )
    
    def _assess_content_quality(self, state: EnhancedContentCreationState) -> float:
        """Assess overall content quality"""
        
        quality_factors = []
        
        # Word count factor
        word_count = getattr(state, 'word_count', 0)
        if word_count >= 500:
            quality_factors.append(1.0)
        elif word_count >= 300:
            quality_factors.append(0.8)
        elif word_count >= 100:
            quality_factors.append(0.6)
        else:
            quality_factors.append(0.3)
        
        # Content structure factor
        content = getattr(state, 'draft_content', '')
        if content:
            paragraphs = len([p for p in content.split('\n\n') if p.strip()])
            structure_score = min(1.0, paragraphs / 4.0)  # Optimal: 4+ paragraphs
            quality_factors.append(structure_score)
        
        # Keyword integration factor
        primary_keywords = getattr(state, 'primary_keywords', [])
        if primary_keywords and content:
            keyword_integration = sum(1 for kw in primary_keywords if kw.lower() in content.lower())
            integration_score = min(1.0, keyword_integration / len(primary_keywords))
            quality_factors.append(integration_score)
        
        return sum(quality_factors) / len(quality_factors) if quality_factors else 0.0

    # =============================================================================
    # RECOVERY AND ROLLBACK METHODS
    # =============================================================================
    
    def _create_rollback_point(self, state: EnhancedContentCreationState, point_name: str) -> None:
        """Create a rollback point for state recovery"""
        try:
            # Create a deep copy of the current state
            state_snapshot = {
                "timestamp": datetime.now().isoformat(),
                "stage": state.workflow_stage,
                "content": getattr(state, 'draft_content', ''),
                "metadata": state.metadata.copy() if state.metadata else {},
                "quality_score": getattr(state, 'quality_score', 0.0),
                "error_count": len(state.error_messages)
            }
            
            state.state_snapshots[point_name] = state_snapshot
            print(f"📸 Created rollback point: {point_name}")
            
        except Exception as e:
            print(f"⚠️ Failed to create rollback point {point_name}: {e}")
    
    def _attempt_research_recovery(self, state: EnhancedContentCreationState) -> EnhancedContentCreationState:
        """Attempt to recover from research failures"""
        print("🔄 Attempting research recovery...")
        
        # Try to use existing partial results
        if hasattr(state, 'search_results') and state.search_results:
            # Use what we have and adjust confidence
            state.research_confidence = max(0.4, state.research_confidence)
            state.error_messages.append("Used partial research results due to validation failure")
            return state
        else:
            # Fallback to minimal research data
            state.search_results = [{"title": f"Information about {state.topic}", "snippet": f"Basic information about {state.topic}"}]
            state.extracted_keywords = state.topic.split()[:3]
            state.research_confidence = 0.3
            state.error_messages.append("Used fallback research data due to failure")
            return state
    
    def _attempt_writing_recovery(self, state: EnhancedContentCreationState) -> EnhancedContentCreationState:
        """Attempt to recover from writing failures"""
        print("🔄 Attempting writing recovery...")
        
        # Try to use outline to generate basic content
        if hasattr(state, 'content_outline') and state.content_outline:
            # Generate basic content from outline
            outline_content = f"This content covers {state.topic}.\n\n{state.content_outline}\n\nThis provides valuable insights about {state.topic}."
            state.draft_content = outline_content
            state.word_count = len(outline_content.split())
            state.error_messages.append("Used outline-based content due to writing failure")
            return state
        else:
            # Absolute fallback
            fallback_content = f"This article discusses {state.topic} and its implications. {' '.join(state.primary_keywords or [])} are important considerations."
            state.draft_content = fallback_content
            state.word_count = len(fallback_content.split())
            state.error_messages.append("Used minimal fallback content due to complete writing failure")
            return state
    
    def _handle_node_failure(self, state: EnhancedContentCreationState, node_name: str, error: Exception) -> EnhancedContentCreationState:
        """Handle node execution failures"""
        
        error_message = f"Node '{node_name}' failed: {str(error)}"
        state.error_messages.append(error_message)
        state.workflow_stage = f"{node_name}_failed"
        
        print(f"❌ Node failure handled: {node_name}")
        
        # Try to rollback to last stable state if available
        rollback_attempted = self._attempt_rollback(state, node_name)
        if not rollback_attempted:
            print(f"⚠️ No rollback available for {node_name}, continuing with error state")
        
        return state
    
    def _handle_handoff_failure(self, state: EnhancedContentCreationState, handoff_record: StateHandoffRecord) -> EnhancedContentCreationState:
        """Handle state handoff failures"""
        
        error_message = f"Handoff failed: {handoff_record.source_node} → {handoff_record.target_node}"
        state.error_messages.extend(handoff_record.errors)
        state.error_messages.append(error_message)
        
        print(f"❌ Handoff failure handled: {error_message}")
        
        return state
    
    def _attempt_rollback(self, state: EnhancedContentCreationState, failed_node: str) -> bool:
        """Attempt to rollback to a previous stable state"""
        
        # Find the most recent rollback point
        rollback_points = getattr(state, 'rollback_points', [])
        
        if not rollback_points:
            return False
        
        try:
            latest_rollback = rollback_points[-1]
            snapshot = state.state_snapshots.get(latest_rollback)
            
            if snapshot:
                # Restore key state elements
                state.workflow_stage = snapshot.get("stage", state.workflow_stage)
                if snapshot.get("content"):
                    state.draft_content = snapshot["content"]
                    state.word_count = len(snapshot["content"].split())
                
                state.metadata.update(snapshot.get("metadata", {}))
                
                print(f"🔄 Rolled back to: {latest_rollback}")
                return True
                
        except Exception as e:
            print(f"❌ Rollback failed: {e}")
        
        return False

    # =============================================================================
    # SIMPLIFIED IMPLEMENTATIONS FOR MISSING METHODS
    # =============================================================================
    
    def _execute_enhanced_quality_assurance(self, state: EnhancedContentCreationState) -> EnhancedContentCreationState:
        """Execute enhanced quality assurance (simplified implementation)"""
        
        content = getattr(state, 'optimized_content', '') or getattr(state, 'draft_content', '')
        word_count = len(content.split()) if content else 0
        
        # Simple quality assessment
        quality_score = 50  # Base score
        
        if word_count >= 300:
            quality_score += 20
        if word_count >= 500:
            quality_score += 10
        
        # Check for keywords
        primary_keywords = getattr(state, 'primary_keywords', [])
        if primary_keywords and content:
            keyword_found = sum(1 for kw in primary_keywords if kw.lower() in content.lower())
            quality_score += min(20, keyword_found * 5)
        
        # Check for structure
        if content.count('\n\n') >= 2:  # Multiple paragraphs
            quality_score += 10
        
        state.quality_score = min(100, quality_score)
        state.quality_checks = {"basic_quality": True}
        
        if state.quality_score < 70:
            state.revision_needed = True
            state.quality_feedback = ["Content needs improvement for better quality"]
        
        return state
    
    def _execute_enhanced_revision_planning(self, state: EnhancedContentCreationState) -> EnhancedContentCreationState:
        """Execute enhanced revision planning (simplified implementation)"""
        
        state.revision_count += 1
        
        # Simple revision strategy
        revision_strategy = {
            "revision_number": state.revision_count,
            "focus_areas": ["content_expansion", "keyword_integration"],
            "target_improvement": 15
        }
        
        state.metadata["revision_strategy"] = revision_strategy
        
        return state
    
    def _execute_enhanced_content_revision(self, state: EnhancedContentCreationState) -> EnhancedContentCreationState:
        """Execute enhanced content revision (simplified implementation)"""
        
        # Simple content enhancement
        current_content = getattr(state, 'draft_content', '')
        
        if current_content:
            # Add basic improvements
            enhanced_content = current_content
            
            # Add conclusion if missing
            if not any(word in current_content.lower() for word in ['conclusion', 'summary']):
                enhanced_content += f"\n\nIn conclusion, {state.topic} offers significant value and opportunities."
            
            # Ensure minimum length
            if len(enhanced_content.split()) < 300:
                enhanced_content += f" This comprehensive overview of {state.topic} provides essential insights for implementation and success."
            
            state.draft_content = enhanced_content
            state.word_count = len(enhanced_content.split())
        
        return state
    
    def _execute_enhanced_final_assembly(self, state: EnhancedContentCreationState) -> EnhancedContentCreationState:
        """Execute enhanced final assembly (simplified implementation)"""
        
        # Use the best available content
        final_content = (
            getattr(state, 'optimized_content', '') or 
            getattr(state, 'draft_content', '') or 
            f"Content about {state.topic}"
        )
        
        state.final_content = final_content
        
        # Compile final metadata
        state.metadata.update({
            "final_word_count": len(final_content.split()),
            "final_quality_score": getattr(state, 'quality_score', 0),
            "seo_score": getattr(state, 'seo_score', 0),
            "revision_cycles": getattr(state, 'revision_count', 0),
            "assembly_timestamp": datetime.now().isoformat()
        })
        
        return state
    
    def _execute_enhanced_workflow_completion(self, state: EnhancedContentCreationState) -> EnhancedContentCreationState:
        """Execute enhanced workflow completion (simplified implementation)"""
        
        state.completion_timestamp = datetime.now().isoformat()
        state.workflow_stage = "completed"
        
        # Calculate total processing time
        total_time = sum(state.processing_time.values())
        
        state.metadata.update({
            "completion_status": "success",
            "total_processing_time": total_time,
            "workflow_efficiency": 100 - (len(state.error_messages) * 10)
        })
        
        return state
    
    def _execute_enhanced_error_handling(self, state: EnhancedContentCreationState) -> EnhancedContentCreationState:
        """Execute enhanced error handling (simplified implementation)"""
        
        state.workflow_stage = "error"
        state.completion_timestamp = datetime.now().isoformat()
        
        # Try to provide partial results
        if getattr(state, 'draft_content', ''):
            state.final_content = state.draft_content
            state.metadata["status"] = "completed_with_errors"
        else:
            state.final_content = f"Content generation failed. Topic: {state.topic}"
            state.metadata["status"] = "failed"
        
        state.metadata.update({
            "error_summary": "; ".join(state.error_messages),
            "error_count": len(state.error_messages),
            "partial_completion": bool(getattr(state, 'draft_content', ''))
        })
        
        return state
    
    def _update_workflow_metrics(self, state: EnhancedContentCreationState, success: bool) -> None:
        """Update workflow performance metrics"""
        
        self.workflow_metrics["total_executions"] += 1
        
        if success:
            self.workflow_metrics["successful_executions"] += 1
        
        # Calculate success rate
        total = self.workflow_metrics["total_executions"]
        successful = self.workflow_metrics["successful_executions"]
        
        self.workflow_metrics["error_rate"] = ((total - successful) / total) * 100 if total > 0 else 0
        
        # Calculate average processing time
        if hasattr(state, 'processing_time'):
            total_time = sum(state.processing_time.values())
            current_avg = self.workflow_metrics["average_processing_time"]
            self.workflow_metrics["average_processing_time"] = (current_avg * (total - 1) + total_time) / total

    # =============================================================================
    # MAIN WORKFLOW EXECUTION METHOD
    # =============================================================================
    
    def run_enhanced_workflow(self, 
                            topic: str, 
                            content_type: str = "blog_post",
                            target_audience: str = "",
                            specific_keywords: List[str] = None) -> Dict[str, Any]:
        """
        Execute the enhanced workflow with comprehensive state management
        """
        
        print("="*80)
        print("🚀 STARTING ENHANCED LANGGRAPH WORKFLOW WITH STATE HANDOFF MANAGEMENT")
        print("="*80)
        
        # Initialize enhanced state
        initial_state = EnhancedContentCreationState(
            topic=topic,
            content_type=content_type,
            target_audience=target_audience,
            specific_keywords=specific_keywords or []
        )
        
        try:
            # Execute the enhanced workflow
            config = {"configurable": {"thread_id": f"enhanced_workflow_{datetime.now().timestamp()}"}}
            final_state = self.graph.invoke(initial_state, config)
            
            # Get handoff analytics
            handoff_analytics = self.handoff_manager.get_handoff_analytics()
            
            # Prepare comprehensive results
            return {
                "success": True,
                "final_content": getattr(final_state, 'final_content', ''),
                "quality_score": getattr(final_state, 'quality_score', 0),
                "seo_score": getattr(final_state, 'seo_score', 0),
                "metadata": getattr(final_state, 'metadata', {}),
                "handoff_analytics": handoff_analytics,
                "workflow_metrics": self.workflow_metrics,
                "error_messages": getattr(final_state, 'error_messages', []),
                "rollback_points": getattr(final_state, 'rollback_points', []),
                "state_validation": getattr(final_state, 'validation_results', {})
            }
            
        except Exception as e:
            print(f"❌ Enhanced workflow execution failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "final_content": "Enhanced workflow execution failed",
                "metadata": {"error": str(e), "workflow_type": "enhanced"}
            }

# =============================================================================
# MAIN EXECUTION FUNCTION
# =============================================================================

def run_enhanced_workflow_with_handoffs(topic: str, 
                                       content_type: str = "blog_post",
                                       target_audience: str = "",
                                       specific_keywords: List[str] = None) -> Dict[str, Any]:
    """
    Main function to execute the enhanced workflow with comprehensive state handoff management
    """
    orchestrator = EnhancedWorkflowOrchestrator()
    return orchestrator.run_enhanced_workflow(topic, content_type, target_audience, specific_keywords)

if __name__ == "__main__":
    # Example execution
    result = run_enhanced_workflow_with_handoffs(
        topic="AI automation for small businesses",
        content_type="blog_post",
        target_audience="small business owners and entrepreneurs",
        specific_keywords=["automation", "efficiency", "cost reduction"]
    )
    
    if result["success"]:
        print("\n" + "="*60)
        print("✅ ENHANCED WORKFLOW COMPLETED SUCCESSFULLY")
        print("="*60)
        print(f"Quality Score: {result['quality_score']:.1f}/100")
        print(f"SEO Score: {result['seo_score']:.1f}/100")
        print(f"Handoffs Executed: {result['handoff_analytics'].get('total_handoffs', 0)}")
        print(f"Success Rate: {result['handoff_analytics'].get('success_rate', 0):.2%}")
        print(f"Rollback Points Created: {len(result['rollback_points'])}")
    else:
        print(f"❌ Enhanced workflow failed: {result['error']}")