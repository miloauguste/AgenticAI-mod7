"""
State Handoff Manager for LangGraph Content Creation Workflow
Comprehensive management of information flow and transitions between nodes
"""

import os
import json
from typing import Dict, Any, List, Optional, Tuple, Union
from dataclasses import dataclass, field, asdict
from datetime import datetime
import copy
import hashlib
from enum import Enum

class HandoffStatus(Enum):
    """Status codes for state handoffs"""
    SUCCESS = "success"
    WARNING = "warning"
    FAILURE = "failure"
    PARTIAL = "partial"
    VALIDATION_ERROR = "validation_error"

class NodeType(Enum):
    """Types of nodes in the workflow"""
    INITIALIZATION = "initialization"
    RESEARCH = "research"
    ANALYSIS = "analysis"
    PLANNING = "planning"
    WRITING = "writing"
    REVIEW = "review"
    SEO = "seo"
    QA = "qa"
    REVISION = "revision"
    ASSEMBLY = "assembly"
    COMPLETION = "completion"
    ERROR = "error"

@dataclass
class StateHandoffRecord:
    """Record of a state handoff between nodes"""
    handoff_id: str
    source_node: str
    target_node: str
    timestamp: str
    status: HandoffStatus
    data_transferred: Dict[str, Any]
    data_size: int
    validation_results: Dict[str, Any]
    transformation_applied: List[str]
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    processing_time: float = 0.0
    checksum: str = ""

@dataclass
class StateValidationRule:
    """Validation rule for state data"""
    field_name: str
    required: bool
    data_type: type
    min_length: Optional[int] = None
    max_length: Optional[int] = None
    allowed_values: Optional[List[Any]] = None
    validation_function: Optional[callable] = None
    transformation_function: Optional[callable] = None

