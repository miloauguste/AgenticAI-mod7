"""
Enhanced Agent Implementations for LangGraph Content Creation Workflow
Comprehensive node functions with sophisticated processing logic
"""

import os
import re
import json
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
import random
from collections import Counter

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate

from research_tool import research_tool
from writing_tool import writing_tool
from SEO_tool import seo_tool
from config import Config

class AdvancedContentAgents:
    """
    Enhanced agent implementations with sophisticated processing capabilities
    """
    
    def __init__(self):
        self.llm = ChatOpenAI(temperature=0.7, model="gpt-3.5-turbo")
        self.analytical_llm = ChatOpenAI(temperature=0.1, model="gpt-3.5-turbo")  # Lower temp for analysis
        
        # Content quality indicators
        self.quality_keywords = {
            "technology": ["innovation", "digital", "automation", "AI", "machine learning", "data", "cloud"],
            "business": ["growth", "efficiency", "ROI", "productivity", "scalability", "optimization"],
            "trends": ["2024", "future", "emerging", "next-generation", "cutting-edge", "revolutionary"]
        }
        
        # Writing style templates
        self.style_templates = {
            "professional": {
                "tone": "formal and authoritative",
                "vocabulary": "industry-specific terminology",
                "structure": "logical progression with clear sections"
            },
            "engaging": {
                "tone": "conversational yet informative",
                "vocabulary": "accessible language with strategic jargon",
                "structure": "hook-driven with storytelling elements"
            },
            "persuasive": {
                "tone": "compelling and action-oriented",
                "vocabulary": "benefit-focused language",
                "structure": "problem-solution-action format"
            }
        }

    # =============================================================================
    # INITIALIZATION AND SETUP AGENTS
    # =============================================================================
    
    def initialize_workflow_enhanced(self, state) -> Dict[str, Any]:
        """
        ENHANCED: Initialize Workflow
        AGENT: System Coordinator
        PURPOSE: Advanced setup with intelligent parameter optimization
        """
        print("🚀 ENHANCED WORKFLOW INITIALIZATION")
        state.current_agent = "system_coordinator"
        state.workflow_stage = "initialization"
        start_time = datetime.now()
        
        try:
            # Validate and enhance inputs
            if not state.topic:
                state.error_messages.append("Topic is required for content generation")
                return state
            
            # Intelligent content type configuration
            content_configs = {
                "blog_post": {
                    "min_words": 800, "max_words": 1500, "style": "professional",
                    "sections": ["introduction", "main_content", "benefits", "conclusion"],
                    "seo_priority": "high", "readability_level": "professional"
                },
                "social_media": {
                    "min_words": 50, "max_words": 280, "style": "engaging", 
                    "sections": ["hook", "value_prop", "cta"],
                    "seo_priority": "medium", "readability_level": "casual"
                },
                "website_copy": {
                    "min_words": 200, "max_words": 500, "style": "persuasive",
                    "sections": ["headline", "benefits", "social_proof", "cta"],
                    "seo_priority": "high", "readability_level": "accessible"
                }
            }
            
            config = content_configs.get(state.content_type, content_configs["blog_post"])
            
            # Set intelligent defaults based on topic analysis
            topic_keywords = self._extract_topic_keywords(state.topic)
            industry_context = self._determine_industry_context(state.topic)
            
            # Enhanced metadata initialization
            state.metadata.update({
                "workflow_start": start_time.isoformat(),
                "content_config": config,
                "topic_keywords": topic_keywords,
                "industry_context": industry_context,
                "target_min_words": config["min_words"],
                "target_max_words": config["max_words"],
                "writing_style": config["style"],
                "seo_priority": config["seo_priority"],
                "readability_target": config["readability_level"],
                "expected_sections": config["sections"]
            })
            
            # Set writing style and parameters
            state.writing_style = config["style"]
            
            # Initialize quality thresholds based on content type
            if state.content_type == "blog_post":
                state.metadata["quality_threshold"] = 85
            elif state.content_type == "social_media":
                state.metadata["quality_threshold"] = 75
            else:  # website_copy
                state.metadata["quality_threshold"] = 80
            
            print(f"✅ Enhanced initialization complete")
            print(f"   📝 Content Type: {state.content_type}")
            print(f"   🎯 Target Words: {config['min_words']}-{config['max_words']}")
            print(f"   📊 Quality Threshold: {state.metadata['quality_threshold']}")
            
        except Exception as e:
            state.error_messages.append(f"Initialization error: {str(e)}")
            print(f"❌ Initialization failed: {e}")
        
        state.processing_time["initialization"] = (datetime.now() - start_time).total_seconds()
        return state
    
    def _extract_topic_keywords(self, topic: str) -> List[str]:
        """Extract key terms from the topic for better content focus"""
        # Simple keyword extraction (in production, use NLP libraries like spaCy)
        words = re.findall(r'\b\w+\b', topic.lower())
        
        # Filter out common words and extract meaningful terms
        stop_words = {'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
        keywords = [word for word in words if len(word) > 3 and word not in stop_words]
        
        return keywords[:5]  # Return top 5 keywords
    
    def _determine_industry_context(self, topic: str) -> str:
        """Determine industry context from topic"""
        topic_lower = topic.lower()
        
        contexts = {
            "technology": ["ai", "artificial intelligence", "machine learning", "automation", "digital", "tech", "software"],
            "business": ["business", "startup", "entrepreneur", "growth", "strategy", "marketing"],
            "finance": ["fintech", "finance", "banking", "investment", "cryptocurrency", "blockchain"],
            "healthcare": ["health", "medical", "healthcare", "telemedicine", "wellness"],
            "education": ["education", "learning", "training", "e-learning", "edtech"]
        }
        
        for context, keywords in contexts.items():
            if any(keyword in topic_lower for keyword in keywords):
                return context
        
        return "general"

    # =============================================================================
    # RESEARCH AND ANALYSIS AGENTS
    # =============================================================================
    
    def research_agent_enhanced(self, state) -> Dict[str, Any]:
        """
        ENHANCED: Research Agent
        AGENT: Research Specialist
        PURPOSE: Comprehensive research with intelligent data processing
        """
        print("🔍 ENHANCED RESEARCH AGENT ACTIVE")
        state.current_agent = "research_specialist"
        state.workflow_stage = "research"
        start_time = datetime.now()
        
        # Increment iteration counter
        state.agent_iterations["research"] = state.agent_iterations.get("research", 0) + 1
        
        try:
            # Build sophisticated research strategy
            research_strategy = self._build_research_strategy(state)
            
            # Execute multi-dimensional research
            research_results = self._execute_comprehensive_research(state, research_strategy)
            
            # Process and analyze research data
            processed_data = self._process_research_data(research_results)
            
            # Update state with comprehensive research data
            state.research_query = research_strategy["primary_query"]
            state.search_results = research_results.get("search_results", [])
            state.trending_topics = processed_data.get("trending_topics", [])
            state.extracted_keywords = processed_data.get("keywords", [])
            state.research_summary = processed_data.get("summary", "")
            state.research_confidence = processed_data.get("confidence", 0.0)
            
            # Advanced research metrics
            state.metadata.update({
                "research_strategy": research_strategy,
                "research_metrics": {
                    "sources_found": len(state.search_results),
                    "keywords_extracted": len(state.extracted_keywords),
                    "trending_topics": len(state.trending_topics),
                    "confidence_score": state.research_confidence,
                    "research_depth": processed_data.get("depth_score", 0)
                }
            })
            
            print(f"📊 Research completed:")
            print(f"   🔍 Sources: {len(state.search_results)}")
            print(f"   🎯 Keywords: {len(state.extracted_keywords)}")
            print(f"   📈 Confidence: {state.research_confidence:.2f}")
            
        except Exception as e:
            state.error_messages.append(f"Research error: {str(e)}")
            state.research_confidence = 0.0
            print(f"❌ Research failed: {e}")
        
        state.processing_time["research"] = (datetime.now() - start_time).total_seconds()
        return state
    
    def _build_research_strategy(self, state) -> Dict[str, Any]:
        """Build intelligent research strategy based on topic and context"""
        
        base_topic = state.topic
        industry_context = state.metadata.get("industry_context", "general")
        content_type = state.content_type
        
        # Build multi-layered search queries
        primary_query = f"{base_topic} {industry_context} 2024 trends"
        
        secondary_queries = [
            f"{base_topic} benefits applications",
            f"{base_topic} implementation guide",
            f"{base_topic} case studies examples",
            f"{base_topic} future outlook predictions"
        ]
        
        # Adapt strategy based on content type
        if content_type == "blog_post":
            focus_areas = ["detailed_analysis", "case_studies", "future_trends"]
        elif content_type == "social_media":
            focus_areas = ["quick_insights", "statistics", "engaging_facts"]
        else:  # website_copy
            focus_areas = ["benefits", "social_proof", "competitive_advantages"]
        
        return {
            "primary_query": primary_query,
            "secondary_queries": secondary_queries,
            "focus_areas": focus_areas,
            "industry_context": industry_context,
            "search_depth": "comprehensive" if content_type == "blog_post" else "targeted"
        }
    
    def _execute_comprehensive_research(self, state, strategy: Dict[str, Any]) -> Dict[str, Any]:
        """Execute research using multiple strategies and sources"""
        
        all_results = []
        
        try:
            # Primary research
            print(f"🔎 Primary search: {strategy['primary_query']}")
            primary_results = research_tool.run(strategy["primary_query"])
            
            if isinstance(primary_results, list):
                all_results.extend(primary_results)
            
            # Secondary research for comprehensive coverage
            if strategy["search_depth"] == "comprehensive" and len(all_results) < 3:
                for secondary_query in strategy["secondary_queries"][:2]:
                    print(f"🔍 Secondary search: {secondary_query}")
                    secondary_results = research_tool.run(secondary_query)
                    if isinstance(secondary_results, list):
                        all_results.extend(secondary_results[:2])  # Limit secondary results
            
        except Exception as e:
            print(f"⚠️ Research execution error: {e}")
        
        return {
            "search_results": all_results,
            "strategy_used": strategy
        }
    
    def _process_research_data(self, research_results: Dict[str, Any]) -> Dict[str, Any]:
        """Process and analyze research data for insights"""
        
        search_results = research_results.get("search_results", [])
        
        if not search_results:
            return {
                "summary": "No research data available",
                "confidence": 0.0,
                "keywords": [],
                "trending_topics": [],
                "depth_score": 0
            }
        
        # Extract and analyze text content
        all_text = ""
        for result in search_results:
            title = result.get("title", "")
            snippet = result.get("snippet", "")
            all_text += f"{title} {snippet} "
        
        # Keyword extraction and frequency analysis
        keywords = self._extract_keywords_from_text(all_text)
        
        # Trending topic identification
        trending_topics = self._identify_trending_topics(search_results)
        
        # Generate research summary
        summary = self._generate_research_summary(search_results, keywords)
        
        # Calculate confidence score
        confidence = self._calculate_research_confidence(search_results, keywords)
        
        # Depth score based on content richness
        depth_score = min(len(search_results) * 10 + len(keywords) * 2, 100)
        
        return {
            "summary": summary,
            "confidence": confidence,
            "keywords": keywords,
            "trending_topics": trending_topics,
            "depth_score": depth_score,
            "text_analyzed": len(all_text)
        }
    
    def _extract_keywords_from_text(self, text: str) -> List[str]:
        """Enhanced keyword extraction from research text"""
        
        # Clean and normalize text
        text_lower = text.lower()
        words = re.findall(r'\b\w+\b', text_lower)
        
        # Filter relevant terms
        stop_words = {'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'a', 'an'}
        meaningful_words = [word for word in words if len(word) > 3 and word not in stop_words]
        
        # Count frequency and get top keywords
        word_freq = Counter(meaningful_words)
        top_keywords = [word for word, freq in word_freq.most_common(10) if freq > 1]
        
        # Add domain-specific keywords
        domain_keywords = []
        for category, keywords in self.quality_keywords.items():
            for keyword in keywords:
                if keyword.lower() in text_lower:
                    domain_keywords.append(keyword)
        
        # Combine and deduplicate
        all_keywords = list(set(top_keywords + domain_keywords))
        return all_keywords[:15]  # Return top 15 keywords
    
    def _identify_trending_topics(self, search_results: List[Dict]) -> List[str]:
        """Identify trending topics from search results"""
        
        trending_indicators = ["2024", "trend", "emerging", "new", "latest", "future", "next"]
        trending_topics = []
        
        for result in search_results:
            title = result.get("title", "").lower()
            snippet = result.get("snippet", "").lower()
            
            if any(indicator in title or indicator in snippet for indicator in trending_indicators):
                # Extract the main topic from title
                clean_title = re.sub(r'\d{4}', '', result.get("title", ""))  # Remove years
                clean_title = re.sub(r'[^\w\s]', '', clean_title)  # Remove special chars
                if len(clean_title.strip()) > 10:
                    trending_topics.append(clean_title.strip())
        
        return trending_topics[:5]  # Return top 5 trending topics
    
    def _generate_research_summary(self, search_results: List[Dict], keywords: List[str]) -> str:
        """Generate intelligent research summary"""
        
        if not search_results:
            return "No research data available for analysis."
        
        summary_parts = [
            f"Research analysis of {len(search_results)} sources reveals key insights.",
            f"Primary themes include: {', '.join(keywords[:5])}.",
        ]
        
        # Add source quality assessment
        if len(search_results) >= 5:
            summary_parts.append("Comprehensive source coverage provides high-confidence insights.")
        elif len(search_results) >= 3:
            summary_parts.append("Good source diversity supports reliable content development.")
        else:
            summary_parts.append("Limited sources available; additional research may be beneficial.")
        
        return " ".join(summary_parts)
    
    def _calculate_research_confidence(self, search_results: List[Dict], keywords: List[str]) -> float:
        """Calculate confidence score for research quality"""
        
        confidence_factors = {
            "source_count": min(len(search_results) / 5.0, 1.0) * 0.4,  # 40% weight
            "keyword_richness": min(len(keywords) / 10.0, 1.0) * 0.3,   # 30% weight
            "content_quality": self._assess_content_quality(search_results) * 0.3  # 30% weight
        }
        
        total_confidence = sum(confidence_factors.values())
        return min(total_confidence, 1.0)
    
    def _assess_content_quality(self, search_results: List[Dict]) -> float:
        """Assess the quality of research content"""
        
        if not search_results:
            return 0.0
        
        quality_indicators = 0
        total_results = len(search_results)
        
        for result in search_results:
            title = result.get("title", "").lower()
            snippet = result.get("snippet", "").lower()
            
            # Check for quality indicators
            if len(snippet) > 100:  # Substantial content
                quality_indicators += 1
            if any(word in title + snippet for word in ["guide", "analysis", "report", "study"]):
                quality_indicators += 1
            if "2024" in title + snippet:  # Recent content
                quality_indicators += 1
        
        return min(quality_indicators / (total_results * 2), 1.0)

    def analyze_research_enhanced(self, state) -> Dict[str, Any]:
        """
        ENHANCED: Analyze Research
        AGENT: Research Analyst
        PURPOSE: Advanced research quality assessment and strategic planning
        """
        print("📊 ENHANCED RESEARCH ANALYSIS")
        state.current_agent = "research_analyst"
        state.workflow_stage = "research_analysis"
        start_time = datetime.now()
        
        try:
            # Comprehensive research quality assessment
            quality_assessment = self._comprehensive_research_assessment(state)
            
            # Strategic content planning based on research
            content_strategy = self._develop_content_strategy(state, quality_assessment)
            
            # Research gap analysis
            gap_analysis = self._analyze_research_gaps(state)
            
            # Update state with analysis results
            state.metadata.update({
                "research_assessment": quality_assessment,
                "content_strategy": content_strategy,
                "research_gaps": gap_analysis,
                "analysis_timestamp": datetime.now().isoformat()
            })
            
            # Determine trending topics with priority scoring
            state.trending_topics = self._prioritize_trending_topics(state)
            
            print(f"🎯 Research analysis complete:")
            print(f"   📊 Quality Score: {quality_assessment['overall_score']:.2f}")
            print(f"   🎯 Strategy: {content_strategy['approach']}")
            print(f"   📈 Trending Topics: {len(state.trending_topics)}")
            
        except Exception as e:
            state.error_messages.append(f"Research analysis error: {str(e)}")
            print(f"❌ Analysis failed: {e}")
        
        state.processing_time["research_analysis"] = (datetime.now() - start_time).total_seconds()
        return state
    
    def _comprehensive_research_assessment(self, state) -> Dict[str, Any]:
        """Comprehensive assessment of research quality and completeness"""
        
        assessment = {
            "source_quality": 0.0,
            "content_depth": 0.0,
            "keyword_relevance": 0.0,
            "trend_coverage": 0.0,
            "overall_score": 0.0
        }
        
        # Source quality assessment
        if state.search_results:
            source_score = min(len(state.search_results) / 5.0, 1.0)
            content_richness = sum(1 for result in state.search_results if len(result.get("snippet", "")) > 100)
            assessment["source_quality"] = (source_score + content_richness / len(state.search_results)) / 2
        
        # Content depth assessment
        total_content = sum(len(result.get("snippet", "")) for result in state.search_results)
        assessment["content_depth"] = min(total_content / 1000, 1.0)  # Normalize to 1000 chars
        
        # Keyword relevance assessment
        topic_keywords = set(state.metadata.get("topic_keywords", []))
        extracted_keywords = set(state.extracted_keywords)
        keyword_overlap = len(topic_keywords.intersection(extracted_keywords))
        assessment["keyword_relevance"] = keyword_overlap / max(len(topic_keywords), 1)
        
        # Trend coverage assessment
        assessment["trend_coverage"] = min(len(state.trending_topics) / 3.0, 1.0)
        
        # Calculate overall score
        weights = {"source_quality": 0.3, "content_depth": 0.25, "keyword_relevance": 0.25, "trend_coverage": 0.2}
        assessment["overall_score"] = sum(assessment[key] * weights[key] for key in weights)
        
        return assessment
    
    def _develop_content_strategy(self, state, quality_assessment: Dict[str, Any]) -> Dict[str, Any]:
        """Develop content strategy based on research analysis"""
        
        overall_score = quality_assessment["overall_score"]
        content_type = state.content_type
        
        # Determine content approach based on research quality
        if overall_score >= 0.8:
            approach = "comprehensive"
            depth_level = "detailed"
        elif overall_score >= 0.6:
            approach = "balanced"
            depth_level = "moderate"
        else:
            approach = "focused"
            depth_level = "concise"
        
        # Content structure recommendations
        if content_type == "blog_post":
            if approach == "comprehensive":
                sections = ["introduction", "background", "main_analysis", "case_studies", "future_outlook", "conclusion"]
            elif approach == "balanced":
                sections = ["introduction", "key_points", "benefits", "implementation", "conclusion"]
            else:
                sections = ["introduction", "main_points", "conclusion"]
        elif content_type == "social_media":
            sections = ["hook", "key_insight", "call_to_action"]
        else:  # website_copy
            sections = ["headline", "value_proposition", "benefits", "social_proof", "call_to_action"]
        
        # Keyword integration strategy
        primary_keywords = state.extracted_keywords[:5]
        secondary_keywords = state.extracted_keywords[5:10]
        
        return {
            "approach": approach,
            "depth_level": depth_level,
            "recommended_sections": sections,
            "primary_keywords": primary_keywords,
            "secondary_keywords": secondary_keywords,
            "tone_recommendation": self._recommend_tone(state, quality_assessment),
            "length_recommendation": self._recommend_length(state, approach)
        }
    
    def _analyze_research_gaps(self, state) -> Dict[str, Any]:
        """Analyze gaps in research coverage"""
        
        gaps = {
            "missing_perspectives": [],
            "insufficient_data": [],
            "recommendations": []
        }
        
        # Check for common content gaps
        content_areas = ["benefits", "challenges", "implementation", "costs", "alternatives"]
        covered_areas = []
        
        all_text = " ".join([
            result.get("title", "") + " " + result.get("snippet", "")
            for result in state.search_results
        ]).lower()
        
        for area in content_areas:
            area_keywords = {
                "benefits": ["benefit", "advantage", "positive", "gain"],
                "challenges": ["challenge", "problem", "difficulty", "issue"],
                "implementation": ["implement", "deploy", "setup", "install"],
                "costs": ["cost", "price", "expense", "budget"],
                "alternatives": ["alternative", "option", "choice", "competitor"]
            }
            
            if any(keyword in all_text for keyword in area_keywords.get(area, [])):
                covered_areas.append(area)
            else:
                gaps["missing_perspectives"].append(area)
        
        # Generate recommendations
        if gaps["missing_perspectives"]:
            gaps["recommendations"].append("Consider addressing missing perspectives in content")
        
        if state.research_confidence < 0.6:
            gaps["recommendations"].append("Additional research may improve content quality")
        
        return gaps
    
    def _prioritize_trending_topics(self, state) -> List[str]:
        """Prioritize trending topics based on relevance and recency"""
        
        if not state.trending_topics:
            return []
        
        # Score topics based on multiple factors
        scored_topics = []
        
        for topic in state.trending_topics:
            score = 0
            topic_lower = topic.lower()
            
            # Relevance to main topic
            main_keywords = state.metadata.get("topic_keywords", [])
            relevance_score = sum(1 for keyword in main_keywords if keyword in topic_lower)
            score += relevance_score * 3
            
            # Industry relevance
            industry_context = state.metadata.get("industry_context", "general")
            if industry_context in topic_lower:
                score += 2
            
            # Innovation indicators
            innovation_words = ["new", "emerging", "breakthrough", "revolutionary", "next-gen"]
            if any(word in topic_lower for word in innovation_words):
                score += 1
            
            scored_topics.append((topic, score))
        
        # Sort by score and return top topics
        scored_topics.sort(key=lambda x: x[1], reverse=True)
        return [topic for topic, score in scored_topics[:5]]
    
    def _recommend_tone(self, state, quality_assessment: Dict[str, Any]) -> str:
        """Recommend writing tone based on research and content type"""
        
        content_type = state.content_type
        research_quality = quality_assessment["overall_score"]
        
        if content_type == "blog_post":
            if research_quality >= 0.8:
                return "authoritative and analytical"
            else:
                return "informative and accessible"
        elif content_type == "social_media":
            return "engaging and conversational"
        else:  # website_copy
            return "persuasive and confident"
    
    def _recommend_length(self, state, approach: str) -> Dict[str, int]:
        """Recommend content length based on approach and type"""
        
        base_config = state.metadata.get("content_config", {})
        base_min = base_config.get("min_words", 300)
        base_max = base_config.get("max_words", 1000)
        
        if approach == "comprehensive":
            return {"min_words": int(base_max * 0.8), "max_words": base_max}
        elif approach == "balanced":
            return {"min_words": int((base_min + base_max) / 2), "max_words": int(base_max * 0.9)}
        else:  # focused
            return {"min_words": base_min, "max_words": int((base_min + base_max) / 2)}

    # =============================================================================
    # CONTENT PLANNING AND STRATEGY AGENTS
    # =============================================================================
    
    def content_planning_enhanced(self, state) -> Dict[str, Any]:
        """
        ENHANCED: Content Planning
        AGENT: Content Strategist
        PURPOSE: Sophisticated content structure and strategy development
        """
        print("📋 ENHANCED CONTENT PLANNING")
        state.current_agent = "content_strategist"
        state.workflow_stage = "planning"
        start_time = datetime.now()
        
        try:
            # Get content strategy from research analysis
            content_strategy = state.metadata.get("content_strategy", {})
            
            # Create comprehensive content plan
            content_plan = self._create_comprehensive_content_plan(state, content_strategy)
            
            # Develop section-specific strategies
            section_strategies = self._develop_section_strategies(state, content_plan)
            
            # Create keyword integration plan
            keyword_plan = self._create_keyword_integration_plan(state, content_strategy)
            
            # Generate content outline
            detailed_outline = self._generate_detailed_outline(content_plan, section_strategies)
            
            # Update state with planning results
            state.content_outline = detailed_outline["text_outline"]
            state.content_sections = detailed_outline["section_details"]
            state.primary_keywords = keyword_plan["primary_keywords"]
            
            state.metadata.update({
                "content_plan": content_plan,
                "section_strategies": section_strategies,
                "keyword_plan": keyword_plan,
                "detailed_outline": detailed_outline,
                "planning_timestamp": datetime.now().isoformat()
            })
            
            print(f"📝 Content planning complete:")
            print(f"   📋 Sections: {len(state.content_sections)}")
            print(f"   🎯 Keywords: {len(state.primary_keywords)}")
            print(f"   📊 Strategy: {content_plan['approach']}")
            
        except Exception as e:
            state.error_messages.append(f"Content planning error: {str(e)}")
            print(f"❌ Planning failed: {e}")
        
        state.processing_time["planning"] = (datetime.now() - start_time).total_seconds()
        return state
    
    def _create_comprehensive_content_plan(self, state, content_strategy: Dict[str, Any]) -> Dict[str, Any]:
        """Create detailed content plan based on research and strategy"""
        
        content_type = state.content_type
        approach = content_strategy.get("approach", "balanced")
        research_insights = state.research_summary
        
        plan = {
            "approach": approach,
            "primary_objective": self._determine_primary_objective(state),
            "target_audience_profile": self._create_audience_profile(state),
            "content_structure": content_strategy.get("recommended_sections", []),
            "tone_and_style": {
                "tone": content_strategy.get("tone_recommendation", "professional"),
                "style": state.writing_style,
                "voice": "authoritative yet accessible"
            },
            "length_specifications": content_strategy.get("length_recommendation", {}),
            "engagement_strategy": self._develop_engagement_strategy(state),
            "differentiation_factors": self._identify_differentiation_factors(state)
        }
        
        return plan
    
    def _determine_primary_objective(self, state) -> str:
        """Determine the primary objective for the content"""
        
        content_type = state.content_type
        industry_context = state.metadata.get("industry_context", "general")
        
        objectives = {
            "blog_post": {
                "technology": "educate and inform about technological capabilities and applications",
                "business": "provide strategic insights and actionable business guidance",
                "finance": "explain financial concepts and market opportunities",
                "general": "inform and engage readers with valuable insights"
            },
            "social_media": {
                "technology": "create awareness and drive engagement around tech innovations",
                "business": "inspire and motivate business professionals",
                "finance": "build trust and showcase financial expertise",
                "general": "engage audience and encourage interaction"
            },
            "website_copy": {
                "technology": "convert visitors by demonstrating technical value propositions",
                "business": "persuade prospects to take action on business solutions",
                "finance": "build confidence and trust in financial services",
                "general": "convert visitors into customers or leads"
            }
        }
        
        return objectives.get(content_type, {}).get(industry_context, objectives[content_type]["general"])
    
    def _create_audience_profile(self, state) -> Dict[str, Any]:
        """Create detailed target audience profile"""
        
        target_audience = state.target_audience or "technology professionals"
        content_type = state.content_type
        industry_context = state.metadata.get("industry_context", "general")
        
        # Base audience characteristics
        audience_profiles = {
            "technology professionals": {
                "knowledge_level": "intermediate to advanced",
                "interests": ["innovation", "efficiency", "technical solutions"],
                "pain_points": ["complexity", "implementation challenges", "ROI concerns"],
                "preferred_content": "detailed analysis with practical applications"
            },
            "small business owners": {
                "knowledge_level": "beginner to intermediate",
                "interests": ["growth", "cost-effectiveness", "productivity"],
                "pain_points": ["limited resources", "time constraints", "complexity"],
                "preferred_content": "practical guides with clear benefits"
            },
            "startup founders": {
                "knowledge_level": "intermediate",
                "interests": ["scalability", "innovation", "competitive advantage"],
                "pain_points": ["resource constraints", "market competition", "rapid scaling"],
                "preferred_content": "strategic insights with actionable steps"
            }
        }
        
        # Get base profile or create generic one
        base_profile = audience_profiles.get(target_audience, {
            "knowledge_level": "intermediate",
            "interests": ["innovation", "efficiency"],
            "pain_points": ["complexity", "cost"],
            "preferred_content": "informative and practical"
        })
        
        # Enhance with context-specific details
        base_profile["industry_context"] = industry_context
        base_profile["content_type_preference"] = content_type
        
        return base_profile
    
    def _develop_engagement_strategy(self, state) -> Dict[str, Any]:
        """Develop strategy for audience engagement"""
        
        content_type = state.content_type
        audience_profile = self._create_audience_profile(state)
        
        strategies = {
            "blog_post": {
                "opening_hook": "start with compelling statistic or question",
                "structure_approach": "use clear headings and logical flow",
                "engagement_elements": ["examples", "case studies", "actionable insights"],
                "closing_strategy": "summarize key points and provide clear next steps"
            },
            "social_media": {
                "opening_hook": "bold statement or intriguing question",
                "structure_approach": "concise and scannable format",
                "engagement_elements": ["hashtags", "call-to-action", "visual appeal"],
                "closing_strategy": "clear call-to-action for engagement"
            },
            "website_copy": {
                "opening_hook": "value proposition in headline",
                "structure_approach": "benefits-focused with social proof",
                "engagement_elements": ["testimonials", "guarantees", "urgency"],
                "closing_strategy": "strong call-to-action with clear next steps"
            }
        }
        
        return strategies.get(content_type, strategies["blog_post"])
    
    def _identify_differentiation_factors(self, state) -> List[str]:
        """Identify factors that will differentiate this content"""
        
        factors = []
        
        # Based on research insights
        if state.research_confidence > 0.8:
            factors.append("comprehensive research-backed insights")
        
        if len(state.trending_topics) > 3:
            factors.append("coverage of latest industry trends")
        
        # Based on content approach
        content_strategy = state.metadata.get("content_strategy", {})
        if content_strategy.get("approach") == "comprehensive":
            factors.append("in-depth analysis and detailed coverage")
        
        # Based on industry context
        industry_context = state.metadata.get("industry_context", "general")
        if industry_context != "general":
            factors.append(f"specialized {industry_context} industry focus")
        
        # Add default factors if none identified
        if not factors:
            factors = ["practical insights", "actionable guidance", "clear explanations"]
        
        return factors
    
    def _develop_section_strategies(self, state, content_plan: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
        """Develop specific strategies for each content section"""
        
        sections = content_plan.get("content_structure", [])
        section_strategies = {}
        
        for section in sections:
            strategy = self._create_section_strategy(section, state, content_plan)
            section_strategies[section] = strategy
        
        return section_strategies
    
    def _create_section_strategy(self, section: str, state, content_plan: Dict[str, Any]) -> Dict[str, Any]:
        """Create strategy for individual content section"""
        
        content_type = state.content_type
        keywords = state.extracted_keywords[:10]
        
        # Section-specific strategies
        section_templates = {
            "introduction": {
                "purpose": "hook reader and establish credibility",
                "key_elements": ["attention-grabbing opening", "problem identification", "value proposition"],
                "keyword_integration": "primary keyword in first paragraph",
                "length_target": "10-15% of total content"
            },
            "main_content": {
                "purpose": "deliver core value and information",
                "key_elements": ["detailed analysis", "supporting evidence", "practical examples"],
                "keyword_integration": "natural distribution of primary and secondary keywords",
                "length_target": "50-60% of total content"
            },
            "benefits": {
                "purpose": "highlight value propositions and advantages",
                "key_elements": ["specific benefits", "quantified improvements", "competitive advantages"],
                "keyword_integration": "benefit-focused keywords",
                "length_target": "15-20% of total content"
            },
            "conclusion": {
                "purpose": "summarize and drive action",
                "key_elements": ["key takeaways", "call to action", "next steps"],
                "keyword_integration": "primary keyword reinforcement",
                "length_target": "10-15% of total content"
            }
        }
        
        # Get base template or create generic one
        base_template = section_templates.get(section, {
            "purpose": f"provide valuable information about {section}",
            "key_elements": ["relevant information", "supporting details"],
            "keyword_integration": "natural keyword usage",
            "length_target": "appropriate for section importance"
        })
        
        # Customize based on content type and research
        if content_type == "social_media":
            base_template["length_target"] = "concise and impactful"
        elif content_type == "website_copy":
            base_template["key_elements"].append("conversion-focused language")
        
        # Add section-specific keywords
        relevant_keywords = [kw for kw in keywords if section.lower() in kw.lower() or kw.lower() in section.lower()]
        base_template["relevant_keywords"] = relevant_keywords[:3]
        
        return base_template
    
    def _create_keyword_integration_plan(self, state, content_strategy: Dict[str, Any]) -> Dict[str, Any]:
        """Create comprehensive keyword integration plan"""
        
        primary_keywords = content_strategy.get("primary_keywords", state.extracted_keywords[:5])
        secondary_keywords = content_strategy.get("secondary_keywords", state.extracted_keywords[5:10])
        
        # Calculate keyword density targets
        content_length = state.metadata.get("content_config", {}).get("max_words", 1000)
        
        plan = {
            "primary_keywords": primary_keywords,
            "secondary_keywords": secondary_keywords,
            "density_targets": {
                "primary": "1-2% density per primary keyword",
                "secondary": "0.5-1% density per secondary keyword"
            },
            "placement_strategy": {
                "title": "include primary keyword",
                "introduction": "primary keyword in first 100 words",
                "headings": "distribute keywords across section headings",
                "conclusion": "reinforce primary keyword",
                "meta_description": "primary keyword naturally integrated"
            },
            "semantic_variations": self._generate_semantic_variations(primary_keywords),
            "long_tail_opportunities": self._identify_long_tail_keywords(state)
        }
        
        return plan
    
    def _generate_semantic_variations(self, keywords: List[str]) -> Dict[str, List[str]]:
        """Generate semantic variations for keywords"""
        
        variations = {}
        
        for keyword in keywords:
            keyword_variations = []
            
            # Add plural/singular variations
            if keyword.endswith('s'):
                keyword_variations.append(keyword[:-1])
            else:
                keyword_variations.append(keyword + 's')
            
            # Add related terms (simplified approach)
            related_terms = {
                "ai": ["artificial intelligence", "machine learning", "automation"],
                "business": ["company", "organization", "enterprise"],
                "technology": ["tech", "digital", "innovation"],
                "automation": ["automated", "automatic", "streamlined"]
            }
            
            if keyword.lower() in related_terms:
                keyword_variations.extend(related_terms[keyword.lower()])
            
            variations[keyword] = keyword_variations[:3]  # Limit to 3 variations
        
        return variations
    
    def _identify_long_tail_keywords(self, state) -> List[str]:
        """Identify long-tail keyword opportunities"""
        
        topic = state.topic
        industry_context = state.metadata.get("industry_context", "general")
        content_type = state.content_type
        
        # Generate long-tail combinations
        long_tail_templates = [
            f"how to implement {topic}",
            f"{topic} for {industry_context} industry",
            f"benefits of {topic}",
            f"{topic} best practices",
            f"{topic} vs alternatives"
        ]
        
        # Filter and clean long-tail keywords
        long_tail = []
        for template in long_tail_templates:
            if len(template.split()) >= 3:  # Ensure it's actually long-tail
                long_tail.append(template)
        
        return long_tail[:5]  # Return top 5 long-tail opportunities
    
    def _generate_detailed_outline(self, content_plan: Dict[str, Any], section_strategies: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
        """Generate detailed content outline with section specifications"""
        
        sections = content_plan.get("content_structure", [])
        
        outline_parts = []
        section_details = []
        
        for i, section in enumerate(sections, 1):
            strategy = section_strategies.get(section, {})
            
            # Create section outline entry
            outline_entry = f"{i}. {section.replace('_', ' ').title()}"
            
            if strategy.get("purpose"):
                outline_entry += f"\n   Purpose: {strategy['purpose']}"
            
            if strategy.get("key_elements"):
                outline_entry += f"\n   Elements: {', '.join(strategy['key_elements'])}"
            
            if strategy.get("relevant_keywords"):
                outline_entry += f"\n   Keywords: {', '.join(strategy['relevant_keywords'])}"
            
            outline_parts.append(outline_entry)
            
            # Create detailed section specification
            section_detail = {
                "section_name": section,
                "order": i,
                "strategy": strategy,
                "estimated_length": strategy.get("length_target", "proportional")
            }
            
            section_details.append(section_detail)
        
        return {
            "text_outline": "\n\n".join(outline_parts),
            "section_details": section_details,
            "total_sections": len(sections)
        }

if __name__ == "__main__":
    # Test the enhanced agents
    print("Enhanced Content Creation Agents - Ready for Integration")