"""
Enhanced Agent Implementations Part 3: SEO, Quality Assurance, and Workflow Management
Advanced node functions for SEO optimization, quality control, and workflow orchestration
"""

import os
import re
import json
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
import statistics
from collections import Counter
import hashlib

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

from SEO_tool import seo_tool
from config import Config

class AdvancedContentAgentsPart3:
    """
    Enhanced agent implementations for SEO, QA, and workflow management
    """
    
    def __init__(self):
        self.llm = ChatOpenAI(temperature=0.7, model="gpt-3.5-turbo")
        self.analytical_llm = ChatOpenAI(temperature=0.1, model="gpt-3.5-turbo")
        
        # SEO optimization parameters
        self.seo_best_practices = {
            "keyword_density": {"optimal_range": (1.0, 2.5), "max_safe": 3.0},
            "title_optimization": {"length_range": (30, 60), "keyword_position": "front"},
            "meta_description": {"length_range": (140, 160), "include_cta": True},
            "heading_structure": {"h1_count": 1, "h2_range": (2, 6), "h3_max": 8},
            "content_length": {"min_words": 300, "optimal_range": (800, 1500)},
            "internal_linking": {"suggestions_per_1000_words": 2},
            "readability": {"target_score": 70, "min_acceptable": 60}
        }
        
        # Quality assurance framework
        self.qa_framework = {
            "content_quality": {
                "structure": {"weight": 0.25, "criteria": ["intro", "body", "conclusion"]},
                "coherence": {"weight": 0.20, "criteria": ["flow", "transitions", "logic"]},
                "value": {"weight": 0.25, "criteria": ["actionable", "informative", "relevant"]},
                "engagement": {"weight": 0.15, "criteria": ["hook", "examples", "cta"]},
                "technical": {"weight": 0.15, "criteria": ["grammar", "spelling", "formatting"]}
            },
            "seo_quality": {
                "keyword_optimization": {"weight": 0.30},
                "technical_seo": {"weight": 0.25},
                "content_optimization": {"weight": 0.25},
                "user_experience": {"weight": 0.20}
            },
            "brand_alignment": {
                "tone_consistency": {"weight": 0.40},
                "message_alignment": {"weight": 0.35},
                "audience_targeting": {"weight": 0.25}
            }
        }
        
        # Revision strategies
        self.revision_strategies = {
            "structure_improvement": {
                "techniques": ["reorganize_sections", "improve_transitions", "strengthen_intro_conclusion"],
                "priority": "high"
            },
            "content_enhancement": {
                "techniques": ["add_examples", "expand_explanations", "include_data"],
                "priority": "medium"
            },
            "seo_optimization": {
                "techniques": ["keyword_integration", "meta_optimization", "heading_structure"],
                "priority": "medium"
            },
            "readability_improvement": {
                "techniques": ["simplify_language", "shorten_sentences", "improve_flow"],
                "priority": "high"
            }
        }

    # =============================================================================
    # SEO OPTIMIZATION AGENTS
    # =============================================================================
    
    def seo_optimization_enhanced(self, state) -> Dict[str, Any]:
        """
        ENHANCED: SEO Optimization
        AGENT: SEO Specialist
        PURPOSE: Comprehensive SEO optimization with advanced techniques and analysis
        """
        print("🔍 ENHANCED SEO OPTIMIZATION")
        state.current_agent = "seo_specialist"
        state.workflow_stage = "seo_optimization"
        start_time = datetime.now()
        
        try:
            # Get content and keyword data
            content = state.draft_content or ""
            keyword_plan = state.metadata.get("keyword_plan", {})
            
            if not content:
                state.error_messages.append("No content available for SEO optimization")
                return state
            
            # Comprehensive SEO analysis
            seo_analysis = self._comprehensive_seo_analysis(content, keyword_plan, state)
            
            # Generate SEO optimizations
            seo_optimizations = self._generate_seo_optimizations(content, seo_analysis, keyword_plan)
            
            # Apply optimizations to content
            optimized_result = self._apply_seo_optimizations(content, seo_optimizations)
            
            # Generate SEO metadata
            seo_metadata = self._generate_seo_metadata(optimized_result["content"], keyword_plan, state)
            
            # Calculate SEO score
            seo_score = self._calculate_comprehensive_seo_score(optimized_result["content"], seo_metadata, keyword_plan)
            
            # Update state with SEO results
            state.optimized_content = optimized_result["content"]
            state.seo_score = seo_score["overall_score"]
            state.meta_description = seo_metadata["meta_description"]
            state.title_suggestions = seo_metadata["title_suggestions"]
            
            # Store comprehensive SEO data
            state.metadata.update({
                "seo_analysis": seo_analysis,
                "seo_optimizations": seo_optimizations,
                "seo_metadata": seo_metadata,
                "seo_score_breakdown": seo_score,
                "seo_timestamp": datetime.now().isoformat()
            })
            
            print(f"🎯 SEO optimization complete:")
            print(f"   📊 SEO Score: {state.seo_score:.1f}/100")
            print(f"   🔍 Optimizations Applied: {len(seo_optimizations['applied'])}")
            print(f"   📝 Meta Description: {len(state.meta_description)} chars")
            
        except Exception as e:
            state.error_messages.append(f"SEO optimization error: {str(e)}")
            state.optimized_content = state.draft_content
            state.seo_score = 50.0
            print(f"❌ SEO optimization failed: {e}")
        
        state.processing_time["seo_optimization"] = (datetime.now() - start_time).total_seconds()
        return state
    
    def _comprehensive_seo_analysis(self, content: str, keyword_plan: Dict[str, Any], state) -> Dict[str, Any]:
        """Perform comprehensive SEO analysis of content"""
        
        analysis = {
            "keyword_analysis": self._analyze_keyword_performance(content, keyword_plan),
            "content_structure": self._analyze_content_structure_seo(content),
            "technical_seo": self._analyze_technical_seo_factors(content),
            "competitive_analysis": self._basic_competitive_analysis(state),
            "optimization_opportunities": []
        }
        
        # Identify optimization opportunities
        analysis["optimization_opportunities"] = self._identify_seo_opportunities(analysis)
        
        return analysis
    
    def _analyze_keyword_performance(self, content: str, keyword_plan: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze keyword usage and performance"""
        
        content_lower = content.lower()
        word_count = len(content.split())
        
        primary_keywords = keyword_plan.get("primary_keywords", [])
        secondary_keywords = keyword_plan.get("secondary_keywords", [])
        
        keyword_performance = {
            "primary_keywords": {},
            "secondary_keywords": {},
            "density_analysis": {},
            "placement_analysis": {},
            "semantic_coverage": {}
        }
        
        # Analyze primary keywords
        for keyword in primary_keywords:
            keyword_lower = keyword.lower()
            count = content_lower.count(keyword_lower)
            density = (count / word_count) * 100 if word_count > 0 else 0
            
            # Placement analysis
            first_paragraph = content.split('\n\n')[0] if '\n\n' in content else content[:200]
            last_paragraph = content.split('\n\n')[-1] if '\n\n' in content else content[-200:]
            
            placement = {
                "in_title_area": keyword_lower in content[:100].lower(),
                "in_first_paragraph": keyword_lower in first_paragraph.lower(),
                "in_last_paragraph": keyword_lower in last_paragraph.lower(),
                "in_headings": self._check_keyword_in_headings(content, keyword_lower),
                "distribution_score": self._calculate_keyword_distribution(content, keyword_lower)
            }
            
            keyword_performance["primary_keywords"][keyword] = {
                "count": count,
                "density": density,
                "placement": placement,
                "optimization_status": self._assess_keyword_optimization(count, density, placement)
            }
        
        # Analyze secondary keywords
        for keyword in secondary_keywords:
            keyword_lower = keyword.lower()
            count = content_lower.count(keyword_lower)
            density = (count / word_count) * 100 if word_count > 0 else 0
            
            keyword_performance["secondary_keywords"][keyword] = {
                "count": count,
                "density": density,
                "optimization_status": "optimal" if 0.5 <= density <= 1.5 else "needs_improvement"
            }
        
        # Semantic variations analysis
        semantic_variations = keyword_plan.get("semantic_variations", {})
        for main_keyword, variations in semantic_variations.items():
            coverage_score = 0
            for variation in variations:
                if variation.lower() in content_lower:
                    coverage_score += 1
            
            keyword_performance["semantic_coverage"][main_keyword] = {
                "variations_found": coverage_score,
                "total_variations": len(variations),
                "coverage_percentage": (coverage_score / len(variations)) * 100 if variations else 0
            }
        
        return keyword_performance
    
    def _check_keyword_in_headings(self, content: str, keyword: str) -> bool:
        """Check if keyword appears in headings"""
        
        # Simple heading detection (in production, use more sophisticated parsing)
        heading_patterns = [r'#\s+.*', r'\*\*.*\*\*', r'##\s+.*']
        
        for pattern in heading_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            for match in matches:
                if keyword in match.lower():
                    return True
        
        return False
    
    def _calculate_keyword_distribution(self, content: str, keyword: str) -> float:
        """Calculate how well keyword is distributed throughout content"""
        
        # Split content into quarters
        words = content.split()
        quarter_size = len(words) // 4
        
        quarters = [
            ' '.join(words[:quarter_size]),
            ' '.join(words[quarter_size:quarter_size*2]),
            ' '.join(words[quarter_size*2:quarter_size*3]),
            ' '.join(words[quarter_size*3:])
        ]
        
        # Count keyword occurrences in each quarter
        quarter_counts = [quarter.lower().count(keyword) for quarter in quarters]
        
        # Calculate distribution score (higher is more evenly distributed)
        if sum(quarter_counts) == 0:
            return 0
        
        # Penalty for uneven distribution
        max_count = max(quarter_counts)
        min_count = min(quarter_counts)
        
        if max_count == 0:
            return 0
        
        distribution_score = (1 - (max_count - min_count) / max_count) * 100
        return distribution_score
    
    def _assess_keyword_optimization(self, count: int, density: float, placement: Dict[str, Any]) -> str:
        """Assess keyword optimization status"""
        
        optimal_density = self.seo_best_practices["keyword_density"]["optimal_range"]
        
        # Check density
        if density < optimal_density[0]:
            return "under_optimized"
        elif density > optimal_density[1]:
            return "over_optimized"
        
        # Check placement
        placement_score = sum([
            placement.get("in_first_paragraph", False),
            placement.get("in_last_paragraph", False),
            placement.get("in_headings", False),
            placement.get("distribution_score", 0) > 50
        ])
        
        if placement_score >= 3:
            return "well_optimized"
        elif placement_score >= 2:
            return "moderately_optimized"
        else:
            return "poorly_positioned"
    
    def _analyze_content_structure_seo(self, content: str) -> Dict[str, Any]:
        """Analyze content structure from SEO perspective"""
        
        structure_analysis = {
            "heading_structure": self._analyze_heading_structure(content),
            "paragraph_structure": self._analyze_paragraph_structure(content),
            "content_length": self._analyze_content_length(content),
            "readability": self._assess_seo_readability(content)
        }
        
        return structure_analysis
    
    def _analyze_heading_structure(self, content: str) -> Dict[str, Any]:
        """Analyze heading structure for SEO"""
        
        # Simple heading detection
        h1_count = content.count('# ') + content.count('\n# ')
        h2_count = content.count('## ') + content.count('\n## ')
        h3_count = content.count('### ') + content.count('\n### ')
        
        # Also check for bold headings
        bold_headings = len(re.findall(r'\*\*[^*]+\*\*', content))
        
        best_practices = self.seo_best_practices["heading_structure"]
        
        analysis = {
            "h1_count": h1_count,
            "h2_count": h2_count,
            "h3_count": h3_count,
            "bold_headings": bold_headings,
            "total_headings": h1_count + h2_count + h3_count + bold_headings,
            "structure_score": 100
        }
        
        # Assess structure quality
        if h1_count != best_practices["h1_count"]:
            analysis["structure_score"] -= 20
        
        if h2_count < 2 or h2_count > 6:
            analysis["structure_score"] -= 15
        
        if h3_count > best_practices["h3_max"]:
            analysis["structure_score"] -= 10
        
        analysis["structure_score"] = max(0, analysis["structure_score"])
        
        return analysis
    
    def _analyze_paragraph_structure(self, content: str) -> Dict[str, Any]:
        """Analyze paragraph structure for SEO readability"""
        
        paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]
        
        if not paragraphs:
            return {"paragraph_count": 0, "avg_length": 0, "structure_score": 0}
        
        paragraph_lengths = [len(p.split()) for p in paragraphs]
        avg_length = statistics.mean(paragraph_lengths)
        
        # Assess paragraph quality
        structure_score = 100
        
        if avg_length > 150:  # Too long
            structure_score -= 20
        elif avg_length < 30:  # Too short
            structure_score -= 15
        
        # Check for very long paragraphs
        long_paragraphs = sum(1 for length in paragraph_lengths if length > 200)
        if long_paragraphs > 0:
            structure_score -= long_paragraphs * 10
        
        return {
            "paragraph_count": len(paragraphs),
            "avg_length": avg_length,
            "max_length": max(paragraph_lengths),
            "min_length": min(paragraph_lengths),
            "long_paragraphs": long_paragraphs,
            "structure_score": max(0, structure_score)
        }
    
    def _analyze_content_length(self, content: str) -> Dict[str, Any]:
        """Analyze content length for SEO optimization"""
        
        word_count = len(content.split())
        best_practices = self.seo_best_practices["content_length"]
        
        length_analysis = {
            "word_count": word_count,
            "character_count": len(content),
            "meets_minimum": word_count >= best_practices["min_words"],
            "in_optimal_range": best_practices["optimal_range"][0] <= word_count <= best_practices["optimal_range"][1],
            "length_score": 100
        }
        
        # Calculate length score
        if word_count < best_practices["min_words"]:
            deficit = best_practices["min_words"] - word_count
            length_analysis["length_score"] -= min(50, (deficit / best_practices["min_words"]) * 100)
        elif word_count > best_practices["optimal_range"][1] * 1.5:  # Significantly too long
            excess = word_count - best_practices["optimal_range"][1]
            length_analysis["length_score"] -= min(30, (excess / best_practices["optimal_range"][1]) * 50)
        
        length_analysis["length_score"] = max(0, length_analysis["length_score"])
        
        return length_analysis
    
    def _assess_seo_readability(self, content: str) -> Dict[str, Any]:
        """Assess readability from SEO perspective"""
        
        words = content.split()
        sentences = [s.strip() for s in content.split('.') if s.strip()]
        
        if not sentences:
            return {"readability_score": 0, "seo_readability": "poor"}
        
        # Calculate basic readability metrics
        avg_words_per_sentence = len(words) / len(sentences)
        avg_chars_per_word = sum(len(word) for word in words) / len(words) if words else 0
        
        # Simplified Flesch Reading Ease calculation
        readability_score = 206.835 - (1.015 * avg_words_per_sentence) - (84.6 * (avg_chars_per_word / 4.7))
        readability_score = max(0, min(100, readability_score))
        
        # SEO readability assessment
        target_score = self.seo_best_practices["readability"]["target_score"]
        min_acceptable = self.seo_best_practices["readability"]["min_acceptable"]
        
        if readability_score >= target_score:
            seo_readability = "excellent"
        elif readability_score >= min_acceptable:
            seo_readability = "good"
        elif readability_score >= 40:
            seo_readability = "acceptable"
        else:
            seo_readability = "poor"
        
        return {
            "readability_score": readability_score,
            "seo_readability": seo_readability,
            "avg_words_per_sentence": avg_words_per_sentence,
            "avg_chars_per_word": avg_chars_per_word,
            "meets_seo_standards": readability_score >= min_acceptable
        }
    
    def _analyze_technical_seo_factors(self, content: str) -> Dict[str, Any]:
        """Analyze technical SEO factors"""
        
        technical_analysis = {
            "content_uniqueness": self._assess_content_uniqueness(content),
            "internal_linking": self._analyze_internal_linking_opportunities(content),
            "media_optimization": self._assess_media_elements(content),
            "schema_opportunities": self._identify_schema_opportunities(content)
        }
        
        return technical_analysis
    
    def _assess_content_uniqueness(self, content: str) -> Dict[str, Any]:
        """Assess content uniqueness (simplified approach)"""
        
        # Create content fingerprint
        content_hash = hashlib.md5(content.encode()).hexdigest()
        
        # Basic uniqueness indicators
        unique_phrases = []
        sentences = [s.strip() for s in content.split('.') if s.strip() and len(s.split()) > 5]
        
        for sentence in sentences[:10]:  # Check first 10 sentences
            if '"' in sentence or "according to" in sentence.lower() or "research shows" in sentence.lower():
                unique_phrases.append(sentence[:50] + "...")
        
        return {
            "content_hash": content_hash,
            "unique_phrases_detected": len(unique_phrases),
            "quoted_content": unique_phrases,
            "estimated_originality": max(0, 100 - len(unique_phrases) * 10)  # Simplified scoring
        }
    
    def _analyze_internal_linking_opportunities(self, content: str) -> Dict[str, Any]:
        """Analyze opportunities for internal linking"""
        
        word_count = len(content.split())
        recommended_links = max(1, word_count // 500)  # 1 link per 500 words
        
        # Identify potential link anchor texts (simplified)
        potential_anchors = []
        content_lower = content.lower()
        
        common_link_phrases = [
            "learn more about", "read our guide", "see our article", "check out",
            "find out more", "discover how", "explore our"
        ]
        
        for phrase in common_link_phrases:
            if phrase in content_lower:
                potential_anchors.append(phrase)
        
        return {
            "recommended_link_count": recommended_links,
            "potential_anchors": potential_anchors,
            "linking_opportunities": max(0, recommended_links - len(potential_anchors))
        }
    
    def _assess_media_elements(self, content: str) -> Dict[str, Any]:
        """Assess media elements and optimization opportunities"""
        
        # Simple detection of media references
        image_references = content.lower().count('image') + content.lower().count('photo') + content.lower().count('screenshot')
        video_references = content.lower().count('video') + content.lower().count('demonstration')
        chart_references = content.lower().count('chart') + content.lower().count('graph') + content.lower().count('data')
        
        return {
            "image_opportunities": image_references,
            "video_opportunities": video_references,
            "chart_opportunities": chart_references,
            "total_media_opportunities": image_references + video_references + chart_references
        }
    
    def _identify_schema_opportunities(self, content: str) -> List[str]:
        """Identify structured data opportunities"""
        
        opportunities = []
        content_lower = content.lower()
        
        # Common schema types for content marketing
        if any(word in content_lower for word in ["how to", "step", "guide", "tutorial"]):
            opportunities.append("HowTo")
        
        if any(word in content_lower for word in ["faq", "question", "answer"]):
            opportunities.append("FAQPage")
        
        if any(word in content_lower for word in ["review", "rating", "star"]):
            opportunities.append("Review")
        
        if any(word in content_lower for word in ["product", "service", "tool"]):
            opportunities.append("Product")
        
        return opportunities
    
    def _basic_competitive_analysis(self, state) -> Dict[str, Any]:
        """Basic competitive analysis based on topic"""
        
        topic = state.topic
        industry_context = state.metadata.get("industry_context", "general")
        
        # Simplified competitive indicators
        competitive_factors = {
            "topic_competitiveness": "high" if any(word in topic.lower() for word in ["ai", "automation", "digital"]) else "medium",
            "industry_saturation": "high" if industry_context == "technology" else "medium",
            "content_differentiation_needed": True,
            "recommended_content_depth": "comprehensive" if industry_context == "technology" else "moderate"
        }
        
        return competitive_factors
    
    def _identify_seo_opportunities(self, analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identify specific SEO improvement opportunities"""
        
        opportunities = []
        
        # Keyword opportunities
        keyword_analysis = analysis.get("keyword_analysis", {})
        for keyword, data in keyword_analysis.get("primary_keywords", {}).items():
            if data["optimization_status"] in ["under_optimized", "poorly_positioned"]:
                opportunities.append({
                    "type": "keyword_optimization",
                    "priority": "high",
                    "description": f"Improve optimization for keyword '{keyword}'",
                    "specific_action": f"Increase usage and improve placement of '{keyword}'"
                })
        
        # Structure opportunities
        structure_analysis = analysis.get("content_structure", {})
        heading_structure = structure_analysis.get("heading_structure", {})
        
        if heading_structure.get("structure_score", 0) < 80:
            opportunities.append({
                "type": "structure_improvement",
                "priority": "medium",
                "description": "Improve heading structure for better SEO",
                "specific_action": "Add appropriate H1, H2, and H3 headings"
            })
        
        # Readability opportunities
        readability = structure_analysis.get("readability", {})
        if readability.get("seo_readability") in ["poor", "acceptable"]:
            opportunities.append({
                "type": "readability_improvement",
                "priority": "medium",
                "description": "Improve content readability for better user experience",
                "specific_action": "Simplify language and shorten sentences"
            })
        
        return opportunities
    
    def _generate_seo_optimizations(self, content: str, seo_analysis: Dict[str, Any], keyword_plan: Dict[str, Any]) -> Dict[str, Any]:
        """Generate specific SEO optimizations to apply"""
        
        optimizations = {
            "keyword_optimizations": [],
            "structure_optimizations": [],
            "content_optimizations": [],
            "technical_optimizations": [],
            "applied": [],
            "priority_order": []
        }
        
        # Generate keyword optimizations
        keyword_analysis = seo_analysis.get("keyword_analysis", {})
        primary_keywords = keyword_plan.get("primary_keywords", [])
        
        for keyword in primary_keywords[:3]:  # Focus on top 3 keywords
            keyword_data = keyword_analysis.get("primary_keywords", {}).get(keyword, {})
            optimization_status = keyword_data.get("optimization_status", "")
            
            if optimization_status == "under_optimized":
                optimizations["keyword_optimizations"].append({
                    "keyword": keyword,
                    "action": "increase_usage",
                    "target_density": "1.5-2.0%",
                    "placement_focus": ["introduction", "conclusion", "headings"]
                })
            elif optimization_status == "poorly_positioned":
                optimizations["keyword_optimizations"].append({
                    "keyword": keyword,
                    "action": "improve_placement",
                    "focus_areas": ["first_paragraph", "headings", "conclusion"]
                })
        
        # Generate structure optimizations
        structure_analysis = seo_analysis.get("content_structure", {})
        heading_structure = structure_analysis.get("heading_structure", {})
        
        if heading_structure.get("h1_count", 0) == 0:
            optimizations["structure_optimizations"].append({
                "action": "add_h1_heading",
                "description": "Add main H1 heading with primary keyword"
            })
        
        if heading_structure.get("h2_count", 0) < 2:
            optimizations["structure_optimizations"].append({
                "action": "add_h2_headings",
                "description": "Add section headings (H2) for better structure"
            })
        
        # Generate content optimizations
        content_length = structure_analysis.get("content_length", {})
        if not content_length.get("meets_minimum", True):
            optimizations["content_optimizations"].append({
                "action": "expand_content",
                "target_words": self.seo_best_practices["content_length"]["min_words"],
                "focus": "add_value_not_fluff"
            })
        
        readability = structure_analysis.get("readability", {})
        if readability.get("seo_readability") == "poor":
            optimizations["content_optimizations"].append({
                "action": "improve_readability",
                "focus": ["shorter_sentences", "simpler_words", "better_flow"]
            })
        
        # Prioritize optimizations
        priority_mapping = {
            "keyword_optimizations": 1,
            "structure_optimizations": 2,
            "content_optimizations": 3,
            "technical_optimizations": 4
        }
        
        all_optimizations = []
        for category, items in optimizations.items():
            if category != "applied" and category != "priority_order" and items:
                for item in items:
                    all_optimizations.append({
                        "category": category,
                        "priority": priority_mapping.get(category, 5),
                        "optimization": item
                    })
        
        # Sort by priority
        all_optimizations.sort(key=lambda x: x["priority"])
        optimizations["priority_order"] = all_optimizations
        
        return optimizations
    
    def _apply_seo_optimizations(self, content: str, optimizations: Dict[str, Any]) -> Dict[str, Any]:
        """Apply SEO optimizations to content"""
        
        optimized_content = content
        applied_optimizations = []
        
        # Apply keyword optimizations
        for opt in optimizations.get("keyword_optimizations", []):
            if opt["action"] == "increase_usage":
                keyword = opt["keyword"]
                
                # Simple keyword insertion (in production, use more sophisticated NLP)
                if "introduction" in opt.get("placement_focus", []):
                    optimized_content = self._enhance_keyword_in_introduction(optimized_content, keyword)
                    applied_optimizations.append(f"Enhanced '{keyword}' in introduction")
                
                if "conclusion" in opt.get("placement_focus", []):
                    optimized_content = self._enhance_keyword_in_conclusion(optimized_content, keyword)
                    applied_optimizations.append(f"Enhanced '{keyword}' in conclusion")
        
        # Apply structure optimizations
        for opt in optimizations.get("structure_optimizations", []):
            if opt["action"] == "add_h1_heading":
                optimized_content = self._add_main_heading(optimized_content)
                applied_optimizations.append("Added main H1 heading")
            
            elif opt["action"] == "add_h2_headings":
                optimized_content = self._add_section_headings(optimized_content)
                applied_optimizations.append("Added section headings")
        
        # Apply basic SEO tool optimization
        try:
            primary_keywords = optimizations.get("keyword_optimizations", [])
            if primary_keywords:
                keywords_str = ", ".join([opt["keyword"] for opt in primary_keywords])
                tool_optimized = seo_tool.run(optimized_content, keywords_str)
                
                if tool_optimized and tool_optimized != optimized_content:
                    optimized_content = tool_optimized
                    applied_optimizations.append("Applied SEO tool optimizations")
        except Exception as e:
            print(f"⚠️ SEO tool optimization failed: {e}")
        
        return {
            "content": optimized_content,
            "applied_optimizations": applied_optimizations,
            "optimization_count": len(applied_optimizations)
        }
    
    def _enhance_keyword_in_introduction(self, content: str, keyword: str) -> str:
        """Enhance keyword usage in introduction"""
        
        paragraphs = content.split('\n\n')
        if not paragraphs:
            return content
        
        first_paragraph = paragraphs[0]
        
        # Check if keyword is already well-integrated
        if keyword.lower() in first_paragraph.lower():
            return content
        
        # Simple keyword integration (in production, use more sophisticated methods)
        if first_paragraph:
            # Try to naturally integrate the keyword
            enhanced_intro = f"Understanding {keyword} is essential for modern businesses. {first_paragraph}"
            paragraphs[0] = enhanced_intro
        
        return '\n\n'.join(paragraphs)
    
    def _enhance_keyword_in_conclusion(self, content: str, keyword: str) -> str:
        """Enhance keyword usage in conclusion"""
        
        paragraphs = content.split('\n\n')
        if len(paragraphs) < 2:
            return content
        
        last_paragraph = paragraphs[-1]
        
        # Check if keyword is already present
        if keyword.lower() in last_paragraph.lower():
            return content
        
        # Add keyword to conclusion naturally
        if "conclusion" in last_paragraph.lower() or "summary" in last_paragraph.lower():
            enhanced_conclusion = last_paragraph.replace(
                "In conclusion", f"In conclusion, {keyword} represents"
            ).replace(
                "To summarize", f"To summarize, {keyword} offers"
            )
            paragraphs[-1] = enhanced_conclusion
        
        return '\n\n'.join(paragraphs)
    
    def _add_main_heading(self, content: str) -> str:
        """Add main H1 heading if missing"""
        
        # Check if content already has H1
        if content.startswith('# ') or '\n# ' in content:
            return content
        
        # Add H1 at the beginning
        lines = content.split('\n')
        if lines:
            # Create heading from first sentence or paragraph
            first_line = lines[0].strip()
            if len(first_line) > 10:
                heading = f"# {first_line.split('.')[0]}\n\n"
                return heading + content
        
        return content
    
    def _add_section_headings(self, content: str) -> str:
        """Add section headings for better structure"""
        
        paragraphs = content.split('\n\n')
        if len(paragraphs) < 3:
            return content
        
        # Add headings every 2-3 paragraphs for long content
        if len(paragraphs) >= 6:
            enhanced_paragraphs = []
            for i, paragraph in enumerate(paragraphs):
                if i == 2:  # Add heading before 3rd paragraph
                    enhanced_paragraphs.append("## Key Benefits and Applications")
                elif i == len(paragraphs) - 2:  # Add heading before second-to-last
                    enhanced_paragraphs.append("## Implementation and Next Steps")
                
                enhanced_paragraphs.append(paragraph)
            
            return '\n\n'.join(enhanced_paragraphs)
        
        return content
    
    def _generate_seo_metadata(self, content: str, keyword_plan: Dict[str, Any], state) -> Dict[str, Any]:
        """Generate comprehensive SEO metadata"""
        
        primary_keywords = keyword_plan.get("primary_keywords", [])
        topic = state.topic
        
        metadata = {
            "meta_description": self._generate_meta_description(content, primary_keywords, topic),
            "title_suggestions": self._generate_title_suggestions(topic, primary_keywords),
            "heading_recommendations": self._generate_heading_recommendations(content, primary_keywords),
            "schema_suggestions": self._generate_schema_suggestions(content, state),
            "social_meta": self._generate_social_meta(topic, primary_keywords)
        }
        
        return metadata
    
    def _generate_meta_description(self, content: str, keywords: List[str], topic: str) -> str:
        """Generate optimized meta description"""
        
        # Extract key points from content
        first_sentences = '. '.join(content.split('. ')[:2])
        
        # Include primary keyword if available
        primary_keyword = keywords[0] if keywords else topic
        
        # Create meta description
        if len(first_sentences) > 160:
            # Truncate and add primary keyword
            base_description = first_sentences[:140]
            meta_description = f"{base_description}... Learn about {primary_keyword}."
        else:
            # Use first sentences and enhance with keyword
            meta_description = f"{first_sentences} Discover how {primary_keyword} can benefit your business."
        
        # Ensure optimal length
        if len(meta_description) > 160:
            meta_description = meta_description[:157] + "..."
        elif len(meta_description) < 140:
            meta_description += f" Expert insights on {primary_keyword}."
        
        return meta_description[:160]  # Hard limit
    
    def _generate_title_suggestions(self, topic: str, keywords: List[str]) -> List[str]:
        """Generate SEO-optimized title suggestions"""
        
        primary_keyword = keywords[0] if keywords else topic
        
        title_templates = [
            f"{primary_keyword}: Complete Guide for 2024",
            f"How {primary_keyword} Transforms Business Operations",
            f"The Ultimate {primary_keyword} Implementation Guide",
            f"{primary_keyword} Benefits: What You Need to Know",
            f"Mastering {primary_keyword}: Expert Strategies and Tips"
        ]
        
        # Ensure titles are within optimal length
        optimized_titles = []
        for title in title_templates:
            if 30 <= len(title) <= 60:
                optimized_titles.append(title)
            elif len(title) > 60:
                # Truncate long titles
                truncated = title[:57] + "..."
                optimized_titles.append(truncated)
        
        return optimized_titles[:4]  # Return top 4 suggestions
    
    def _generate_heading_recommendations(self, content: str, keywords: List[str]) -> List[str]:
        """Generate heading recommendations for better structure"""
        
        recommendations = []
        
        # Analyze current heading structure
        h1_count = content.count('# ')
        h2_count = content.count('## ')
        
        if h1_count == 0:
            recommendations.append(f"Add H1: '{keywords[0] if keywords else 'Main Topic'} - Complete Overview'")
        
        if h2_count < 2:
            recommendations.extend([
                f"Add H2: 'Understanding {keywords[0] if keywords else 'the Topic'}'",
                f"Add H2: 'Key Benefits and Applications'",
                f"Add H2: 'Implementation Best Practices'",
                f"Add H2: 'Conclusion and Next Steps'"
            ])
        
        return recommendations
    
    def _generate_schema_suggestions(self, content: str, state) -> List[Dict[str, Any]]:
        """Generate structured data suggestions"""
        
        suggestions = []
        content_lower = content.lower()
        content_type = state.content_type
        
        # Article schema for blog posts
        if content_type == "blog_post":
            suggestions.append({
                "type": "Article",
                "properties": {
                    "headline": state.topic,
                    "description": "Comprehensive guide about " + state.topic,
                    "author": "Content Team",
                    "datePublished": datetime.now().isoformat()
                }
            })
        
        # FAQ schema if Q&A content detected
        if any(indicator in content_lower for indicator in ["what is", "how to", "why", "when"]):
            suggestions.append({
                "type": "FAQPage",
                "description": "Add FAQ schema for question-based content"
            })
        
        # HowTo schema for instructional content
        if any(indicator in content_lower for indicator in ["step", "guide", "tutorial", "how to"]):
            suggestions.append({
                "type": "HowTo",
                "description": "Add HowTo schema for instructional content"
            })
        
        return suggestions
    
    def _generate_social_meta(self, topic: str, keywords: List[str]) -> Dict[str, str]:
        """Generate social media meta tags"""
        
        primary_keyword = keywords[0] if keywords else topic
        
        return {
            "og_title": f"{primary_keyword}: Expert Guide and Insights",
            "og_description": f"Discover everything you need to know about {primary_keyword}. Expert insights, practical tips, and implementation strategies.",
            "twitter_title": f"{primary_keyword} Guide",
            "twitter_description": f"Expert insights on {primary_keyword} for business success."
        }
    
    def _calculate_comprehensive_seo_score(self, content: str, metadata: Dict[str, Any], keyword_plan: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate comprehensive SEO score with detailed breakdown"""
        
        score_components = {
            "keyword_optimization": self._score_keyword_optimization(content, keyword_plan),
            "content_structure": self._score_content_structure(content),
            "technical_seo": self._score_technical_seo(content, metadata),
            "user_experience": self._score_user_experience(content),
            "metadata_quality": self._score_metadata_quality(metadata)
        }
        
        # Weight factors
        weights = {
            "keyword_optimization": 0.30,
            "content_structure": 0.25,
            "technical_seo": 0.20,
            "user_experience": 0.15,
            "metadata_quality": 0.10
        }
        
        # Calculate weighted overall score
        overall_score = sum(score_components[component] * weights[component] for component in weights)
        
        return {
            "overall_score": overall_score,
            "component_scores": score_components,
            "weights": weights,
            "grade": self._assign_seo_grade(overall_score)
        }
    
    def _score_keyword_optimization(self, content: str, keyword_plan: Dict[str, Any]) -> float:
        """Score keyword optimization effectiveness"""
        
        score = 100
        content_lower = content.lower()
        word_count = len(content.split())
        
        primary_keywords = keyword_plan.get("primary_keywords", [])
        
        for keyword in primary_keywords[:3]:  # Focus on top 3
            keyword_count = content_lower.count(keyword.lower())
            density = (keyword_count / word_count) * 100 if word_count > 0 else 0
            
            # Optimal density scoring
            optimal_range = self.seo_best_practices["keyword_density"]["optimal_range"]
            if density < optimal_range[0]:
                score -= 15  # Under-optimized
            elif density > optimal_range[1] * 1.5:
                score -= 20  # Over-optimized
            
            # Placement scoring
            first_100 = ' '.join(content.split()[:100]).lower()
            if keyword.lower() not in first_100:
                score -= 10  # Not in introduction
        
        return max(0, score)
    
    def _score_content_structure(self, content: str) -> float:
        """Score content structure for SEO"""
        
        score = 100
        
        # Heading structure
        h1_count = content.count('# ')
        h2_count = content.count('## ')
        
        if h1_count != 1:
            score -= 20
        if h2_count < 2:
            score -= 15
        
        # Paragraph structure
        paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]
        if len(paragraphs) < 3:
            score -= 15
        
        # Content length
        word_count = len(content.split())
        min_words = self.seo_best_practices["content_length"]["min_words"]
        if word_count < min_words:
            score -= 25
        
        return max(0, score)
    
    def _score_technical_seo(self, content: str, metadata: Dict[str, Any]) -> float:
        """Score technical SEO factors"""
        
        score = 100
        
        # Meta description quality
        meta_desc = metadata.get("meta_description", "")
        if not meta_desc:
            score -= 30
        elif len(meta_desc) < 140 or len(meta_desc) > 160:
            score -= 15
        
        # Title suggestions quality
        titles = metadata.get("title_suggestions", [])
        if not titles:
            score -= 20
        
        return max(0, score)
    
    def _score_user_experience(self, content: str) -> float:
        """Score user experience factors"""
        
        words = content.split()
        sentences = [s.strip() for s in content.split('.') if s.strip()]
        
        if not sentences:
            return 0
        
        score = 100
        
        # Readability
        avg_words_per_sentence = len(words) / len(sentences)
        if avg_words_per_sentence > 25:
            score -= 20
        elif avg_words_per_sentence < 8:
            score -= 10
        
        # Paragraph length
        paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]
        if paragraphs:
            avg_paragraph_length = sum(len(p.split()) for p in paragraphs) / len(paragraphs)
            if avg_paragraph_length > 150:
                score -= 15
        
        return max(0, score)
    
    def _score_metadata_quality(self, metadata: Dict[str, Any]) -> float:
        """Score metadata quality"""
        
        score = 100
        
        # Meta description
        meta_desc = metadata.get("meta_description", "")
        if not meta_desc:
            score -= 40
        elif len(meta_desc) < 140:
            score -= 20
        
        # Title suggestions
        titles = metadata.get("title_suggestions", [])
        if len(titles) < 3:
            score -= 20
        
        # Schema suggestions
        schema = metadata.get("schema_suggestions", [])
        if not schema:
            score -= 20
        
        return max(0, score)
    
    def _assign_seo_grade(self, score: float) -> str:
        """Assign letter grade to SEO score"""
        
        if score >= 90:
            return "A+"
        elif score >= 85:
            return "A"
        elif score >= 80:
            return "B+"
        elif score >= 75:
            return "B"
        elif score >= 70:
            return "C+"
        elif score >= 65:
            return "C"
        elif score >= 60:
            return "D"
        else:
            return "F"

if __name__ == "__main__":
    # Test the enhanced agents part 3
    print("Enhanced Content Creation Agents Part 3 - Ready for Integration")