class StateHandoffManager:
    """
    Manages state transitions and data handoffs between workflow nodes
    """
    
    def __init__(self):
        self.handoff_history: List[StateHandoffRecord] = []
        self.validation_rules = self._initialize_validation_rules()
        self.transformation_rules = self._initialize_transformation_rules()
        self.node_requirements = self._initialize_node_requirements()
        
    def _initialize_validation_rules(self) -> Dict[str, List[StateValidationRule]]:
        """Initialize validation rules for each node transition"""
        
        return {
            # Initialize Workflow → Research Agent
            "initialize_workflow->research_agent": [
                StateValidationRule("topic", True, str, min_length=5, max_length=200),
                StateValidationRule("content_type", True, str, allowed_values=["blog_post", "social_media", "website_copy"]),
                StateValidationRule("target_audience", False, str, max_length=100),
                StateValidationRule("metadata", True, dict),
                StateValidationRule("workflow_stage", True, str, allowed_values=["initialization"]),
            ],
            
            # Research Agent → Analyze Research
            "research_agent->analyze_research": [
                StateValidationRule("research_query", True, str, min_length=10),
                StateValidationRule("search_results", True, list, min_length=0),
                StateValidationRule("research_confidence", True, float, validation_function=lambda x: 0.0 <= x <= 1.0),
                StateValidationRule("extracted_keywords", True, list),
                StateValidationRule("research_summary", True, str, min_length=20),
            ],
            
            # Analyze Research → Content Planning
            "analyze_research->content_planning": [
                StateValidationRule("trending_topics", True, list),
                StateValidationRule("research_confidence", True, float, validation_function=lambda x: x >= 0.3),
                StateValidationRule("metadata", True, dict),
            ],
            
            # Content Planning → Content Writing
            "content_planning->content_writing": [
                StateValidationRule("content_outline", True, str, min_length=50),
                StateValidationRule("content_sections", True, list, min_length=2),
                StateValidationRule("primary_keywords", True, list, min_length=1),
                StateValidationRule("metadata", True, dict),
            ],
            
            # Content Writing → Content Review
            "content_writing->content_review": [
                StateValidationRule("draft_content", True, str, min_length=100),
                StateValidationRule("word_count", True, int, validation_function=lambda x: x >= 50),
                StateValidationRule("content_sections", True, list),
            ],
            
            # Content Review → SEO Optimization
            "content_review->seo_optimization": [
                StateValidationRule("draft_content", True, str, min_length=100),
                StateValidationRule("word_count", True, int, validation_function=lambda x: x >= 100),
                StateValidationRule("primary_keywords", True, list, min_length=1),
            ],
            
            # SEO Optimization → Quality Assurance
            "seo_optimization->quality_assurance": [
                StateValidationRule("optimized_content", True, str, min_length=100),
                StateValidationRule("seo_score", True, float, validation_function=lambda x: 0.0 <= x <= 100.0),
                StateValidationRule("meta_description", True, str, min_length=120, max_length=160),
                StateValidationRule("title_suggestions", True, list, min_length=1),
            ],
            
            # Quality Assurance → Final Assembly (success path)
            "quality_assurance->final_assembly": [
                StateValidationRule("quality_score", True, float, validation_function=lambda x: x >= 70.0),
                StateValidationRule("optimized_content", True, str, min_length=200),
                StateValidationRule("quality_checks", True, dict),
            ],
            
            # Quality Assurance → Revision Planning (revision path)
            "quality_assurance->revision_planning": [
                StateValidationRule("quality_score", True, float, validation_function=lambda x: x < 80.0),
                StateValidationRule("quality_feedback", True, list, min_length=1),
                StateValidationRule("revision_count", True, int, validation_function=lambda x: x < 2),
            ],
            
            # Revision Planning → Content Revision
            "revision_planning->content_revision": [
                StateValidationRule("metadata", True, dict),
                StateValidationRule("quality_feedback", True, list, min_length=1),
                StateValidationRule("revision_count", True, int),
            ],
            
            # Content Revision → Content Review (loop back)
            "content_revision->content_review": [
                StateValidationRule("draft_content", True, str, min_length=100),
                StateValidationRule("word_count", True, int, validation_function=lambda x: x >= 100),
                StateValidationRule("revision_count", True, int, validation_function=lambda x: x <= 2),
            ],
            
            # Final Assembly → Workflow Completion
            "final_assembly->workflow_completion": [
                StateValidationRule("final_content", True, str, min_length=200),
                StateValidationRule("quality_score", True, float, validation_function=lambda x: x >= 70.0),
                StateValidationRule("metadata", True, dict),
            ],
            
            # Any Node → Error Handling
            "any->error_handling": [
                StateValidationRule("error_messages", True, list, min_length=1),
                StateValidationRule("current_agent", True, str),
                StateValidationRule("workflow_stage", True, str),
            ],
        }
    
    def _initialize_transformation_rules(self) -> Dict[str, List[callable]]:
        """Initialize data transformation rules for state handoffs"""
        
        return {
            # Research Agent → Analyze Research transformations
            "research_agent->analyze_research": [
                self._normalize_search_results,
                self._calculate_research_metrics,
                self._extract_trending_indicators,
            ],
            
            # Analyze Research → Content Planning transformations
            "analyze_research->content_planning": [
                self._prioritize_keywords,
                self._prepare_content_strategy,
                self._calculate_content_targets,
            ],
            
            # Content Planning → Content Writing transformations
            "content_planning->content_writing": [
                self._prepare_writing_context,
                self._optimize_section_distribution,
                self._prepare_keyword_integration_plan,
            ],
            
            # Content Writing → Content Review transformations
            "content_writing->content_review": [
                self._prepare_content_for_review,
                self._calculate_basic_metrics,
                self._extract_content_characteristics,
            ],
            
            # Content Review → SEO Optimization transformations
            "content_review->seo_optimization": [
                self._prepare_seo_context,
                self._extract_content_structure,
                self._prepare_keyword_data,
            ],
            
            # SEO Optimization → Quality Assurance transformations
            "seo_optimization->quality_assurance": [
                self._prepare_qa_context,
                self._consolidate_content_versions,
                self._prepare_quality_criteria,
            ],
            
            # Quality Assurance → Revision Planning transformations
            "quality_assurance->revision_planning": [
                self._analyze_quality_gaps,
                self._prioritize_improvements,
                self._prepare_revision_strategy,
            ],
            
            # Final Assembly → Workflow Completion transformations
            "final_assembly->workflow_completion": [
                self._prepare_final_output,
                self._calculate_final_metrics,
                self._prepare_success_summary,
            ],
        }
    
    def _initialize_node_requirements(self) -> Dict[str, Dict[str, Any]]:
        """Initialize requirements for each node"""
        
        return {
            "initialize_workflow": {
                "required_inputs": ["topic"],
                "optional_inputs": ["content_type", "target_audience", "specific_keywords"],
                "outputs": ["metadata", "workflow_stage", "content_config"],
                "processing_time_target": 1.0,
                "memory_requirements": "low"
            },
            
            "research_agent": {
                "required_inputs": ["topic", "metadata"],
                "optional_inputs": ["target_audience", "specific_keywords"],
                "outputs": ["search_results", "research_confidence", "extracted_keywords", "research_summary"],
                "processing_time_target": 5.0,
                "memory_requirements": "medium"
            },
            
            "analyze_research": {
                "required_inputs": ["search_results", "research_confidence", "extracted_keywords"],
                "optional_inputs": ["trending_topics"],
                "outputs": ["research_assessment", "content_strategy", "trending_topics"],
                "processing_time_target": 2.0,
                "memory_requirements": "low"
            },
            
            "content_planning": {
                "required_inputs": ["research_assessment", "content_strategy"],
                "optional_inputs": ["target_audience"],
                "outputs": ["content_outline", "content_sections", "primary_keywords"],
                "processing_time_target": 2.0,
                "memory_requirements": "low"
            },
            
            "content_writing": {
                "required_inputs": ["content_outline", "content_sections", "primary_keywords"],
                "optional_inputs": ["research_summary", "trending_topics"],
                "outputs": ["draft_content", "word_count", "content_analytics"],
                "processing_time_target": 8.0,
                "memory_requirements": "high"
            },
            
            "content_review": {
                "required_inputs": ["draft_content", "word_count"],
                "optional_inputs": ["content_sections"],
                "outputs": ["content_analysis", "review_score", "improvement_suggestions"],
                "processing_time_target": 3.0,
                "memory_requirements": "medium"
            },
            
            "seo_optimization": {
                "required_inputs": ["draft_content", "primary_keywords"],
                "optional_inputs": ["meta_description", "title_suggestions"],
                "outputs": ["optimized_content", "seo_score", "meta_description", "title_suggestions"],
                "processing_time_target": 4.0,
                "memory_requirements": "medium"
            },
            
            "quality_assurance": {
                "required_inputs": ["optimized_content", "seo_score"],
                "optional_inputs": ["quality_criteria"],
                "outputs": ["quality_score", "quality_checks", "quality_feedback", "revision_needed"],
                "processing_time_target": 3.0,
                "memory_requirements": "medium"
            },
            
            "revision_planning": {
                "required_inputs": ["quality_feedback", "quality_score"],
                "optional_inputs": ["revision_count"],
                "outputs": ["revision_strategy", "improvement_plan"],
                "processing_time_target": 1.0,
                "memory_requirements": "low"
            },
            
            "content_revision": {
                "required_inputs": ["draft_content", "revision_strategy"],
                "optional_inputs": ["improvement_plan"],
                "outputs": ["draft_content", "word_count", "revision_applied"],
                "processing_time_target": 6.0,
                "memory_requirements": "high"
            },
            
            "final_assembly": {
                "required_inputs": ["optimized_content", "quality_score", "metadata"],
                "optional_inputs": ["seo_score", "content_analytics"],
                "outputs": ["final_content", "comprehensive_metadata", "performance_metrics"],
                "processing_time_target": 2.0,
                "memory_requirements": "medium"
            },
            
            "workflow_completion": {
                "required_inputs": ["final_content", "comprehensive_metadata"],
                "optional_inputs": ["performance_metrics"],
                "outputs": ["completion_status", "success_metrics", "output_package"],
                "processing_time_target": 1.0,
                "memory_requirements": "low"
            },
            
            "error_handling": {
                "required_inputs": ["error_messages", "current_agent"],
                "optional_inputs": ["partial_results"],
                "outputs": ["error_analysis", "recovery_options", "partial_output"],
                "processing_time_target": 1.0,
                "memory_requirements": "low"
            }
        }

    # =============================================================================
    # CORE HANDOFF MANAGEMENT METHODS
    # =============================================================================
    
    def execute_handoff(self, state, source_node: str, target_node: str) -> Tuple[Any, StateHandoffRecord]:
        """
        Execute a complete state handoff between two nodes
        """
        start_time = datetime.now()
        handoff_id = self._generate_handoff_id(source_node, target_node)
        
        print(f"🔄 Executing handoff: {source_node} → {target_node}")
        
        # Initialize handoff record
        handoff_record = StateHandoffRecord(
            handoff_id=handoff_id,
            source_node=source_node,
            target_node=target_node,
            timestamp=start_time.isoformat(),
            status=HandoffStatus.SUCCESS,
            data_transferred={},
            data_size=0,
            validation_results={},
            transformation_applied=[]
        )
        
        try:
            # Step 1: Pre-handoff validation
            validation_result = self._validate_pre_handoff(state, source_node, target_node)
            handoff_record.validation_results["pre_handoff"] = validation_result
            
            if not validation_result["valid"]:
                handoff_record.status = HandoffStatus.VALIDATION_ERROR
                handoff_record.errors.extend(validation_result["errors"])
                return state, handoff_record
            
            # Step 2: Create state snapshot
            state_snapshot = self._create_state_snapshot(state)
            handoff_record.data_size = len(json.dumps(asdict(state_snapshot), default=str))
            
            # Step 3: Apply transformations
            transformed_state = self._apply_transformations(state, source_node, target_node)
            handoff_record.transformation_applied = self._get_applied_transformations(source_node, target_node)
            
            # Step 4: Post-handoff validation
            post_validation = self._validate_post_handoff(transformed_state, source_node, target_node)
            handoff_record.validation_results["post_handoff"] = post_validation
            
            if not post_validation["valid"]:
                handoff_record.status = HandoffStatus.WARNING
                handoff_record.warnings.extend(post_validation["warnings"])
            
            # Step 5: Update state metadata
            transformed_state = self._update_handoff_metadata(transformed_state, handoff_record)
            
            # Step 6: Generate checksum
            handoff_record.checksum = self._generate_state_checksum(transformed_state)
            
            # Step 7: Record data transferred
            handoff_record.data_transferred = self._extract_transferred_data(state, transformed_state)
            
            print(f"✅ Handoff completed: {source_node} → {target_node}")
            return transformed_state, handoff_record
            
        except Exception as e:
            handoff_record.status = HandoffStatus.FAILURE
            handoff_record.errors.append(f"Handoff execution failed: {str(e)}")
            print(f"❌ Handoff failed: {source_node} → {target_node}: {e}")
            return state, handoff_record
            
        finally:
            # Record processing time and store handoff record
            handoff_record.processing_time = (datetime.now() - start_time).total_seconds()
            self.handoff_history.append(handoff_record)
    
    def _validate_pre_handoff(self, state, source_node: str, target_node: str) -> Dict[str, Any]:
        """Validate state before handoff"""
        
        transition_key = f"{source_node}->{target_node}"
        validation_rules = self.validation_rules.get(transition_key, [])
        
        validation_result = {
            "valid": True,
            "errors": [],
            "warnings": [],
            "checked_fields": []
        }
        
        # Check each validation rule
        for rule in validation_rules:
            field_value = getattr(state, rule.field_name, None)
            validation_result["checked_fields"].append(rule.field_name)
            
            # Required field check
            if rule.required and field_value is None:
                validation_result["valid"] = False
                validation_result["errors"].append(f"Required field '{rule.field_name}' is missing")
                continue
            
            if field_value is not None:
                # Type check
                if not isinstance(field_value, rule.data_type):
                    validation_result["valid"] = False
                    validation_result["errors"].append(
                        f"Field '{rule.field_name}' has wrong type. Expected {rule.data_type}, got {type(field_value)}"
                    )
                    continue
                
                # Length checks for strings and lists
                if rule.min_length is not None and hasattr(field_value, '__len__'):
                    if len(field_value) < rule.min_length:
                        validation_result["valid"] = False
                        validation_result["errors"].append(
                            f"Field '{rule.field_name}' is too short. Minimum length: {rule.min_length}"
                        )
                
                if rule.max_length is not None and hasattr(field_value, '__len__'):
                    if len(field_value) > rule.max_length:
                        validation_result["warnings"].append(
                            f"Field '{rule.field_name}' is very long. Maximum recommended: {rule.max_length}"
                        )
                
                # Allowed values check
                if rule.allowed_values is not None and field_value not in rule.allowed_values:
                    validation_result["valid"] = False
                    validation_result["errors"].append(
                        f"Field '{rule.field_name}' has invalid value. Allowed: {rule.allowed_values}"
                    )
                
                # Custom validation function
                if rule.validation_function is not None:
                    try:
                        if not rule.validation_function(field_value):
                            validation_result["valid"] = False
                            validation_result["errors"].append(
                                f"Field '{rule.field_name}' failed custom validation"
                            )
                    except Exception as e:
                        validation_result["warnings"].append(
                            f"Custom validation failed for '{rule.field_name}': {e}"
                        )
        
        return validation_result
    
    def _apply_transformations(self, state, source_node: str, target_node: str):
        """Apply data transformations during handoff"""
        
        # Create a copy of the state to avoid modifying the original
        transformed_state = copy.deepcopy(state)
        
        transition_key = f"{source_node}->{target_node}"
        transformation_functions = self.transformation_rules.get(transition_key, [])
        
        # Apply each transformation function
        for transform_func in transformation_functions:
            try:
                transformed_state = transform_func(transformed_state)
            except Exception as e:
                print(f"⚠️ Transformation failed: {transform_func.__name__}: {e}")
                # Continue with other transformations
        
        return transformed_state
    
    def _validate_post_handoff(self, state, source_node: str, target_node: str) -> Dict[str, Any]:
        """Validate state after handoff and transformations"""
        
        # Check target node requirements
        target_requirements = self.node_requirements.get(target_node, {})
        required_inputs = target_requirements.get("required_inputs", [])
        
        validation_result = {
            "valid": True,
            "errors": [],
            "warnings": [],
            "requirements_met": []
        }
        
        # Check if all required inputs for target node are present
        for required_input in required_inputs:
            field_value = getattr(state, required_input, None)
            
            if field_value is None:
                validation_result["valid"] = False
                validation_result["errors"].append(
                    f"Target node '{target_node}' requires field '{required_input}' which is missing"
                )
            else:
                validation_result["requirements_met"].append(required_input)
        
        # Check data quality metrics
        quality_checks = self._perform_quality_checks(state, target_node)
        validation_result.update(quality_checks)
        
        return validation_result
    
    def _perform_quality_checks(self, state, target_node: str) -> Dict[str, Any]:
        """Perform quality checks on state data"""
        
        quality_result = {
            "quality_score": 100,
            "quality_issues": [],
            "quality_warnings": []
        }
        
        # Node-specific quality checks
        if target_node == "content_writing":
            # Check if we have sufficient research data
            if hasattr(state, 'research_confidence') and state.research_confidence < 0.5:
                quality_result["quality_score"] -= 20
                quality_result["quality_warnings"].append("Low research confidence may affect content quality")
            
            if hasattr(state, 'primary_keywords') and len(state.primary_keywords) < 3:
                quality_result["quality_score"] -= 10
                quality_result["quality_warnings"].append("Limited keywords may affect SEO optimization")
        
        elif target_node == "seo_optimization":
            # Check content length for SEO
            if hasattr(state, 'word_count') and state.word_count < 300:
                quality_result["quality_score"] -= 30
                quality_result["quality_issues"].append("Content too short for effective SEO optimization")
        
        elif target_node == "quality_assurance":
            # Check if content has been properly optimized
            if not hasattr(state, 'seo_score') or state.seo_score < 60:
                quality_result["quality_score"] -= 25
                quality_result["quality_warnings"].append("Low SEO score may affect overall quality assessment")
        
        return quality_result
    
    def _create_state_snapshot(self, state) -> Dict[str, Any]:
        """Create a snapshot of current state for tracking"""
        
        try:
            # Convert state to dictionary for serialization
            if hasattr(state, '__dict__'):
                snapshot = copy.deepcopy(state.__dict__)
            else:
                snapshot = copy.deepcopy(asdict(state))
            
            # Add metadata about the snapshot
            snapshot["_snapshot_metadata"] = {
                "timestamp": datetime.now().isoformat(),
                "fields_count": len(snapshot),
                "snapshot_id": self._generate_snapshot_id()
            }
            
            return snapshot
            
        except Exception as e:
            print(f"⚠️ Failed to create state snapshot: {e}")
            return {"error": "snapshot_creation_failed"}
    
    def _update_handoff_metadata(self, state, handoff_record: StateHandoffRecord):
        """Update state with handoff metadata"""
        
        # Ensure metadata dictionary exists
        if not hasattr(state, 'metadata') or state.metadata is None:
            state.metadata = {}
        
        # Add handoff tracking
        if "handoff_history" not in state.metadata:
            state.metadata["handoff_history"] = []
        
        # Record this handoff
        handoff_summary = {
            "handoff_id": handoff_record.handoff_id,
            "source_node": handoff_record.source_node,
            "target_node": handoff_record.target_node,
            "timestamp": handoff_record.timestamp,
            "status": handoff_record.status.value,
            "processing_time": handoff_record.processing_time
        }
        
        state.metadata["handoff_history"].append(handoff_summary)
        
        # Update current workflow position
        state.metadata["current_node"] = handoff_record.target_node
        state.metadata["last_handoff"] = handoff_record.handoff_id
        
        return state
    
    def _generate_handoff_id(self, source_node: str, target_node: str) -> str:
        """Generate unique ID for handoff"""
        timestamp = datetime.now().isoformat()
        content = f"{source_node}→{target_node}→{timestamp}"
        return hashlib.md5(content.encode()).hexdigest()[:12]
    
    def _generate_snapshot_id(self) -> str:
        """Generate unique ID for state snapshot"""
        timestamp = datetime.now().isoformat()
        return hashlib.md5(timestamp.encode()).hexdigest()[:8]
    
    def _generate_state_checksum(self, state) -> str:
        """Generate checksum for state integrity verification"""
        try:
            state_str = json.dumps(asdict(state), sort_keys=True, default=str)
            return hashlib.sha256(state_str.encode()).hexdigest()[:16]
        except Exception:
            return "checksum_failed"
    
    def _extract_transferred_data(self, original_state, transformed_state) -> Dict[str, Any]:
        """Extract information about what data was transferred"""
        
        transferred_data = {
            "fields_modified": [],
            "fields_added": [],
            "fields_removed": [],
            "data_summary": {}
        }
        
        try:
            original_dict = asdict(original_state) if hasattr(original_state, '__dataclass_fields__') else original_state.__dict__
            transformed_dict = asdict(transformed_state) if hasattr(transformed_state, '__dataclass_fields__') else transformed_state.__dict__
            
            # Compare fields
            original_keys = set(original_dict.keys())
            transformed_keys = set(transformed_dict.keys())
            
            transferred_data["fields_added"] = list(transformed_keys - original_keys)
            transferred_data["fields_removed"] = list(original_keys - transformed_keys)
            
            # Check for modified fields
            common_keys = original_keys & transformed_keys
            for key in common_keys:
                if original_dict[key] != transformed_dict[key]:
                    transferred_data["fields_modified"].append(key)
            
            # Data summary
            transferred_data["data_summary"] = {
                "total_fields": len(transformed_keys),
                "modified_fields": len(transferred_data["fields_modified"]),
                "new_fields": len(transferred_data["fields_added"])
            }
            
        except Exception as e:
            transferred_data["error"] = f"Failed to extract transfer data: {e}"
        
        return transferred_data
    
    def _get_applied_transformations(self, source_node: str, target_node: str) -> List[str]:
        """Get list of transformations that were applied"""
        
        transition_key = f"{source_node}->{target_node}"
        transformation_functions = self.transformation_rules.get(transition_key, [])
        
        return [func.__name__ for func in transformation_functions]

    # =============================================================================
    # TRANSFORMATION FUNCTIONS
    # =============================================================================
    
    def _normalize_search_results(self, state):
        """Normalize search results format"""
        if hasattr(state, 'search_results') and state.search_results:
            normalized_results = []
            for result in state.search_results:
                if isinstance(result, dict):
                    normalized_result = {
                        "title": result.get("title", "").strip(),
                        "snippet": result.get("snippet", "").strip(),
                        "link": result.get("link", ""),
                        "source_quality": len(result.get("snippet", "")) > 100
                    }
                    normalized_results.append(normalized_result)
            
            state.search_results = normalized_results
        
        return state
    
    def _calculate_research_metrics(self, state):
        """Calculate additional research metrics"""
        if hasattr(state, 'search_results'):
            # Calculate research depth
            total_content_length = sum(
                len(result.get("snippet", "")) for result in state.search_results
            )
            
            # Add research metrics to metadata
            if not hasattr(state, 'metadata'):
                state.metadata = {}
            
            state.metadata["research_metrics"] = {
                "total_sources": len(state.search_results),
                "total_content_length": total_content_length,
                "avg_snippet_length": total_content_length / len(state.search_results) if state.search_results else 0,
                "quality_sources": sum(1 for r in state.search_results if r.get("source_quality", False))
            }
        
        return state
    
    def _extract_trending_indicators(self, state):
        """Extract trending indicators from research"""
        if hasattr(state, 'search_results') and state.search_results:
            trend_indicators = []
            current_year = datetime.now().year
            
            for result in state.search_results:
                title = result.get("title", "").lower()
                snippet = result.get("snippet", "").lower()
                
                # Look for trend indicators
                if any(indicator in title + snippet for indicator in [
                    str(current_year), "trend", "emerging", "future", "new", "latest"
                ]):
                    trend_indicators.append({
                        "title": result.get("title", ""),
                        "trend_strength": sum(1 for ind in ["trend", "emerging", "future"] if ind in title + snippet)
                    })
            
            state.trending_topics = [item["title"] for item in sorted(
                trend_indicators, key=lambda x: x["trend_strength"], reverse=True
            )[:5]]
        
        return state
    
    def _prioritize_keywords(self, state):
        """Prioritize keywords based on research data"""
        if hasattr(state, 'extracted_keywords') and state.extracted_keywords:
            # Simple prioritization based on frequency and relevance
            keyword_scores = {}
            
            for keyword in state.extracted_keywords:
                score = 1  # Base score
                
                # Boost score if keyword appears in topic
                if hasattr(state, 'topic') and keyword.lower() in state.topic.lower():
                    score += 2
                
                # Boost score based on research confidence
                if hasattr(state, 'research_confidence'):
                    score += state.research_confidence
                
                keyword_scores[keyword] = score
            
            # Sort keywords by score and take top ones
            sorted_keywords = sorted(keyword_scores.items(), key=lambda x: x[1], reverse=True)
            state.primary_keywords = [kw for kw, score in sorted_keywords[:5]]
        
        return state
    
    def _prepare_content_strategy(self, state):
        """Prepare content strategy based on research analysis"""
        if not hasattr(state, 'metadata'):
            state.metadata = {}
        
        # Determine content approach based on research quality
        research_confidence = getattr(state, 'research_confidence', 0.5)
        
        if research_confidence >= 0.8:
            content_approach = "comprehensive"
            content_depth = "detailed"
        elif research_confidence >= 0.6:
            content_approach = "balanced"
            content_depth = "moderate"
        else:
            content_approach = "focused"
            content_depth = "concise"
        
        state.metadata["content_strategy"] = {
            "approach": content_approach,
            "depth": content_depth,
            "research_confidence": research_confidence,
            "strategy_timestamp": datetime.now().isoformat()
        }
        
        return state
    
    def _calculate_content_targets(self, state):
        """Calculate content length and structure targets"""
        content_type = getattr(state, 'content_type', 'blog_post')
        
        # Content targets based on type
        targets = {
            "blog_post": {"min_words": 800, "max_words": 1500, "sections": 5},
            "social_media": {"min_words": 50, "max_words": 280, "sections": 3},
            "website_copy": {"min_words": 200, "max_words": 500, "sections": 4}
        }
        
        target_config = targets.get(content_type, targets["blog_post"])
        
        if not hasattr(state, 'metadata'):
            state.metadata = {}
        
        state.metadata["content_targets"] = target_config
        
        return state
    
    def _prepare_writing_context(self, state):
        """Prepare comprehensive context for content writing"""
        if not hasattr(state, 'metadata'):
            state.metadata = {}
        
        # Consolidate all relevant information for writing
        writing_context = {
            "topic": getattr(state, 'topic', ''),
            "content_type": getattr(state, 'content_type', 'blog_post'),
            "target_audience": getattr(state, 'target_audience', 'professionals'),
            "primary_keywords": getattr(state, 'primary_keywords', []),
            "research_summary": getattr(state, 'research_summary', ''),
            "content_outline": getattr(state, 'content_outline', ''),
            "content_sections": getattr(state, 'content_sections', []),
            "preparation_timestamp": datetime.now().isoformat()
        }
        
        state.metadata["writing_context"] = writing_context
        
        return state
    
    def _optimize_section_distribution(self, state):
        """Optimize distribution of content across sections"""
        if hasattr(state, 'content_sections') and state.content_sections:
            total_target_words = state.metadata.get("content_targets", {}).get("max_words", 1000)
            
            # Distribute words across sections based on importance
            section_weights = {
                "introduction": 0.15,
                "main_content": 0.50,
                "benefits": 0.20,
                "conclusion": 0.15
            }
            
            # Update section details with word targets
            for section in state.content_sections:
                section_name = section.get("section_name", "")
                weight = section_weights.get(section_name, 1.0 / len(state.content_sections))
                section["target_words"] = int(total_target_words * weight)
        
        return state
    
    def _prepare_keyword_integration_plan(self, state):
        """Prepare detailed keyword integration plan"""
        if hasattr(state, 'primary_keywords') and state.primary_keywords:
            if not hasattr(state, 'metadata'):
                state.metadata = {}
            
            keyword_plan = {
                "primary_keywords": state.primary_keywords[:3],
                "secondary_keywords": state.primary_keywords[3:7],
                "integration_strategy": {
                    "introduction": "primary keyword in first 100 words",
                    "body": "natural distribution of primary and secondary keywords",
                    "conclusion": "primary keyword reinforcement"
                },
                "density_targets": {
                    "primary": "1.5-2.0%",
                    "secondary": "0.5-1.0%"
                }
            }
            
            state.metadata["keyword_integration_plan"] = keyword_plan
        
        return state
    
    def _prepare_content_for_review(self, state):
        """Prepare content for review process"""
        if hasattr(state, 'draft_content'):
            # Calculate basic metrics
            word_count = len(state.draft_content.split())
            sentence_count = len([s for s in state.draft_content.split('.') if s.strip()])
            paragraph_count = len([p for p in state.draft_content.split('\n\n') if p.strip()])
            
            # Update state with calculated metrics
            state.word_count = word_count
            
            if not hasattr(state, 'metadata'):
                state.metadata = {}
            
            state.metadata["content_metrics"] = {
                "word_count": word_count,
                "sentence_count": sentence_count,
                "paragraph_count": paragraph_count,
                "avg_words_per_sentence": word_count / sentence_count if sentence_count > 0 else 0,
                "avg_sentences_per_paragraph": sentence_count / paragraph_count if paragraph_count > 0 else 0
            }
        
        return state
    
    def _calculate_basic_metrics(self, state):
        """Calculate basic content metrics"""
        if hasattr(state, 'draft_content'):
            content = state.draft_content
            
            # Character-level metrics
            char_count = len(content)
            char_count_no_spaces = len(content.replace(' ', ''))
            
            # Reading time estimation (average 200 words per minute)
            word_count = getattr(state, 'word_count', len(content.split()))
            estimated_reading_time = max(1, word_count / 200)
            
            if not hasattr(state, 'metadata'):
                state.metadata = {}
            
            state.metadata["basic_metrics"] = {
                "character_count": char_count,
                "character_count_no_spaces": char_count_no_spaces,
                "estimated_reading_time_minutes": estimated_reading_time,
                "metrics_calculated_at": datetime.now().isoformat()
            }
        
        return state
    
    def _extract_content_characteristics(self, state):
        """Extract content characteristics for further processing"""
        if hasattr(state, 'draft_content'):
            content = state.draft_content.lower()
            
            # Analyze content characteristics
            characteristics = {
                "has_questions": "?" in content,
                "has_lists": any(indicator in content for indicator in ["\n-", "\n*", "\n1.", "\n2."]),
                "has_technical_terms": any(term in content for term in ["api", "system", "process", "technology", "implementation"]),
                "tone_indicators": {
                    "formal": sum(1 for word in ["furthermore", "therefore", "consequently"] if word in content),
                    "casual": sum(1 for word in ["you", "your", "we", "our"] if word in content),
                    "technical": sum(1 for word in ["configure", "optimize", "implement"] if word in content)
                }
            }
            
            if not hasattr(state, 'metadata'):
                state.metadata = {}
            
            state.metadata["content_characteristics"] = characteristics
        
        return state
    
    def _prepare_seo_context(self, state):
        """Prepare context for SEO optimization"""
        seo_context = {
            "content_length": getattr(state, 'word_count', 0),
            "primary_keywords": getattr(state, 'primary_keywords', []),
            "content_type": getattr(state, 'content_type', 'blog_post'),
            "target_audience": getattr(state, 'target_audience', ''),
            "existing_meta": {
                "title": getattr(state, 'topic', ''),
                "description": getattr(state, 'research_summary', '')[:160]
            }
        }
        
        if not hasattr(state, 'metadata'):
            state.metadata = {}
        
        state.metadata["seo_context"] = seo_context
        
        return state
    
    def _extract_content_structure(self, state):
        """Extract content structure for SEO analysis"""
        if hasattr(state, 'draft_content'):
            content = state.draft_content
            
            # Analyze heading structure
            h1_count = content.count('\n# ') + (1 if content.startswith('# ') else 0)
            h2_count = content.count('\n## ') + (1 if content.startswith('## ') else 0)
            h3_count = content.count('\n### ') + (1 if content.startswith('### ') else 0)
            
            structure_analysis = {
                "heading_counts": {
                    "h1": h1_count,
                    "h2": h2_count,
                    "h3": h3_count
                },
                "paragraph_count": len([p for p in content.split('\n\n') if p.strip()]),
                "has_introduction": any(word in content.lower()[:200] for word in ["introduction", "overview"]),
                "has_conclusion": any(word in content.lower()[-200:] for word in ["conclusion", "summary"])
            }
            
            if not hasattr(state, 'metadata'):
                state.metadata = {}
            
            state.metadata["structure_analysis"] = structure_analysis
        
        return state
    
    def _prepare_keyword_data(self, state):
        """Prepare keyword data for SEO optimization"""
        if hasattr(state, 'primary_keywords'):
            keyword_data = {
                "primary_keywords": state.primary_keywords[:3],
                "secondary_keywords": getattr(state, 'extracted_keywords', [])[5:10],
                "long_tail_opportunities": [],
                "semantic_variations": {}
            }
            
            # Generate long-tail opportunities
            topic = getattr(state, 'topic', '')
            if topic:
                keyword_data["long_tail_opportunities"] = [
                    f"how to {topic.lower()}",
                    f"{topic.lower()} benefits",
                    f"best {topic.lower()} practices"
                ]
            
            # Generate semantic variations
            for keyword in keyword_data["primary_keywords"]:
                variations = []
                if keyword.endswith('s'):
                    variations.append(keyword[:-1])
                else:
                    variations.append(keyword + 's')
                
                keyword_data["semantic_variations"][keyword] = variations
            
            if not hasattr(state, 'metadata'):
                state.metadata = {}
            
            state.metadata["keyword_data"] = keyword_data
        
        return state
    
    def _prepare_qa_context(self, state):
        """Prepare context for quality assurance"""
        qa_context = {
            "content_length": getattr(state, 'word_count', 0),
            "seo_score": getattr(state, 'seo_score', 0),
            "content_type": getattr(state, 'content_type', 'blog_post'),
            "quality_criteria": {
                "min_word_count": 300,
                "min_seo_score": 70,
                "required_elements": ["introduction", "conclusion"],
                "max_revision_cycles": 2
            },
            "revision_count": getattr(state, 'revision_count', 0)
        }
        
        if not hasattr(state, 'metadata'):
            state.metadata = {}
        
        state.metadata["qa_context"] = qa_context
        
        return state
    
    def _consolidate_content_versions(self, state):
        """Consolidate different versions of content"""
        # Determine the best content version to use
        final_content = None
        
        if hasattr(state, 'optimized_content') and state.optimized_content:
            final_content = state.optimized_content
        elif hasattr(state, 'draft_content') and state.draft_content:
            final_content = state.draft_content
        
        if final_content:
            state.final_content = final_content
            
            # Update word count if needed
            if not hasattr(state, 'word_count') or state.word_count == 0:
                state.word_count = len(final_content.split())
        
        return state
    
    def _prepare_quality_criteria(self, state):
        """Prepare quality criteria for assessment"""
        content_type = getattr(state, 'content_type', 'blog_post')
        
        # Define quality criteria based on content type
        criteria_sets = {
            "blog_post": {
                "min_word_count": 800,
                "max_word_count": 1500,
                "required_sections": ["introduction", "main_content", "conclusion"],
                "seo_requirements": {"min_score": 75, "keyword_density": "1-2%"},
                "readability": {"max_complexity": 70, "min_readability": 60}
            },
            "social_media": {
                "min_word_count": 50,
                "max_word_count": 280,
                "required_sections": ["hook", "value", "cta"],
                "seo_requirements": {"min_score": 60, "keyword_density": "2-3%"},
                "readability": {"max_complexity": 50, "min_readability": 70}
            },
            "website_copy": {
                "min_word_count": 200,
                "max_word_count": 500,
                "required_sections": ["headline", "benefits", "cta"],
                "seo_requirements": {"min_score": 70, "keyword_density": "1.5-2.5%"},
                "readability": {"max_complexity": 60, "min_readability": 65}
            }
        }
        
        quality_criteria = criteria_sets.get(content_type, criteria_sets["blog_post"])
        
        if not hasattr(state, 'metadata'):
            state.metadata = {}
        
        state.metadata["quality_criteria"] = quality_criteria
        
        return state
    
    def _analyze_quality_gaps(self, state):
        """Analyze gaps in content quality"""
        quality_feedback = getattr(state, 'quality_feedback', [])
        quality_score = getattr(state, 'quality_score', 0)
        
        # Categorize quality issues
        gap_analysis = {
            "structure_gaps": [],
            "content_gaps": [],
            "seo_gaps": [],
            "readability_gaps": [],
            "priority_gaps": []
        }
        
        for feedback in quality_feedback:
            feedback_lower = feedback.lower()
            
            if any(term in feedback_lower for term in ["structure", "section", "heading"]):
                gap_analysis["structure_gaps"].append(feedback)
            elif any(term in feedback_lower for term in ["keyword", "seo", "optimization"]):
                gap_analysis["seo_gaps"].append(feedback)
            elif any(term in feedback_lower for term in ["length", "word", "sentence"]):
                gap_analysis["readability_gaps"].append(feedback)
            else:
                gap_analysis["content_gaps"].append(feedback)
        
        # Determine priority gaps based on quality score
        if quality_score < 60:
            gap_analysis["priority_gaps"] = gap_analysis["structure_gaps"] + gap_analysis["content_gaps"]
        elif quality_score < 75:
            gap_analysis["priority_gaps"] = gap_analysis["seo_gaps"] + gap_analysis["readability_gaps"]
        
        if not hasattr(state, 'metadata'):
            state.metadata = {}
        
        state.metadata["gap_analysis"] = gap_analysis
        
        return state
    
    def _prioritize_improvements(self, state):
        """Prioritize improvements based on impact and effort"""
        gap_analysis = state.metadata.get("gap_analysis", {})
        
        improvement_priorities = {
            "high_impact_low_effort": [],
            "high_impact_high_effort": [],
            "low_impact_low_effort": [],
            "critical_fixes": []
        }
        
        # Map gaps to improvement priorities
        structure_gaps = gap_analysis.get("structure_gaps", [])
        content_gaps = gap_analysis.get("content_gaps", [])
        seo_gaps = gap_analysis.get("seo_gaps", [])
        readability_gaps = gap_analysis.get("readability_gaps", [])
        
        # High impact, low effort improvements
        improvement_priorities["high_impact_low_effort"].extend([
            "Fix keyword integration" if seo_gaps else None,
            "Improve paragraph structure" if readability_gaps else None
        ])
        
        # High impact, high effort improvements
        improvement_priorities["high_impact_high_effort"].extend([
            "Restructure content sections" if structure_gaps else None,
            "Expand content significantly" if "length" in str(content_gaps).lower() else None
        ])
        
        # Critical fixes (must be addressed)
        if getattr(state, 'quality_score', 100) < 50:
            improvement_priorities["critical_fixes"].extend(content_gaps + structure_gaps)
        
        # Remove None values
        for category in improvement_priorities:
            improvement_priorities[category] = [item for item in improvement_priorities[category] if item]
        
        state.metadata["improvement_priorities"] = improvement_priorities
        
        return state
    
    def _prepare_revision_strategy(self, state):
        """Prepare comprehensive revision strategy"""
        improvement_priorities = state.metadata.get("improvement_priorities", {})
        revision_count = getattr(state, 'revision_count', 0)
        
        # Create revision strategy based on priorities and revision count
        revision_strategy = {
            "revision_type": "targeted" if revision_count == 0 else "comprehensive",
            "focus_areas": [],
            "specific_actions": [],
            "success_criteria": {},
            "estimated_effort": "medium"
        }
        
        # Determine focus areas
        if improvement_priorities.get("critical_fixes"):
            revision_strategy["focus_areas"].extend(["critical_issues", "structural_problems"])
            revision_strategy["estimated_effort"] = "high"
        
        if improvement_priorities.get("high_impact_low_effort"):
            revision_strategy["focus_areas"].extend(["quick_wins", "optimization_tweaks"])
        
        # Define specific actions
        revision_strategy["specific_actions"] = [
            "Address critical quality issues",
            "Improve content structure and flow",
            "Enhance keyword integration",
            "Optimize readability and engagement"
        ]
        
        # Set success criteria
        current_quality_score = getattr(state, 'quality_score', 0)
        target_improvement = 20 if current_quality_score < 60 else 10
        
        revision_strategy["success_criteria"] = {
            "min_quality_improvement": target_improvement,
            "target_quality_score": min(100, current_quality_score + target_improvement),
            "max_revision_cycles": 2
        }
        
        state.metadata["revision_strategy"] = revision_strategy
        
        return state
    
    def _prepare_final_output(self, state):
        """Prepare final output package"""
        # Consolidate all final content and metadata
        final_output = {
            "content": getattr(state, 'final_content', ''),
            "metadata": getattr(state, 'metadata', {}),
            "quality_metrics": {
                "quality_score": getattr(state, 'quality_score', 0),
                "seo_score": getattr(state, 'seo_score', 0),
                "word_count": getattr(state, 'word_count', 0)
            },
            "seo_data": {
                "meta_description": getattr(state, 'meta_description', ''),
                "title_suggestions": getattr(state, 'title_suggestions', []),
                "primary_keywords": getattr(state, 'primary_keywords', [])
            }
        }
        
        state.metadata["final_output"] = final_output
        
        return state
    
    def _calculate_final_metrics(self, state):
        """Calculate final performance metrics"""
        # Calculate processing times
        handoff_history = state.metadata.get("handoff_history", [])
        total_processing_time = sum(h.get("processing_time", 0) for h in handoff_history)
        
        # Calculate workflow efficiency
        total_handoffs = len(handoff_history)
        successful_handoffs = sum(1 for h in handoff_history if h.get("status") == "success")
        
        final_metrics = {
            "total_processing_time": total_processing_time,
            "total_handoffs": total_handoffs,
            "successful_handoffs": successful_handoffs,
            "workflow_efficiency": (successful_handoffs / total_handoffs) * 100 if total_handoffs > 0 else 0,
            "revision_cycles": getattr(state, 'revision_count', 0),
            "final_quality_score": getattr(state, 'quality_score', 0),
            "completion_timestamp": datetime.now().isoformat()
        }
        
        state.metadata["final_metrics"] = final_metrics
        
        return state
    
    def _prepare_success_summary(self, state):
        """Prepare success summary for workflow completion"""
        final_metrics = state.metadata.get("final_metrics", {})
        
        success_summary = {
            "workflow_status": "completed_successfully",
            "quality_achievement": "excellent" if final_metrics.get("final_quality_score", 0) >= 85 else "good",
            "efficiency_rating": "high" if final_metrics.get("workflow_efficiency", 0) >= 90 else "medium",
            "content_delivered": bool(getattr(state, 'final_content', '')),
            "metadata_complete": bool(state.metadata),
            "seo_optimized": bool(getattr(state, 'seo_score', 0) >= 70),
            "revision_cycles_used": final_metrics.get("revision_cycles", 0),
            "summary_generated_at": datetime.now().isoformat()
        }
        
        state.metadata["success_summary"] = success_summary
        
        return state

    # =============================================================================
    # MONITORING AND REPORTING METHODS
    # =============================================================================
    
    def get_handoff_analytics(self) -> Dict[str, Any]:
        """Get analytics about all handoffs"""
        
        if not self.handoff_history:
            return {"message": "No handoffs recorded yet"}
        
        analytics = {
            "total_handoffs": len(self.handoff_history),
            "success_rate": len([h for h in self.handoff_history if h.status == HandoffStatus.SUCCESS]) / len(self.handoff_history),
            "average_processing_time": sum(h.processing_time for h in self.handoff_history) / len(self.handoff_history),
            "most_common_transitions": {},
            "error_patterns": {},
            "performance_trends": []
        }
        
        # Analyze transition patterns
        transitions = {}
        for handoff in self.handoff_history:
            transition = f"{handoff.source_node}->{handoff.target_node}"
            transitions[transition] = transitions.get(transition, 0) + 1
        
        analytics["most_common_transitions"] = dict(sorted(transitions.items(), key=lambda x: x[1], reverse=True))
        
        # Analyze error patterns
        error_handoffs = [h for h in self.handoff_history if h.status in [HandoffStatus.FAILURE, HandoffStatus.VALIDATION_ERROR]]
        for handoff in error_handoffs:
            for error in handoff.errors:
                analytics["error_patterns"][error] = analytics["error_patterns"].get(error, 0) + 1
        
        return analytics
    
    def get_workflow_health_report(self) -> Dict[str, Any]:
        """Generate workflow health report"""
        
        recent_handoffs = self.handoff_history[-10:] if len(self.handoff_history) >= 10 else self.handoff_history
        
        if not recent_handoffs:
            return {"status": "no_data", "message": "No recent handoffs to analyze"}
        
        health_report = {
            "overall_health": "healthy",
            "success_rate": len([h for h in recent_handoffs if h.status == HandoffStatus.SUCCESS]) / len(recent_handoffs),
            "average_processing_time": sum(h.processing_time for h in recent_handoffs) / len(recent_handoffs),
            "warning_indicators": [],
            "performance_issues": [],
            "recommendations": []
        }
        
        # Assess health indicators
        if health_report["success_rate"] < 0.8:
            health_report["overall_health"] = "warning"
            health_report["warning_indicators"].append("Low success rate")
        
        if health_report["average_processing_time"] > 5.0:
            health_report["performance_issues"].append("High processing times")
        
        # Generate recommendations
        if health_report["success_rate"] < 0.9:
            health_report["recommendations"].append("Review validation rules for frequent failures")
        
        if health_report["average_processing_time"] > 3.0:
            health_report["recommendations"].append("Optimize transformation functions for better performance")
        
        return health_report

if __name__ == "__main__":
    # Test the state handoff manager
    print("State Handoff Manager - Ready for Integration")