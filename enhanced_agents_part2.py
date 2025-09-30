"""
Enhanced Agent Implementations Part 2: Content Writing, SEO, and Quality Assurance
Advanced node functions for content generation, optimization, and quality control
"""

import os
import re
import json
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
import statistics
from collections import Counter

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate

from writing_tool import writing_tool
from SEO_tool import seo_tool
from config import Config

class AdvancedContentAgentsPart2:
    """
    Enhanced agent implementations for content writing, SEO, and quality assurance
    """
    
    def __init__(self):
        self.llm = ChatOpenAI(temperature=0.7, model="gpt-3.5-turbo")
        self.creative_llm = ChatOpenAI(temperature=0.8, model="gpt-3.5-turbo")  # Higher temp for creativity
        self.analytical_llm = ChatOpenAI(temperature=0.1, model="gpt-3.5-turbo")  # Lower temp for analysis
        
        # Advanced writing templates and guidelines
        self.writing_guidelines = {
            "blog_post": {
                "structure": ["compelling_intro", "informative_body", "actionable_conclusion"],
                "engagement_techniques": ["storytelling", "examples", "statistics", "questions"],
                "readability_targets": {"sentences_per_paragraph": 4, "words_per_sentence": 20}
            },
            "social_media": {
                "structure": ["hook", "value", "action"],
                "engagement_techniques": ["urgency", "curiosity", "emotion", "hashtags"],
                "readability_targets": {"sentences_per_paragraph": 2, "words_per_sentence": 15}
            },
            "website_copy": {
                "structure": ["headline", "benefits", "proof", "action"],
                "engagement_techniques": ["benefits_focus", "social_proof", "urgency", "clarity"],
                "readability_targets": {"sentences_per_paragraph": 3, "words_per_sentence": 18}
            }
        }
        
        # SEO optimization parameters
        self.seo_parameters = {
            "keyword_density": {"optimal": 1.5, "max": 3.0, "min": 0.5},
            "title_length": {"optimal": 60, "max": 70, "min": 30},
            "meta_description": {"optimal": 155, "max": 160, "min": 120},
            "heading_distribution": {"h1": 1, "h2": "3-5", "h3": "0-8"}
        }
        
        # Quality assessment criteria
        self.quality_criteria = {
            "content_structure": {
                "clear_introduction": 10,
                "logical_flow": 15,
                "strong_conclusion": 10
            },
            "language_quality": {
                "grammar_accuracy": 20,
                "vocabulary_appropriateness": 10,
                "tone_consistency": 10
            },
            "audience_alignment": {
                "target_audience_fit": 15,
                "value_proposition": 10
            }
        }

    # =============================================================================
    # CONTENT WRITING AGENTS
    # =============================================================================
    
    def content_writing_enhanced(self, state) -> Dict[str, Any]:
        """
        ENHANCED: Content Writing
        AGENT: Content Writer
        PURPOSE: Sophisticated content generation with style adaptation and quality optimization
        """
        print("✍️ ENHANCED CONTENT WRITING AGENT")
        state.current_agent = "content_writer"
        state.workflow_stage = "writing"
        start_time = datetime.now()
        
        try:
            # Retrieve content plan and strategy
            content_plan = state.metadata.get("content_plan", {})
            section_strategies = state.metadata.get("section_strategies", {})
            keyword_plan = state.metadata.get("keyword_plan", {})
            
            # Generate content using advanced writing strategy
            writing_context = self._build_comprehensive_writing_context(state, content_plan, keyword_plan)
            
            # Create section-by-section content
            content_sections = self._generate_content_by_sections(state, writing_context, section_strategies)
            
            # Assemble and refine complete content
            assembled_content = self._assemble_and_refine_content(content_sections, writing_context)
            
            # Apply style and tone adjustments
            final_content = self._apply_style_adjustments(assembled_content, writing_context)
            
            # Update state with generated content
            state.draft_content = final_content["content"]
            state.word_count = final_content["word_count"]
            state.content_sections = content_sections
            
            # Store detailed writing analytics
            state.metadata.update({
                "writing_context": writing_context,
                "content_analytics": final_content["analytics"],
                "section_breakdown": {
                    "total_sections": len(content_sections),
                    "average_section_length": statistics.mean([s["word_count"] for s in content_sections]),
                    "style_consistency_score": final_content["style_score"]
                },
                "writing_timestamp": datetime.now().isoformat()
            })
            
            print(f"📝 Content writing complete:")
            print(f"   📊 Word Count: {state.word_count}")
            print(f"   📋 Sections: {len(content_sections)}")
            print(f"   🎯 Style Score: {final_content['style_score']:.1f}/100")
            
        except Exception as e:
            state.error_messages.append(f"Content writing error: {str(e)}")
            print(f"❌ Content writing failed: {e}")
        
        state.processing_time["writing"] = (datetime.now() - start_time).total_seconds()
        return state
    
    def _build_comprehensive_writing_context(self, state, content_plan: Dict[str, Any], keyword_plan: Dict[str, Any]) -> Dict[str, Any]:
        """Build comprehensive context for content generation"""
        
        context = {
            # Basic parameters
            "topic": state.topic,
            "content_type": state.content_type,
            "target_audience": state.target_audience or "technology professionals",
            "word_count_target": {
                "min": state.metadata.get("content_config", {}).get("min_words", 300),
                "max": state.metadata.get("content_config", {}).get("max_words", 1000)
            },
            
            # Research insights
            "research_summary": state.research_summary,
            "trending_topics": state.trending_topics,
            "research_confidence": state.research_confidence,
            
            # Content strategy
            "primary_objective": content_plan.get("primary_objective", "inform and engage"),
            "tone_and_style": content_plan.get("tone_and_style", {}),
            "engagement_strategy": content_plan.get("engagement_strategy", {}),
            "differentiation_factors": content_plan.get("differentiation_factors", []),
            
            # SEO and keywords
            "primary_keywords": keyword_plan.get("primary_keywords", []),
            "secondary_keywords": keyword_plan.get("secondary_keywords", []),
            "semantic_variations": keyword_plan.get("semantic_variations", {}),
            "long_tail_keywords": keyword_plan.get("long_tail_opportunities", []),
            
            # Writing guidelines
            "writing_guidelines": self.writing_guidelines.get(state.content_type, {}),
            "industry_context": state.metadata.get("industry_context", "general")
        }
        
        return context
    
    def _generate_content_by_sections(self, state, writing_context: Dict[str, Any], section_strategies: Dict[str, Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate content section by section with specialized strategies"""
        
        content_sections = []
        total_target_words = writing_context["word_count_target"]["max"]
        
        for section_detail in state.content_sections:
            section_name = section_detail["section_name"]
            section_strategy = section_strategies.get(section_name, {})
            
            print(f"📝 Generating section: {section_name}")
            
            # Calculate target words for this section
            section_word_target = self._calculate_section_word_target(
                section_strategy, total_target_words, len(state.content_sections)
            )
            
            # Generate section content
            section_content = self._generate_individual_section(
                section_name, section_strategy, writing_context, section_word_target
            )
            
            content_sections.append(section_content)
        
        return content_sections
    
    def _calculate_section_word_target(self, section_strategy: Dict[str, Any], total_words: int, total_sections: int) -> int:
        """Calculate target word count for individual section"""
        
        length_target = section_strategy.get("length_target", "proportional")
        
        # Parse percentage-based targets
        if "%" in str(length_target):
            percentage = float(re.findall(r'\d+', length_target)[0]) / 100
            return int(total_words * percentage)
        
        # Handle specific targets
        if "introduction" in length_target.lower():
            return int(total_words * 0.15)  # 15% for introduction
        elif "main" in length_target.lower() or "body" in length_target.lower():
            return int(total_words * 0.60)  # 60% for main content
        elif "conclusion" in length_target.lower():
            return int(total_words * 0.15)  # 15% for conclusion
        else:
            # Equal distribution
            return int(total_words / total_sections)
    
    def _generate_individual_section(self, section_name: str, section_strategy: Dict[str, Any], 
                                   writing_context: Dict[str, Any], word_target: int) -> Dict[str, Any]:
        """Generate content for individual section with specialized approach"""
        
        # Build section-specific prompt
        section_prompt = self._build_section_prompt(section_name, section_strategy, writing_context, word_target)
        
        try:
            # Generate section content
            section_text = writing_tool.run(section_prompt)
            
            if not isinstance(section_text, str) or len(section_text) < 50:
                # Fallback content generation
                section_text = self._generate_fallback_section_content(section_name, writing_context)
            
            # Analyze generated section
            section_analysis = self._analyze_section_content(section_text, section_strategy, writing_context)
            
            return {
                "section_name": section_name,
                "content": section_text,
                "word_count": len(section_text.split()),
                "analysis": section_analysis,
                "target_words": word_target,
                "strategy_applied": section_strategy
            }
            
        except Exception as e:
            print(f"⚠️ Section generation failed for {section_name}: {e}")
            return {
                "section_name": section_name,
                "content": self._generate_fallback_section_content(section_name, writing_context),
                "word_count": 0,
                "analysis": {"error": str(e)},
                "target_words": word_target,
                "strategy_applied": section_strategy
            }
    
    def _build_section_prompt(self, section_name: str, section_strategy: Dict[str, Any], 
                            writing_context: Dict[str, Any], word_target: int) -> str:
        """Build specialized prompt for section generation"""
        
        base_prompt = f"""
        Generate a {section_name.replace('_', ' ')} section for {writing_context['content_type']} content about: {writing_context['topic']}
        
        SECTION REQUIREMENTS:
        - Purpose: {section_strategy.get('purpose', f'Provide valuable information about {section_name}')}
        - Target Length: {word_target} words
        - Key Elements: {', '.join(section_strategy.get('key_elements', []))}
        - Tone: {writing_context['tone_and_style'].get('tone', 'professional')}
        
        CONTENT CONTEXT:
        - Target Audience: {writing_context['target_audience']}
        - Industry: {writing_context['industry_context']}
        - Primary Objective: {writing_context['primary_objective']}
        
        KEYWORD INTEGRATION:
        - Primary Keywords: {', '.join(writing_context['primary_keywords'][:3])}
        - Section Keywords: {', '.join(section_strategy.get('relevant_keywords', []))}
        - Integration Style: {section_strategy.get('keyword_integration', 'natural and contextual')}
        
        RESEARCH INSIGHTS TO INCORPORATE:
        {writing_context['research_summary']}
        
        WRITING GUIDELINES:
        - Style: {writing_context['tone_and_style'].get('style', 'professional')}
        - Voice: {writing_context['tone_and_style'].get('voice', 'authoritative yet accessible')}
        - Engagement: {', '.join(writing_context.get('engagement_strategy', {}).get('engagement_elements', []))}
        
        Generate compelling, informative content that fulfills the section purpose while maintaining consistency with the overall content strategy.
        """
        
        # Add section-specific instructions
        if section_name == "introduction":
            base_prompt += "\n\nSPECIAL INSTRUCTIONS: Start with a compelling hook that immediately engages the reader. Establish credibility and clearly preview the value they'll receive."
        
        elif section_name == "main_content" or section_name == "main_analysis":
            base_prompt += "\n\nSPECIAL INSTRUCTIONS: Provide detailed, evidence-based information. Use examples, data, and insights from research. Structure with clear subpoints for readability."
        
        elif section_name == "conclusion":
            base_prompt += "\n\nSPECIAL INSTRUCTIONS: Summarize key takeaways and provide a clear call-to-action. End with actionable next steps for the reader."
        
        elif section_name == "benefits":
            base_prompt += "\n\nSPECIAL INSTRUCTIONS: Focus on specific, quantifiable benefits. Use bullet points or numbered lists. Connect benefits to reader pain points."
        
        return base_prompt
    
    def _generate_fallback_section_content(self, section_name: str, writing_context: Dict[str, Any]) -> str:
        """Generate fallback content when primary generation fails"""
        
        topic = writing_context["topic"]
        
        fallback_templates = {
            "introduction": f"Understanding {topic} is crucial in today's rapidly evolving landscape. This comprehensive guide explores the key aspects and practical applications that matter most to professionals and organizations.",
            
            "main_content": f"The implementation of {topic} involves several critical considerations. Research indicates that successful adoption requires careful planning, appropriate resources, and strategic alignment with organizational goals.",
            
            "benefits": f"The primary benefits of {topic} include improved efficiency, enhanced productivity, and competitive advantages. Organizations that adopt this approach typically see measurable improvements in their operations.",
            
            "conclusion": f"In conclusion, {topic} represents a significant opportunity for growth and improvement. By understanding the key principles and implementing best practices, organizations can achieve substantial benefits and competitive advantages."
        }
        
        return fallback_templates.get(section_name, f"This section provides important information about {topic} that is relevant to {writing_context['target_audience']}.")
    
    def _analyze_section_content(self, section_text: str, section_strategy: Dict[str, Any], writing_context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze generated section content for quality and adherence to strategy"""
        
        analysis = {
            "word_count": len(section_text.split()),
            "sentence_count": len([s for s in section_text.split('.') if s.strip()]),
            "keyword_usage": {},
            "readability_score": 0,
            "strategy_adherence": 0
        }
        
        # Keyword usage analysis
        section_lower = section_text.lower()
        for keyword in writing_context["primary_keywords"]:
            keyword_count = section_lower.count(keyword.lower())
            analysis["keyword_usage"][keyword] = keyword_count
        
        # Basic readability assessment
        if analysis["sentence_count"] > 0:
            avg_words_per_sentence = analysis["word_count"] / analysis["sentence_count"]
            # Simple readability score (inverse of complexity)
            analysis["readability_score"] = max(0, 100 - (avg_words_per_sentence - 15) * 2)
        
        # Strategy adherence assessment
        key_elements = section_strategy.get("key_elements", [])
        adherence_score = 0
        for element in key_elements:
            if any(word in section_lower for word in element.lower().split()):
                adherence_score += 1
        
        if key_elements:
            analysis["strategy_adherence"] = (adherence_score / len(key_elements)) * 100
        
        return analysis
    
    def _assemble_and_refine_content(self, content_sections: List[Dict[str, Any]], writing_context: Dict[str, Any]) -> Dict[str, Any]:
        """Assemble sections and refine for consistency and flow"""
        
        # Combine section content
        full_content = "\n\n".join([section["content"] for section in content_sections])
        
        # Calculate overall metrics
        total_words = sum([section["word_count"] for section in content_sections])
        
        # Assess content flow and consistency
        flow_analysis = self._assess_content_flow(content_sections)
        
        # Apply consistency improvements
        refined_content = self._improve_content_consistency(full_content, writing_context)
        
        # Calculate analytics
        analytics = {
            "sections_generated": len(content_sections),
            "total_word_count": total_words,
            "flow_score": flow_analysis["score"],
            "consistency_improvements": refined_content["improvements_made"],
            "keyword_distribution": self._analyze_keyword_distribution(refined_content["content"], writing_context),
            "readability_assessment": self._assess_overall_readability(refined_content["content"])
        }
        
        return {
            "content": refined_content["content"],
            "word_count": len(refined_content["content"].split()),
            "analytics": analytics,
            "flow_analysis": flow_analysis
        }
    
    def _assess_content_flow(self, content_sections: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Assess the logical flow between content sections"""
        
        flow_score = 100  # Start with perfect score and deduct for issues
        flow_issues = []
        
        # Check section length balance
        word_counts = [section["word_count"] for section in content_sections]
        if word_counts:
            avg_length = statistics.mean(word_counts)
            for i, count in enumerate(word_counts):
                if count < avg_length * 0.3:  # Section too short
                    flow_issues.append(f"Section {i+1} is significantly shorter than average")
                    flow_score -= 10
                elif count > avg_length * 3:  # Section too long
                    flow_issues.append(f"Section {i+1} is significantly longer than average")
                    flow_score -= 5
        
        # Check for logical progression
        section_names = [section["section_name"] for section in content_sections]
        expected_order = ["introduction", "background", "main_content", "benefits", "implementation", "conclusion"]
        
        order_score = self._calculate_order_score(section_names, expected_order)
        flow_score = flow_score * (order_score / 100)
        
        return {
            "score": max(0, flow_score),
            "issues": flow_issues,
            "order_score": order_score,
            "section_balance": "balanced" if not flow_issues else "needs_adjustment"
        }
    
    def _calculate_order_score(self, actual_order: List[str], expected_order: List[str]) -> float:
        """Calculate score for section ordering"""
        
        score = 100
        
        # Check if introduction is first
        if actual_order and "introduction" in actual_order[0].lower():
            score += 0  # No penalty
        else:
            score -= 20
        
        # Check if conclusion is last
        if actual_order and "conclusion" in actual_order[-1].lower():
            score += 0  # No penalty
        else:
            score -= 20
        
        return max(0, score)
    
    def _improve_content_consistency(self, content: str, writing_context: Dict[str, Any]) -> Dict[str, Any]:
        """Improve content consistency and coherence"""
        
        improvements_made = []
        improved_content = content
        
        # Fix paragraph breaks (ensure proper spacing)
        if "\n\n\n" in improved_content:
            improved_content = re.sub(r'\n{3,}', '\n\n', improved_content)
            improvements_made.append("Fixed excessive paragraph breaks")
        
        # Ensure consistent keyword usage
        primary_keywords = writing_context["primary_keywords"]
        for keyword in primary_keywords[:3]:  # Focus on top 3 keywords
            keyword_variations = [keyword, keyword.capitalize(), keyword.upper()]
            
            # Count occurrences of each variation
            variation_counts = {}
            for variation in keyword_variations:
                variation_counts[variation] = improved_content.count(variation)
            
            # Standardize to most common variation (or lowercase if tie)
            if variation_counts:
                most_common = max(variation_counts.items(), key=lambda x: x[1])
                if most_common[1] > 1:  # Only standardize if keyword appears multiple times
                    for variation in keyword_variations:
                        if variation != most_common[0]:
                            improved_content = improved_content.replace(variation, most_common[0])
                    improvements_made.append(f"Standardized keyword '{keyword}' usage")
        
        # Improve transition consistency
        transition_improvements = self._improve_transitions(improved_content)
        improved_content = transition_improvements["content"]
        improvements_made.extend(transition_improvements["improvements"])
        
        return {
            "content": improved_content,
            "improvements_made": improvements_made
        }
    
    def _improve_transitions(self, content: str) -> Dict[str, Any]:
        """Improve transitions between paragraphs and sections"""
        
        improvements = []
        paragraphs = content.split('\n\n')
        
        # Add transitions where needed (simplified approach)
        transition_words = {
            "addition": ["Furthermore", "Additionally", "Moreover"],
            "contrast": ["However", "Nevertheless", "On the other hand"],
            "conclusion": ["Therefore", "As a result", "In conclusion"]
        }
        
        improved_paragraphs = []
        for i, paragraph in enumerate(paragraphs):
            # Keep paragraph as is for now (more sophisticated transition analysis would go here)
            improved_paragraphs.append(paragraph)
        
        return {
            "content": '\n\n'.join(improved_paragraphs),
            "improvements": improvements
        }
    
    def _analyze_keyword_distribution(self, content: str, writing_context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze keyword distribution throughout content"""
        
        content_lower = content.lower()
        word_count = len(content.split())
        
        distribution = {
            "primary_keywords": {},
            "secondary_keywords": {},
            "density_scores": {},
            "placement_analysis": {}
        }
        
        # Analyze primary keywords
        for keyword in writing_context["primary_keywords"]:
            keyword_count = content_lower.count(keyword.lower())
            density = (keyword_count / word_count) * 100 if word_count > 0 else 0
            
            distribution["primary_keywords"][keyword] = keyword_count
            distribution["density_scores"][keyword] = density
            
            # Analyze placement
            first_100_words = ' '.join(content.split()[:100]).lower()
            last_100_words = ' '.join(content.split()[-100:]).lower()
            
            distribution["placement_analysis"][keyword] = {
                "in_introduction": keyword.lower() in first_100_words,
                "in_conclusion": keyword.lower() in last_100_words,
                "total_occurrences": keyword_count
            }
        
        # Analyze secondary keywords
        for keyword in writing_context["secondary_keywords"]:
            keyword_count = content_lower.count(keyword.lower())
            density = (keyword_count / word_count) * 100 if word_count > 0 else 0
            
            distribution["secondary_keywords"][keyword] = keyword_count
            distribution["density_scores"][keyword] = density
        
        return distribution
    
    def _assess_overall_readability(self, content: str) -> Dict[str, Any]:
        """Assess overall content readability"""
        
        words = content.split()
        sentences = [s.strip() for s in content.split('.') if s.strip()]
        
        if not sentences:
            return {"score": 0, "level": "unreadable", "issues": ["No complete sentences found"]}
        
        # Basic readability metrics
        avg_words_per_sentence = len(words) / len(sentences)
        avg_chars_per_word = sum(len(word) for word in words) / len(words) if words else 0
        
        # Simple readability score calculation
        readability_score = 206.835 - (1.015 * avg_words_per_sentence) - (84.6 * (avg_chars_per_word / 4.7))
        readability_score = max(0, min(100, readability_score))
        
        # Determine readability level
        if readability_score >= 90:
            level = "very_easy"
        elif readability_score >= 80:
            level = "easy"
        elif readability_score >= 70:
            level = "fairly_easy"
        elif readability_score >= 60:
            level = "standard"
        elif readability_score >= 50:
            level = "fairly_difficult"
        elif readability_score >= 30:
            level = "difficult"
        else:
            level = "very_difficult"
        
        # Identify potential issues
        issues = []
        if avg_words_per_sentence > 25:
            issues.append("Sentences are too long on average")
        if avg_chars_per_word > 6:
            issues.append("Words are too complex on average")
        
        return {
            "score": readability_score,
            "level": level,
            "avg_words_per_sentence": avg_words_per_sentence,
            "avg_chars_per_word": avg_chars_per_word,
            "issues": issues
        }
    
    def _apply_style_adjustments(self, assembled_content: Dict[str, Any], writing_context: Dict[str, Any]) -> Dict[str, Any]:
        """Apply final style and tone adjustments to content"""
        
        content = assembled_content["content"]
        target_style = writing_context["tone_and_style"]
        
        # Style consistency scoring
        style_score = self._calculate_style_consistency_score(content, target_style)
        
        # Apply tone adjustments if needed
        if style_score < 80:
            adjusted_content = self._adjust_content_tone(content, target_style)
            style_score = self._calculate_style_consistency_score(adjusted_content, target_style)
        else:
            adjusted_content = content
        
        return {
            "content": adjusted_content,
            "word_count": len(adjusted_content.split()),
            "style_score": style_score,
            "analytics": assembled_content["analytics"]
        }
    
    def _calculate_style_consistency_score(self, content: str, target_style: Dict[str, Any]) -> float:
        """Calculate style consistency score"""
        
        score = 100
        content_lower = content.lower()
        
        # Check tone consistency
        tone = target_style.get("tone", "professional")
        
        if tone == "professional":
            # Look for professional language indicators
            professional_indicators = ["analysis", "implementation", "strategy", "optimize", "efficiency"]
            found_indicators = sum(1 for indicator in professional_indicators if indicator in content_lower)
            if found_indicators < 2:
                score -= 20
            
            # Penalize overly casual language
            casual_words = ["gonna", "wanna", "kinda", "sorta"]
            casual_count = sum(1 for word in casual_words if word in content_lower)
            score -= casual_count * 10
        
        elif tone == "conversational":
            # Look for conversational elements
            conversational_indicators = ["you", "your", "we", "our", "let's"]
            found_indicators = sum(1 for indicator in conversational_indicators if indicator in content_lower)
            if found_indicators < 3:
                score -= 15
        
        return max(0, score)
    
    def _adjust_content_tone(self, content: str, target_style: Dict[str, Any]) -> str:
        """Adjust content tone to match target style"""
        
        # This is a simplified tone adjustment
        # In a production system, this would use more sophisticated NLP
        
        tone = target_style.get("tone", "professional")
        
        if tone == "professional":
            # Replace casual phrases with professional alternatives
            adjustments = {
                "pretty good": "effective",
                "really important": "crucial",
                "a lot of": "numerous",
                "kind of": "somewhat"
            }
            
            for casual, professional in adjustments.items():
                content = content.replace(casual, professional)
        
        return content

    # =============================================================================
    # CONTENT REVIEW AND REVISION AGENTS
    # =============================================================================
    
    def content_review_enhanced(self, state) -> Dict[str, Any]:
        """
        ENHANCED: Content Review
        AGENT: Content Editor
        PURPOSE: Comprehensive content quality assessment and improvement recommendations
        """
        print("📖 ENHANCED CONTENT REVIEW")
        state.current_agent = "content_editor"
        state.workflow_stage = "review"
        start_time = datetime.now()
        
        if not state.draft_content:
            state.error_messages.append("No content available for review")
            return state
        
        try:
            # Comprehensive content analysis
            content_analysis = self._comprehensive_content_analysis(state)
            
            # Structure and organization assessment
            structure_assessment = self._assess_content_structure(state)
            
            # Quality scoring with detailed breakdown
            quality_assessment = self._detailed_quality_assessment(state, content_analysis, structure_assessment)
            
            # Generate improvement recommendations
            improvement_recommendations = self._generate_improvement_recommendations(quality_assessment)
            
            # Update state with review results
            state.metadata.update({
                "content_analysis": content_analysis,
                "structure_assessment": structure_assessment,
                "quality_assessment": quality_assessment,
                "improvement_recommendations": improvement_recommendations,
                "review_timestamp": datetime.now().isoformat()
            })
            
            # Calculate overall review score
            overall_score = quality_assessment["overall_score"]
            
            print(f"📊 Content review complete:")
            print(f"   🎯 Overall Score: {overall_score:.1f}/100")
            print(f"   📝 Word Count: {state.word_count}")
            print(f"   📋 Recommendations: {len(improvement_recommendations)}")
            
        except Exception as e:
            state.error_messages.append(f"Content review error: {str(e)}")
            print(f"❌ Content review failed: {e}")
        
        state.processing_time["review"] = (datetime.now() - start_time).total_seconds()
        return state
    
    def _comprehensive_content_analysis(self, state) -> Dict[str, Any]:
        """Perform comprehensive analysis of content quality and characteristics"""
        
        content = state.draft_content
        content_sections = state.content_sections or []
        
        analysis = {
            "basic_metrics": self._calculate_basic_content_metrics(content),
            "linguistic_analysis": self._perform_linguistic_analysis(content),
            "section_analysis": self._analyze_content_sections(content_sections),
            "keyword_analysis": self._analyze_keyword_usage(content, state),
            "audience_alignment": self._assess_audience_alignment(content, state)
        }
        
        return analysis
    
    def _calculate_basic_content_metrics(self, content: str) -> Dict[str, Any]:
        """Calculate basic content metrics"""
        
        words = content.split()
        sentences = [s.strip() for s in content.split('.') if s.strip()]
        paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]
        
        return {
            "word_count": len(words),
            "sentence_count": len(sentences),
            "paragraph_count": len(paragraphs),
            "character_count": len(content),
            "avg_words_per_sentence": len(words) / len(sentences) if sentences else 0,
            "avg_sentences_per_paragraph": len(sentences) / len(paragraphs) if paragraphs else 0,
            "avg_chars_per_word": sum(len(word) for word in words) / len(words) if words else 0
        }
    
    def _perform_linguistic_analysis(self, content: str) -> Dict[str, Any]:
        """Perform linguistic analysis of content"""
        
        content_lower = content.lower()
        words = content.split()
        
        # Vocabulary complexity analysis
        complex_words = [word for word in words if len(word) > 6]
        complexity_ratio = len(complex_words) / len(words) if words else 0
        
        # Passive voice detection (simplified)
        passive_indicators = ["was", "were", "been", "being"]
        passive_count = sum(1 for indicator in passive_indicators if indicator in content_lower)
        
        # Readability assessment
        readability = self._assess_overall_readability(content)
        
        # Tone analysis (simplified)
        tone_indicators = {
            "formal": ["furthermore", "therefore", "consequently", "analysis", "implementation"],
            "casual": ["you", "your", "we", "our", "let's", "really", "pretty"],
            "technical": ["system", "process", "methodology", "framework", "algorithm"]
        }
        
        tone_scores = {}
        for tone, indicators in tone_indicators.items():
            score = sum(1 for indicator in indicators if indicator in content_lower)
            tone_scores[tone] = score
        
        return {
            "vocabulary_complexity": complexity_ratio,
            "passive_voice_count": passive_count,
            "readability": readability,
            "tone_analysis": tone_scores,
            "dominant_tone": max(tone_scores, key=tone_scores.get) if tone_scores else "neutral"
        }
    
    def _analyze_content_sections(self, content_sections: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze individual content sections"""
        
        if not content_sections:
            return {"status": "no_sections_available"}
        
        section_analysis = {
            "total_sections": len(content_sections),
            "section_balance": {},
            "section_quality": {},
            "flow_assessment": {}
        }
        
        # Analyze section balance
        word_counts = [section.get("word_count", 0) for section in content_sections]
        if word_counts:
            avg_length = statistics.mean(word_counts)
            section_analysis["section_balance"] = {
                "average_length": avg_length,
                "length_variance": statistics.variance(word_counts) if len(word_counts) > 1 else 0,
                "balanced": all(0.5 * avg_length <= count <= 2 * avg_length for count in word_counts)
            }
        
        # Analyze individual section quality
        for section in content_sections:
            section_name = section.get("section_name", "unknown")
            section_content = section.get("content", "")
            
            if section_content:
                quality_score = self._assess_section_quality(section_content, section_name)
                section_analysis["section_quality"][section_name] = quality_score
        
        return section_analysis
    
    def _assess_section_quality(self, section_content: str, section_name: str) -> Dict[str, Any]:
        """Assess quality of individual section"""
        
        quality_score = 100
        issues = []
        
        word_count = len(section_content.split())
        
        # Check minimum length requirements
        min_lengths = {
            "introduction": 50,
            "main_content": 100,
            "conclusion": 30
        }
        
        min_length = min_lengths.get(section_name, 40)
        if word_count < min_length:
            quality_score -= 20
            issues.append(f"Section too short (minimum {min_length} words)")
        
        # Check for proper structure
        if section_name == "introduction":
            if not any(word in section_content.lower() for word in ["introduction", "overview", "explore", "discuss"]):
                quality_score -= 10
                issues.append("Introduction lacks proper opening elements")
        
        elif section_name == "conclusion":
            if not any(word in section_content.lower() for word in ["conclusion", "summary", "finally", "in summary"]):
                quality_score -= 10
                issues.append("Conclusion lacks proper closing elements")
        
        return {
            "score": max(0, quality_score),
            "issues": issues,
            "word_count": word_count
        }
    
    def _analyze_keyword_usage(self, content: str, state) -> Dict[str, Any]:
        """Analyze keyword usage effectiveness"""
        
        content_lower = content.lower()
        word_count = len(content.split())
        
        # Get keywords from state
        primary_keywords = state.primary_keywords or []
        extracted_keywords = state.extracted_keywords or []
        
        keyword_analysis = {
            "primary_keyword_usage": {},
            "keyword_density": {},
            "keyword_placement": {},
            "overall_seo_score": 0
        }
        
        # Analyze primary keywords
        for keyword in primary_keywords:
            keyword_count = content_lower.count(keyword.lower())
            density = (keyword_count / word_count) * 100 if word_count > 0 else 0
            
            keyword_analysis["primary_keyword_usage"][keyword] = keyword_count
            keyword_analysis["keyword_density"][keyword] = density
            
            # Check placement
            first_100 = ' '.join(content.split()[:100]).lower()
            last_100 = ' '.join(content.split()[-100:]).lower()
            
            keyword_analysis["keyword_placement"][keyword] = {
                "in_beginning": keyword.lower() in first_100,
                "in_end": keyword.lower() in last_100,
                "well_distributed": keyword_count >= 2 and density <= 3.0
            }
        
        # Calculate overall SEO score
        seo_score = 100
        
        for keyword in primary_keywords[:3]:  # Focus on top 3 keywords
            density = keyword_analysis["keyword_density"].get(keyword, 0)
            placement = keyword_analysis["keyword_placement"].get(keyword, {})
            
            # Optimal density is 1-2%
            if density < 0.5:
                seo_score -= 15  # Too low
            elif density > 3.0:
                seo_score -= 10  # Too high
            
            # Good placement bonus
            if placement.get("in_beginning") and placement.get("well_distributed"):
                seo_score += 5
        
        keyword_analysis["overall_seo_score"] = max(0, seo_score)
        
        return keyword_analysis
    
    def _assess_audience_alignment(self, content: str, state) -> Dict[str, Any]:
        """Assess how well content aligns with target audience"""
        
        target_audience = state.target_audience or "technology professionals"
        content_type = state.content_type
        content_lower = content.lower()
        
        alignment_score = 100
        alignment_factors = []
        
        # Audience-specific vocabulary assessment
        audience_vocabularies = {
            "technology professionals": ["implementation", "integration", "optimization", "scalability", "architecture"],
            "small business owners": ["cost-effective", "ROI", "growth", "efficiency", "practical"],
            "startup founders": ["scalable", "innovation", "competitive advantage", "funding", "growth"],
            "executives": ["strategic", "business value", "ROI", "competitive", "leadership"]
        }
        
        expected_vocab = audience_vocabularies.get(target_audience, audience_vocabularies["technology professionals"])
        vocab_matches = sum(1 for word in expected_vocab if word in content_lower)
        
        if vocab_matches >= 3:
            alignment_factors.append("Appropriate vocabulary for target audience")
        else:
            alignment_score -= 15
            alignment_factors.append("Limited use of audience-appropriate vocabulary")
        
        # Content depth assessment
        if content_type == "blog_post":
            if len(content.split()) < 500:
                alignment_score -= 10
                alignment_factors.append("Content may be too brief for blog post audience expectations")
        
        elif content_type == "social_media":
            if len(content.split()) > 50:
                alignment_score -= 5
                alignment_factors.append("Content may be too long for social media audience")
        
        # Technical complexity assessment
        technical_terms = ["API", "framework", "algorithm", "infrastructure", "methodology"]
        tech_count = sum(1 for term in technical_terms if term.lower() in content_lower)
        
        if target_audience == "technology professionals" and tech_count < 2:
            alignment_score -= 10
            alignment_factors.append("May lack sufficient technical depth for tech professionals")
        elif target_audience == "small business owners" and tech_count > 5:
            alignment_score -= 10
            alignment_factors.append("May be too technical for small business owners")
        
        return {
            "alignment_score": max(0, alignment_score),
            "alignment_factors": alignment_factors,
            "vocabulary_matches": vocab_matches,
            "technical_complexity": tech_count
        }
    
    def _assess_content_structure(self, state) -> Dict[str, Any]:
        """Assess overall content structure and organization"""
        
        content = state.draft_content
        content_sections = state.content_sections or []
        
        structure_score = 100
        structure_issues = []
        
        # Check for proper introduction
        first_paragraph = content.split('\n\n')[0] if '\n\n' in content else content[:200]
        if not any(word in first_paragraph.lower() for word in ["introduction", "overview", "explore", "understanding"]):
            if len(first_paragraph.split()) < 30:
                structure_score -= 15
                structure_issues.append("Weak or missing introduction")
        
        # Check for proper conclusion
        last_paragraph = content.split('\n\n')[-1] if '\n\n' in content else content[-200:]
        if not any(word in last_paragraph.lower() for word in ["conclusion", "summary", "finally", "in conclusion"]):
            if len(last_paragraph.split()) < 20:
                structure_score -= 15
                structure_issues.append("Weak or missing conclusion")
        
        # Check section flow
        if content_sections:
            section_names = [section.get("section_name", "") for section in content_sections]
            
            # Check if introduction comes first
            if section_names and "introduction" not in section_names[0].lower():
                structure_score -= 10
                structure_issues.append("Introduction should be first section")
            
            # Check if conclusion comes last
            if section_names and "conclusion" not in section_names[-1].lower():
                structure_score -= 10
                structure_issues.append("Conclusion should be last section")
        
        # Check paragraph structure
        paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]
        if len(paragraphs) < 3:
            structure_score -= 15
            structure_issues.append("Content needs better paragraph structure")
        
        # Check for headings/subheadings (simplified detection)
        heading_indicators = content.count('\n#') + content.count('**') + content.count('##')
        if len(content.split()) > 500 and heading_indicators < 2:
            structure_score -= 10
            structure_issues.append("Long content should include headings for better structure")
        
        return {
            "structure_score": max(0, structure_score),
            "structure_issues": structure_issues,
            "paragraph_count": len(paragraphs),
            "has_proper_intro": "introduction" in first_paragraph.lower(),
            "has_proper_conclusion": any(word in last_paragraph.lower() for word in ["conclusion", "summary", "finally"])
        }
    
    def _detailed_quality_assessment(self, state, content_analysis: Dict[str, Any], structure_assessment: Dict[str, Any]) -> Dict[str, Any]:
        """Perform detailed quality assessment with weighted scoring"""
        
        # Weight factors for different quality aspects
        weights = {
            "content_structure": 0.25,
            "language_quality": 0.20,
            "audience_alignment": 0.20,
            "keyword_optimization": 0.15,
            "readability": 0.10,
            "length_appropriateness": 0.10
        }
        
        # Calculate individual scores
        scores = {
            "content_structure": structure_assessment.get("structure_score", 0),
            "language_quality": self._calculate_language_quality_score(content_analysis),
            "audience_alignment": content_analysis.get("audience_alignment", {}).get("alignment_score", 0),
            "keyword_optimization": content_analysis.get("keyword_analysis", {}).get("overall_seo_score", 0),
            "readability": content_analysis.get("linguistic_analysis", {}).get("readability", {}).get("score", 0),
            "length_appropriateness": self._assess_length_appropriateness(state)
        }
        
        # Calculate weighted overall score
        overall_score = sum(scores[aspect] * weights[aspect] for aspect in weights)
        
        # Determine quality level
        if overall_score >= 90:
            quality_level = "excellent"
        elif overall_score >= 80:
            quality_level = "good"
        elif overall_score >= 70:
            quality_level = "satisfactory"
        elif overall_score >= 60:
            quality_level = "needs_improvement"
        else:
            quality_level = "poor"
        
        return {
            "overall_score": overall_score,
            "quality_level": quality_level,
            "individual_scores": scores,
            "weights": weights,
            "detailed_breakdown": self._create_detailed_breakdown(scores, content_analysis, structure_assessment)
        }
    
    def _calculate_language_quality_score(self, content_analysis: Dict[str, Any]) -> float:
        """Calculate language quality score"""
        
        linguistic_analysis = content_analysis.get("linguistic_analysis", {})
        basic_metrics = content_analysis.get("basic_metrics", {})
        
        score = 100
        
        # Assess sentence length
        avg_words_per_sentence = basic_metrics.get("avg_words_per_sentence", 0)
        if avg_words_per_sentence > 25:
            score -= 15  # Too long
        elif avg_words_per_sentence < 8:
            score -= 10  # Too short
        
        # Assess vocabulary complexity
        complexity = linguistic_analysis.get("vocabulary_complexity", 0)
        if complexity > 0.4:  # Too complex
            score -= 10
        elif complexity < 0.1:  # Too simple
            score -= 5
        
        # Assess passive voice usage
        passive_count = linguistic_analysis.get("passive_voice_count", 0)
        total_sentences = basic_metrics.get("sentence_count", 1)
        passive_ratio = passive_count / total_sentences
        
        if passive_ratio > 0.3:  # Too much passive voice
            score -= 15
        
        return max(0, score)
    
    def _assess_length_appropriateness(self, state) -> float:
        """Assess if content length is appropriate for content type and audience"""
        
        word_count = state.word_count
        content_type = state.content_type
        target_config = state.metadata.get("content_config", {})
        
        min_words = target_config.get("min_words", 300)
        max_words = target_config.get("max_words", 1000)
        
        score = 100
        
        if word_count < min_words:
            deficit = min_words - word_count
            score -= min(50, (deficit / min_words) * 100)  # Up to 50 point penalty
        elif word_count > max_words:
            excess = word_count - max_words
            score -= min(30, (excess / max_words) * 100)  # Up to 30 point penalty
        
        return max(0, score)
    
    def _create_detailed_breakdown(self, scores: Dict[str, float], content_analysis: Dict[str, Any], structure_assessment: Dict[str, Any]) -> Dict[str, Any]:
        """Create detailed breakdown of quality assessment"""
        
        breakdown = {
            "strengths": [],
            "weaknesses": [],
            "specific_issues": [],
            "recommendations": []
        }
        
        # Identify strengths
        for aspect, score in scores.items():
            if score >= 85:
                breakdown["strengths"].append(f"Excellent {aspect.replace('_', ' ')}")
            elif score >= 75:
                breakdown["strengths"].append(f"Good {aspect.replace('_', ' ')}")
        
        # Identify weaknesses
        for aspect, score in scores.items():
            if score < 60:
                breakdown["weaknesses"].append(f"Poor {aspect.replace('_', ' ')}")
            elif score < 75:
                breakdown["weaknesses"].append(f"Needs improvement in {aspect.replace('_', ' ')}")
        
        # Extract specific issues
        structure_issues = structure_assessment.get("structure_issues", [])
        breakdown["specific_issues"].extend(structure_issues)
        
        audience_factors = content_analysis.get("audience_alignment", {}).get("alignment_factors", [])
        breakdown["specific_issues"].extend([f for f in audience_factors if "limited" in f.lower() or "lack" in f.lower()])
        
        return breakdown
    
    def _generate_improvement_recommendations(self, quality_assessment: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate specific improvement recommendations based on quality assessment"""
        
        recommendations = []
        scores = quality_assessment.get("individual_scores", {})
        breakdown = quality_assessment.get("detailed_breakdown", {})
        
        # Structure recommendations
        if scores.get("content_structure", 0) < 75:
            recommendations.append({
                "category": "structure",
                "priority": "high",
                "recommendation": "Improve content structure with clearer introduction and conclusion",
                "specific_actions": [
                    "Add compelling opening hook in introduction",
                    "Ensure logical flow between sections",
                    "Strengthen conclusion with clear takeaways"
                ]
            })
        
        # Language quality recommendations
        if scores.get("language_quality", 0) < 75:
            recommendations.append({
                "category": "language",
                "priority": "medium",
                "recommendation": "Enhance language quality and readability",
                "specific_actions": [
                    "Vary sentence length for better flow",
                    "Reduce passive voice usage",
                    "Simplify overly complex vocabulary where appropriate"
                ]
            })
        
        # SEO recommendations
        if scores.get("keyword_optimization", 0) < 75:
            recommendations.append({
                "category": "seo",
                "priority": "medium",
                "recommendation": "Improve keyword optimization and SEO elements",
                "specific_actions": [
                    "Better integrate primary keywords naturally",
                    "Ensure keywords appear in introduction and conclusion",
                    "Optimize keyword density to 1-2% for primary keywords"
                ]
            })
        
        # Audience alignment recommendations
        if scores.get("audience_alignment", 0) < 75:
            recommendations.append({
                "category": "audience",
                "priority": "high",
                "recommendation": "Better align content with target audience expectations",
                "specific_actions": [
                    "Use more audience-appropriate vocabulary",
                    "Adjust technical complexity to audience level",
                    "Include more relevant examples and use cases"
                ]
            })
        
        # Length recommendations
        if scores.get("length_appropriateness", 0) < 75:
            recommendations.append({
                "category": "length",
                "priority": "medium",
                "recommendation": "Adjust content length to meet target requirements",
                "specific_actions": [
                    "Expand thin sections with more detailed information",
                    "Remove redundant or off-topic content",
                    "Balance section lengths for better structure"
                ]
            })
        
        return recommendations

if __name__ == "__main__":
    # Test the enhanced agents part 2
    print("Enhanced Content Creation Agents Part 2 - Ready for Integration")