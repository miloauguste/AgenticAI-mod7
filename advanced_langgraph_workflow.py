"""
Advanced LangGraph Workflow for Innovate Marketing Solutions
Comprehensive directed graph implementation with detailed states and transitions
"""

import os
from typing import Dict, Any, List, Optional, Literal
from dataclasses import dataclass, field
from datetime import datetime
import json

from langgraph.graph import StateGraph, END, START
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_openai import ChatOpenAI

from research_tool import research_tool
from writing_tool import writing_tool
from SEO_tool import seo_tool
from config import Config

# Enhanced State Management
@dataclass
class ContentCreationState:
    """
    Comprehensive state management for the content creation workflow
    Each field represents data that flows between agents
    """
    # Input Parameters
    topic: str = ""
    content_type: str = "blog_post"  # blog_post, social_media, website_copy
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
    
    # Workflow Control
    current_agent: str = ""
    workflow_stage: str = "initialized"
    error_messages: List[str] = field(default_factory=list)
    completion_timestamp: Optional[str] = None
    
    # Performance Metrics
    processing_time: Dict[str, float] = field(default_factory=dict)
    agent_iterations: Dict[str, int] = field(default_factory=dict)


class ContentWorkflowGraph:
    """
    LangGraph-based workflow orchestrator for content creation
    """
    
    def __init__(self):
        self.llm = ChatOpenAI(temperature=0.7, model="gpt-3.5-turbo")
        self.memory = MemorySaver()
        self.graph = self._build_workflow_graph()
        
    def _build_workflow_graph(self) -> StateGraph:
        """
        Build the comprehensive directed graph workflow
        """
        # Initialize the state graph
        workflow = StateGraph(ContentCreationState)
        
        # Add all workflow nodes (states)
        workflow.add_node("initialize_workflow", self.initialize_workflow)
        workflow.add_node("research_agent", self.research_agent)
        workflow.add_node("analyze_research", self.analyze_research)
        workflow.add_node("content_planning", self.content_planning)
        workflow.add_node("content_writing", self.content_writing)
        workflow.add_node("content_review", self.content_review)
        workflow.add_node("seo_optimization", self.seo_optimization)
        workflow.add_node("quality_assurance", self.quality_assurance)
        workflow.add_node("revision_planning", self.revision_planning)
        workflow.add_node("content_revision", self.content_revision)
        workflow.add_node("final_assembly", self.final_assembly)
        workflow.add_node("workflow_completion", self.workflow_completion)
        workflow.add_node("error_handling", self.error_handling)
        
        # Define the workflow transitions (edges)
        self._add_workflow_transitions(workflow)
        
        # Set entry point
        workflow.set_entry_point("initialize_workflow")
        
        return workflow.compile(checkpointer=self.memory)
    
    def _add_workflow_transitions(self, workflow: StateGraph) -> None:
        """
        Define all state transitions and conditional logic
        """
        # Sequential workflow transitions
        workflow.add_edge("initialize_workflow", "research_agent")
        workflow.add_edge("research_agent", "analyze_research")
        
        # Conditional transition from research analysis
        workflow.add_conditional_edges(
            "analyze_research",
            self.decide_research_next_step,
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
            self.decide_content_next_step,
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
            self.decide_quality_next_step,
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
    # WORKFLOW NODES (AGENT STATES)
    # =============================================================================
    
    def initialize_workflow(self, state: ContentCreationState) -> ContentCreationState:
        """
        STATE: Initialize Workflow
        PURPOSE: Set up initial parameters and validate inputs
        AGENT: System Coordinator
        """
        print("🚀 INITIALIZING WORKFLOW")
        state.current_agent = "system_coordinator"
        state.workflow_stage = "initialization"
        start_time = datetime.now()
        
        # Validate required inputs
        if not state.topic:
            state.error_messages.append("Topic is required")
            return state
        
        # Set content type defaults
        content_configs = {
            "blog_post": {"min_words": 800, "max_words": 1500, "style": "informative"},
            "social_media": {"min_words": 50, "max_words": 280, "style": "engaging"},
            "website_copy": {"min_words": 200, "max_words": 500, "style": "persuasive"}
        }
        
        config = content_configs.get(state.content_type, content_configs["blog_post"])
        state.writing_style = config["style"]
        
        # Initialize metadata
        state.metadata.update({
            "workflow_start": start_time.isoformat(),
            "content_type": state.content_type,
            "target_min_words": config["min_words"],
            "target_max_words": config["max_words"]
        })
        
        state.processing_time["initialization"] = (datetime.now() - start_time).total_seconds()
        print(f"✅ Workflow initialized for topic: '{state.topic}'")
        
        return state
    
    def research_agent(self, state: ContentCreationState) -> ContentCreationState:
        """
        STATE: Research Agent
        PURPOSE: Conduct comprehensive topic research and trend analysis
        AGENT: Research Specialist
        """
        print("🔍 RESEARCH AGENT ACTIVE")
        state.current_agent = "research_specialist"
        state.workflow_stage = "research"
        start_time = datetime.now()
        
        # Increment iteration counter
        state.agent_iterations["research"] = state.agent_iterations.get("research", 0) + 1
        
        try:
            # Build comprehensive research query
            research_components = [
                state.topic,
                "trends 2024",
                "digital marketing",
                "technology startups"
            ]
            
            if state.target_audience:
                research_components.append(f"for {state.target_audience}")
            
            state.research_query = " ".join(research_components)
            
            # Execute research using SerpAPI
            print(f"🔎 Searching: {state.research_query}")
            search_results = research_tool.run(state.research_query)
            
            if isinstance(search_results, list):
                state.search_results = search_results
                state.research_confidence = min(len(search_results) / 5.0, 1.0)
                
                # Extract trending topics and keywords
                all_text = " ".join([
                    result.get("title", "") + " " + result.get("snippet", "")
                    for result in search_results
                ])
                
                # Simple keyword extraction (in production, use NLP libraries)
                common_words = ["ai", "artificial intelligence", "automation", "digital transformation", 
                              "machine learning", "startup", "technology", "innovation", "saas"]
                
                state.extracted_keywords = [
                    word for word in common_words 
                    if word.lower() in all_text.lower()
                ]
                
                # Create research summary
                state.research_summary = f"Found {len(search_results)} relevant sources. "
                state.research_summary += f"Key topics include: {', '.join(state.extracted_keywords[:5])}"
                
            else:
                state.error_messages.append(f"Research failed: {search_results}")
                state.research_confidence = 0.0
                
        except Exception as e:
            state.error_messages.append(f"Research error: {str(e)}")
            state.research_confidence = 0.0
        
        state.processing_time["research"] = (datetime.now() - start_time).total_seconds()
        print(f"📊 Research completed. Confidence: {state.research_confidence:.2f}")
        
        return state
    
    def analyze_research(self, state: ContentCreationState) -> ContentCreationState:
        """
        STATE: Analyze Research
        PURPOSE: Evaluate research quality and determine next steps
        AGENT: Research Analyst
        """
        print("📊 ANALYZING RESEARCH RESULTS")
        state.current_agent = "research_analyst"
        state.workflow_stage = "research_analysis"
        start_time = datetime.now()
        
        # Analyze research quality
        quality_indicators = {
            "sufficient_sources": len(state.search_results) >= 3,
            "relevant_keywords": len(state.extracted_keywords) >= 3,
            "confidence_threshold": state.research_confidence >= 0.6
        }
        
        state.metadata["research_quality"] = quality_indicators
        
        # Determine trending topics
        if state.search_results:
            # Extract trending topics from titles
            trending_candidates = []
            for result in state.search_results:
                title = result.get("title", "")
                if any(trend_word in title.lower() for trend_word in ["2024", "trend", "future", "new"]):
                    trending_candidates.append(title)
            
            state.trending_topics = trending_candidates[:5]
        
        state.processing_time["research_analysis"] = (datetime.now() - start_time).total_seconds()
        print(f"🎯 Analysis complete. Quality indicators: {quality_indicators}")
        
        return state
    
    def content_planning(self, state: ContentCreationState) -> ContentCreationState:
        """
        STATE: Content Planning
        PURPOSE: Create content outline and structure
        AGENT: Content Strategist
        """
        print("📋 CONTENT PLANNING PHASE")
        state.current_agent = "content_strategist"
        state.workflow_stage = "planning"
        start_time = datetime.now()
        
        # Create content outline based on type and research
        if state.content_type == "blog_post":
            sections = [
                {"title": "Introduction", "purpose": "Hook and overview"},
                {"title": "Main Content", "purpose": "Core information and insights"},
                {"title": "Benefits/Applications", "purpose": "Practical value"},
                {"title": "Future Outlook", "purpose": "Trends and predictions"},
                {"title": "Conclusion", "purpose": "Summary and call-to-action"}
            ]
        elif state.content_type == "social_media":
            sections = [
                {"title": "Hook", "purpose": "Attention grabber"},
                {"title": "Value Proposition", "purpose": "Key benefit"},
                {"title": "Call to Action", "purpose": "Engagement driver"}
            ]
        else:  # website_copy
            sections = [
                {"title": "Headline", "purpose": "Value proposition"},
                {"title": "Benefits", "purpose": "Key advantages"},
                {"title": "Social Proof", "purpose": "Credibility"},
                {"title": "CTA", "purpose": "Conversion driver"}
            ]
        
        state.content_sections = sections
        
        # Create detailed outline
        outline_parts = []
        for i, section in enumerate(sections, 1):
            outline_parts.append(f"{i}. {section['title']}: {section['purpose']}")
        
        state.content_outline = "\n".join(outline_parts)
        
        # Set primary keywords from research
        state.primary_keywords = state.extracted_keywords[:5] + state.specific_keywords
        
        state.processing_time["planning"] = (datetime.now() - start_time).total_seconds()
        print(f"📝 Content plan created with {len(sections)} sections")
        
        return state
    
    def content_writing(self, state: ContentCreationState) -> ContentCreationState:
        """
        STATE: Content Writing
        PURPOSE: Generate content based on research and outline
        AGENT: Content Writer
        """
        print("✍️ CONTENT WRITING PHASE")
        state.current_agent = "content_writer"
        state.workflow_stage = "writing"
        start_time = datetime.now()
        
        try:
            # Prepare comprehensive writing prompt
            writing_context = {
                "topic": state.topic,
                "content_type": state.content_type,
                "outline": state.content_outline,
                "research_summary": state.research_summary,
                "keywords": state.primary_keywords,
                "style": state.writing_style,
                "target_audience": state.target_audience or "technology professionals"
            }
            
            prompt = f"""
            Create {state.content_type} content about: {state.topic}
            
            Content Outline:
            {state.content_outline}
            
            Research Insights:
            {state.research_summary}
            
            Target Keywords: {', '.join(state.primary_keywords)}
            
            Writing Style: {state.writing_style}
            Target Audience: {writing_context['target_audience']}
            
            Requirements:
            - Professional tone appropriate for technology startups
            - Natural integration of keywords
            - Engaging and informative content
            - Clear structure following the outline
            """
            
            # Generate content using OpenAI
            draft_content = writing_tool.run(prompt)
            
            if isinstance(draft_content, str) and len(draft_content) > 100:
                state.draft_content = draft_content
                state.word_count = len(draft_content.split())
                print(f"📝 Content generated: {state.word_count} words")
            else:
                state.error_messages.append("Content generation failed or produced insufficient content")
                
        except Exception as e:
            state.error_messages.append(f"Writing error: {str(e)}")
        
        state.processing_time["writing"] = (datetime.now() - start_time).total_seconds()
        
        return state
    
    def content_review(self, state: ContentCreationState) -> ContentCreationState:
        """
        STATE: Content Review
        PURPOSE: Initial quality check and structure validation
        AGENT: Content Editor
        """
        print("📖 CONTENT REVIEW PHASE")
        state.current_agent = "content_editor"
        state.workflow_stage = "review"
        start_time = datetime.now()
        
        if not state.draft_content:
            state.error_messages.append("No content to review")
            return state
        
        # Perform basic content checks
        review_criteria = {
            "sufficient_length": state.word_count >= state.metadata.get("target_min_words", 300),
            "not_too_long": state.word_count <= state.metadata.get("target_max_words", 1500),
            "has_introduction": "introduction" in state.draft_content.lower()[:200],
            "has_conclusion": any(word in state.draft_content.lower()[-200:] 
                                for word in ["conclusion", "summary", "finally"]),
            "keyword_integration": any(keyword.lower() in state.draft_content.lower() 
                                     for keyword in state.primary_keywords)
        }
        
        # Calculate basic quality score
        passed_checks = sum(review_criteria.values())
        total_checks = len(review_criteria)
        basic_quality_score = (passed_checks / total_checks) * 100
        
        state.metadata["content_review"] = {
            "criteria": review_criteria,
            "basic_quality_score": basic_quality_score,
            "word_count": state.word_count
        }
        
        state.processing_time["review"] = (datetime.now() - start_time).total_seconds()
        print(f"✅ Content review complete. Basic score: {basic_quality_score:.1f}/100")
        
        return state
    
    def seo_optimization(self, state: ContentCreationState) -> ContentCreationState:
        """
        STATE: SEO Optimization
        PURPOSE: Optimize content for search engines
        AGENT: SEO Specialist
        """
        print("🔍 SEO OPTIMIZATION PHASE")
        state.current_agent = "seo_specialist"
        state.workflow_stage = "seo_optimization"
        start_time = datetime.now()
        
        try:
            # Prepare keywords for SEO tool
            seo_keywords = ", ".join(state.primary_keywords)
            
            # Apply SEO optimization
            optimized_content = seo_tool.run(state.draft_content, seo_keywords)
            
            if optimized_content and optimized_content != state.draft_content:
                state.optimized_content = optimized_content
                print("✅ SEO optimization applied")
            else:
                state.optimized_content = state.draft_content
                print("ℹ️ Using original content (no SEO changes needed)")
            
            # Generate meta description (simple extraction)
            first_sentences = ". ".join(state.draft_content.split(". ")[:2])
            if len(first_sentences) > 160:
                state.meta_description = first_sentences[:157] + "..."
            else:
                state.meta_description = first_sentences
            
            # Generate title suggestions
            state.title_suggestions = [
                f"{state.topic}: Complete Guide for 2024",
                f"How {state.topic} is Transforming Business",
                f"The Ultimate Guide to {state.topic}",
                f"{state.topic}: Benefits and Implementation"
            ]
            
            # Calculate SEO score based on keyword density and other factors
            content_lower = state.optimized_content.lower()
            keyword_occurrences = sum(
                content_lower.count(keyword.lower()) 
                for keyword in state.primary_keywords
            )
            
            # Simple SEO scoring
            seo_factors = {
                "keyword_density": min(keyword_occurrences / max(len(state.primary_keywords), 1), 5),
                "meta_description_length": 1 if 120 <= len(state.meta_description) <= 160 else 0.5,
                "title_optimization": 1 if state.topic.lower() in state.title_suggestions[0].lower() else 0.5
            }
            
            state.seo_score = (sum(seo_factors.values()) / len(seo_factors)) * 100
            
        except Exception as e:
            state.error_messages.append(f"SEO optimization error: {str(e)}")
            state.optimized_content = state.draft_content
            state.seo_score = 50.0
        
        state.processing_time["seo_optimization"] = (datetime.now() - start_time).total_seconds()
        print(f"🎯 SEO optimization complete. Score: {state.seo_score:.1f}/100")
        
        return state
    
    def quality_assurance(self, state: ContentCreationState) -> ContentCreationState:
        """
        STATE: Quality Assurance
        PURPOSE: Comprehensive quality evaluation and scoring
        AGENT: Quality Assurance Specialist
        """
        print("✅ QUALITY ASSURANCE PHASE")
        state.current_agent = "qa_specialist"
        state.workflow_stage = "quality_assurance"
        start_time = datetime.now()
        
        content_to_check = state.optimized_content or state.draft_content
        
        # Comprehensive quality checks
        quality_checks = {
            # Content Structure
            "proper_length": state.metadata.get("target_min_words", 300) <= state.word_count <= state.metadata.get("target_max_words", 1500),
            "has_sections": len([line for line in content_to_check.split('\n') if line.strip()]) >= 3,
            "complete_sentences": content_to_check.count('.') >= 3,
            
            # Content Quality
            "keyword_integration": any(keyword.lower() in content_to_check.lower() for keyword in state.primary_keywords),
            "topic_relevance": state.topic.lower().replace(' ', '') in content_to_check.lower().replace(' ', ''),
            "professional_tone": not any(informal in content_to_check.lower() for informal in ['gonna', 'wanna', 'gotta']),
            
            # Technical Requirements
            "no_placeholders": '[' not in content_to_check and '{{' not in content_to_check,
            "proper_capitalization": content_to_check[0].isupper() if content_to_check else False,
            "conclusion_present": any(conclusion_word in content_to_check.lower()[-300:] 
                                    for conclusion_word in ['conclusion', 'summary', 'finally', 'in summary'])
        }
        
        state.quality_checks = quality_checks
        
        # Calculate overall quality score
        passed_checks = sum(quality_checks.values())
        total_checks = len(quality_checks)
        base_quality_score = (passed_checks / total_checks) * 100
        
        # Incorporate SEO score
        state.quality_score = (base_quality_score * 0.7) + (state.seo_score * 0.3)
        
        # Generate feedback for failed checks
        state.quality_feedback = []
        if not quality_checks["proper_length"]:
            state.quality_feedback.append(f"Content length ({state.word_count} words) outside target range")
        if not quality_checks["keyword_integration"]:
            state.quality_feedback.append("Keywords not properly integrated")
        if not quality_checks["conclusion_present"]:
            state.quality_feedback.append("Content lacks proper conclusion")
        if not quality_checks["professional_tone"]:
            state.quality_feedback.append("Tone not sufficiently professional")
        
        # Determine if revision is needed
        state.revision_needed = state.quality_score < Config.MIN_QUALITY_SCORE and state.revision_count < 2
        
        state.processing_time["quality_assurance"] = (datetime.now() - start_time).total_seconds()
        print(f"🎯 Quality assessment complete. Score: {state.quality_score:.1f}/100")
        if state.quality_feedback:
            print(f"📋 Feedback: {'; '.join(state.quality_feedback)}")
        
        return state
    
    def revision_planning(self, state: ContentCreationState) -> ContentCreationState:
        """
        STATE: Revision Planning
        PURPOSE: Plan content improvements based on quality feedback
        AGENT: Revision Planner
        """
        print("🔄 REVISION PLANNING PHASE")
        state.current_agent = "revision_planner"
        state.workflow_stage = "revision_planning"
        start_time = datetime.now()
        
        state.revision_count += 1
        
        # Create revision strategy based on feedback
        revision_strategies = []
        
        if "length" in " ".join(state.quality_feedback).lower():
            if state.word_count < state.metadata.get("target_min_words", 300):
                revision_strategies.append("Expand content with more detailed examples and explanations")
            else:
                revision_strategies.append("Condense content while maintaining key points")
        
        if "keyword" in " ".join(state.quality_feedback).lower():
            revision_strategies.append(f"Better integrate keywords: {', '.join(state.primary_keywords)}")
        
        if "conclusion" in " ".join(state.quality_feedback).lower():
            revision_strategies.append("Add comprehensive conclusion section")
        
        if "professional" in " ".join(state.quality_feedback).lower():
            revision_strategies.append("Enhance professional tone and language")
        
        state.metadata["revision_plan"] = {
            "revision_number": state.revision_count,
            "strategies": revision_strategies,
            "target_improvements": state.quality_feedback
        }
        
        state.processing_time["revision_planning"] = (datetime.now() - start_time).total_seconds()
        print(f"📝 Revision plan created. Strategies: {len(revision_strategies)}")
        
        return state
    
    def content_revision(self, state: ContentCreationState) -> ContentCreationState:
        """
        STATE: Content Revision
        PURPOSE: Implement planned improvements
        AGENT: Content Revisor
        """
        print("✏️ CONTENT REVISION PHASE")
        state.current_agent = "content_revisor"
        state.workflow_stage = "content_revision"
        start_time = datetime.now()
        
        try:
            revision_prompt = f"""
            Revise the following content based on these improvement areas:
            {'; '.join(state.quality_feedback)}
            
            Revision strategies to implement:
            {'; '.join(state.metadata.get('revision_plan', {}).get('strategies', []))}
            
            Original content:
            {state.optimized_content or state.draft_content}
            
            Target keywords to integrate: {', '.join(state.primary_keywords)}
            Target word count: {state.metadata.get('target_min_words', 300)}-{state.metadata.get('target_max_words', 1500)}
            
            Please provide the revised content that addresses all feedback points.
            """
            
            revised_content = writing_tool.run(revision_prompt)
            
            if isinstance(revised_content, str) and len(revised_content) > 100:
                state.draft_content = revised_content
                state.word_count = len(revised_content.split())
                print(f"✅ Content revised: {state.word_count} words")
            else:
                state.error_messages.append("Content revision failed")
                
        except Exception as e:
            state.error_messages.append(f"Revision error: {str(e)}")
        
        state.processing_time["content_revision"] = (datetime.now() - start_time).total_seconds()
        
        return state
    
    def final_assembly(self, state: ContentCreationState) -> ContentCreationState:
        """
        STATE: Final Assembly
        PURPOSE: Prepare final content package with metadata
        AGENT: Content Assembler
        """
        print("📦 FINAL ASSEMBLY PHASE")
        state.current_agent = "content_assembler"
        state.workflow_stage = "final_assembly"
        start_time = datetime.now()
        
        # Use the best available content
        state.final_content = state.optimized_content or state.draft_content
        
        # Compile comprehensive metadata
        state.metadata.update({
            "final_word_count": len(state.final_content.split()),
            "final_quality_score": state.quality_score,
            "seo_score": state.seo_score,
            "revision_count": state.revision_count,
            "primary_keywords": state.primary_keywords,
            "meta_description": state.meta_description,
            "title_suggestions": state.title_suggestions,
            "content_type": state.content_type,
            "target_audience": state.target_audience,
            "research_sources": len(state.search_results),
            "processing_summary": {
                "total_agents": len(state.agent_iterations),
                "total_processing_time": sum(state.processing_time.values()),
                "research_confidence": state.research_confidence
            }
        })
        
        state.processing_time["final_assembly"] = (datetime.now() - start_time).total_seconds()
        print(f"✅ Final content assembled: {len(state.final_content.split())} words, Quality: {state.quality_score:.1f}/100")
        
        return state
    
    def workflow_completion(self, state: ContentCreationState) -> ContentCreationState:
        """
        STATE: Workflow Completion
        PURPOSE: Finalize workflow and prepare output
        AGENT: Workflow Manager
        """
        print("🎉 WORKFLOW COMPLETION")
        state.current_agent = "workflow_manager"
        state.workflow_stage = "completed"
        
        state.completion_timestamp = datetime.now().isoformat()
        state.metadata["completion_timestamp"] = state.completion_timestamp
        state.metadata["workflow_status"] = "completed_successfully"
        
        # Calculate total processing time
        total_time = sum(state.processing_time.values())
        state.metadata["total_processing_time"] = total_time
        
        print(f"🏁 Workflow completed in {total_time:.2f} seconds")
        print(f"📊 Final metrics: {state.quality_score:.1f}/100 quality, {len(state.final_content.split())} words")
        
        return state
    
    def error_handling(self, state: ContentCreationState) -> ContentCreationState:
        """
        STATE: Error Handling
        PURPOSE: Handle workflow errors and prepare error response
        AGENT: Error Handler
        """
        print("❌ ERROR HANDLING ACTIVATED")
        state.current_agent = "error_handler"
        state.workflow_stage = "error"
        
        error_summary = "; ".join(state.error_messages)
        print(f"🚨 Errors encountered: {error_summary}")
        
        # Try to provide partial results if possible
        if state.draft_content:
            state.final_content = state.draft_content
            state.metadata["status"] = "completed_with_errors"
        else:
            state.final_content = f"Content generation failed due to: {error_summary}"
            state.metadata["status"] = "failed"
        
        state.completion_timestamp = datetime.now().isoformat()
        state.metadata.update({
            "completion_timestamp": state.completion_timestamp,
            "error_messages": state.error_messages,
            "partial_completion": bool(state.draft_content)
        })
        
        return state
    
    # =============================================================================
    # CONDITIONAL TRANSITION FUNCTIONS
    # =============================================================================
    
    def decide_research_next_step(self, state: ContentCreationState) -> Literal["proceed_to_planning", "retry_research", "handle_error"]:
        """Decide next step after research analysis"""
        if state.error_messages:
            return "handle_error"
        elif state.research_confidence < 0.3 and state.agent_iterations.get("research", 0) < 2:
            return "retry_research"
        else:
            return "proceed_to_planning"
    
    def decide_content_next_step(self, state: ContentCreationState) -> Literal["proceed_to_seo", "revise_content", "handle_error"]:
        """Decide next step after content review"""
        if state.error_messages:
            return "handle_error"
        elif not state.draft_content or state.word_count < 100:
            return "revise_content"
        else:
            return "proceed_to_seo"
    
    def decide_quality_next_step(self, state: ContentCreationState) -> Literal["finalize_content", "plan_revision", "handle_error"]:
        """Decide next step after quality assurance"""
        if state.error_messages:
            return "handle_error"
        elif state.revision_needed and state.revision_count < 2:
            return "plan_revision"
        else:
            return "finalize_content"
    
    # =============================================================================
    # WORKFLOW EXECUTION METHODS
    # =============================================================================
    
    def run_workflow(self, 
                    topic: str, 
                    content_type: str = "blog_post",
                    target_audience: str = "",
                    specific_keywords: List[str] = None) -> Dict[str, Any]:
        """
        Execute the complete workflow
        """
        print("="*80)
        print("🚀 STARTING LANGGRAPH CONTENT CREATION WORKFLOW")
        print("="*80)
        
        # Initialize state
        initial_state = ContentCreationState(
            topic=topic,
            content_type=content_type,
            target_audience=target_audience,
            specific_keywords=specific_keywords or []
        )
        
        try:
            # Execute workflow
            config = {"configurable": {"thread_id": f"content_creation_{datetime.now().timestamp()}"}}
            final_state = self.graph.invoke(initial_state, config)
            
            # Return results
            return {
                "success": True,
                "final_content": final_state.final_content,
                "quality_score": final_state.quality_score,
                "metadata": final_state.metadata,
                "seo_data": {
                    "meta_description": final_state.meta_description,
                    "title_suggestions": final_state.title_suggestions,
                    "primary_keywords": final_state.primary_keywords,
                    "seo_score": final_state.seo_score
                },
                "workflow_analytics": {
                    "processing_time": final_state.processing_time,
                    "agent_iterations": final_state.agent_iterations,
                    "revision_count": final_state.revision_count,
                    "research_confidence": final_state.research_confidence
                }
            }
            
        except Exception as e:
            print(f"❌ Workflow execution failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "final_content": "Workflow execution failed",
                "metadata": {"error": str(e)}
            }

# =============================================================================
# WORKFLOW EXECUTION FUNCTION
# =============================================================================

def run_advanced_langgraph_workflow(topic: str, 
                                   content_type: str = "blog_post",
                                   target_audience: str = "",
                                   specific_keywords: List[str] = None) -> Dict[str, Any]:
    """
    Main function to execute the advanced LangGraph workflow
    """
    workflow = ContentWorkflowGraph()
    return workflow.run_workflow(topic, content_type, target_audience, specific_keywords)


if __name__ == "__main__":
    # Example execution
    result = run_advanced_langgraph_workflow(
        topic="AI automation for small businesses",
        content_type="blog_post",
        target_audience="small business owners and entrepreneurs",
        specific_keywords=["automation", "efficiency", "cost reduction"]
    )
    
    if result["success"]:
        print("\n" + "="*60)
        print("✅ WORKFLOW COMPLETED SUCCESSFULLY")
        print("="*60)
        print(f"Quality Score: {result['quality_score']:.1f}/100")
        print(f"Word Count: {result['metadata'].get('final_word_count', 0)}")
        print(f"Processing Time: {result['metadata'].get('total_processing_time', 0):.2f}s")
        print(f"\nContent Preview:\n{result['final_content'][:300]}...")
    else:
        print(f"❌ Workflow failed: {result['error']}")