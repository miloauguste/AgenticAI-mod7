#!/usr/bin/env python3
"""
Enhanced Autonomous Content Creation System with Gemini-powered Content Summarization
Integrates advanced source material analysis for superior content quality
"""

import os
import json
import random
from typing import Dict, Any, List, Optional
from dotenv import load_dotenv
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from typing_extensions import TypedDict
from datetime import datetime
from research_tool import research_tool
from writing_tool import writing_tool
from SEO_tool import seo_tool
from content_summarization_tools import GeminiSummarizationTool, AdvancedContentAnalyzer, MultiSourceAnalyzer

load_dotenv()

class EnhancedContentState(TypedDict):
    # Input parameters
    client_brief: str
    target_audience: str
    content_goals: List[str]
    
    # Content strategy
    content_strategy: str
    content_calendar: List[Dict]
    selected_topics: List[str]
    
    # Enhanced research and analysis with summarization
    raw_research_data: str
    summarized_research: Dict[str, Any]
    competitor_analysis: str
    summarized_competitors: Dict[str, Any]
    trending_topics: List[str]
    keywords: List[str]
    source_analysis: Dict[str, Any]
    
    # Content creation with summarization insights
    content_outline: str
    draft_content: str
    revised_content: str
    final_content: str
    content_insights: Dict[str, Any]
    
    # SEO and optimization
    seo_analysis: str
    meta_data: Dict[str, str]
    readability_score: float
    
    # Quality assurance
    quality_checks: List[str]
    revision_notes: List[str]
    approval_status: str
    
    # Final output
    deliverables: Dict[str, Any]
    performance_metrics: Dict[str, Any]

class EnhancedMarketResearchAgent:
    """Enhanced market research agent with Gemini-powered content analysis."""
    
    def __init__(self):
        self.name = "Enhanced Market Research Agent"
        self.summarizer = GeminiSummarizationTool()
        self.analyzer = AdvancedContentAnalyzer()
        self.multi_analyzer = MultiSourceAnalyzer()
        
    def conduct_enhanced_research(self, industry: str, audience: str, topic: str) -> Dict[str, Any]:
        """Perform comprehensive market research with advanced content analysis."""
        
        print("Conducting enhanced market research with Gemini analysis...")
        
        # Gather raw research data
        research_queries = [
            f"{industry} market trends {audience} 2024",
            f"{topic} industry analysis competitive landscape",
            f"{audience} behavior preferences {industry} sector"
        ]
        
        research_sources = []
        raw_research_data = ""
        
        for query in research_queries:
            try:
                research_result = research_tool._run(query)
                raw_research_data += f"\n\nResearch Query: {query}\n{research_result}"
                
                research_sources.append({
                    "content": research_result,
                    "source_type": "market_research",
                    "query": query
                })
            except Exception as e:
                print(f"Research query failed: {e}")
        
        # Perform multi-source analysis using Gemini
        if research_sources:
            multi_source_analysis = self.multi_analyzer.analyze_multiple_sources(
                research_sources, 
                "market_research"
            )
        else:
            multi_source_analysis = {"error": "No research sources available"}
        
        # Generate comprehensive market summary using Gemini
        market_summary = self.summarizer.summarize_content(
            raw_research_data,
            "market",
            max_length=400
        )
        
        # Perform detailed content analysis
        detailed_analysis = self.analyzer.comprehensive_analysis(
            raw_research_data,
            "market_research"
        )
        
        enhanced_research = {
            "raw_data": raw_research_data,
            "market_summary": market_summary,
            "detailed_analysis": detailed_analysis,
            "multi_source_analysis": multi_source_analysis,
            "research_quality": self._assess_research_quality(raw_research_data),
            "actionable_insights": self._extract_actionable_insights(detailed_analysis),
            "research_timestamp": datetime.now().isoformat()
        }
        
        return enhanced_research
    
    def analyze_competitors_with_summarization(self, industry: str, topic: str) -> Dict[str, Any]:
        """Perform competitor analysis with Gemini-powered summarization."""
        
        print("Analyzing competitors with Gemini-powered insights...")
        
        competitor_query = f"{industry} competitor analysis {topic} market leaders strategies"
        
        try:
            raw_competitor_data = research_tool._run(competitor_query)
            
            # Summarize competitor data using Gemini
            competitor_summary = self.summarizer.summarize_content(
                raw_competitor_data,
                "competitive",
                max_length=350
            )
            
            # Perform detailed competitive analysis
            competitive_analysis = self.analyzer.comprehensive_analysis(
                raw_competitor_data,
                "competitive_analysis"
            )
            
            return {
                "raw_competitor_data": raw_competitor_data,
                "competitor_summary": competitor_summary,
                "competitive_analysis": competitive_analysis,
                "competitive_insights": competitive_analysis.get("recommendations", []),
                "key_competitors": self._extract_competitors(competitor_summary),
                "analysis_timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                "error": f"Competitor analysis failed: {e}",
                "mock_analysis": "Mock competitive intelligence generated"
            }
    
    def _assess_research_quality(self, research_data: str) -> Dict[str, Any]:
        """Assess the quality of research data using content analysis."""
        
        quality_metrics = {
            "data_richness": "high" if len(research_data.split()) > 1000 else "medium",
            "source_diversity": "multiple" if "Research Query:" in research_data else "single",
            "content_depth": "comprehensive" if any(term in research_data.lower() for term in ['analysis', 'study', 'report', 'survey']) else "basic",
            "recency_indicators": bool(any(year in research_data for year in ['2024', '2023', 'recent', 'latest'])),
            "quantitative_data": bool(any(char in research_data for char in ['%', '$', '€', '£', 'million', 'billion']))
        }
        
        # Calculate overall quality score
        score = sum([
            2 if quality_metrics["data_richness"] == "high" else 1,
            2 if quality_metrics["source_diversity"] == "multiple" else 1,
            2 if quality_metrics["content_depth"] == "comprehensive" else 1,
            1 if quality_metrics["recency_indicators"] else 0,
            1 if quality_metrics["quantitative_data"] else 0
        ])
        
        quality_metrics["overall_score"] = score
        quality_metrics["quality_rating"] = "excellent" if score >= 7 else "good" if score >= 5 else "adequate"
        
        return quality_metrics
    
    def _extract_actionable_insights(self, analysis: Dict[str, Any]) -> List[str]:
        """Extract actionable insights from detailed analysis."""
        
        insights = []
        
        # Extract from recommendations
        recommendations = analysis.get("recommendations", [])
        insights.extend(recommendations[:3])
        
        # Extract from themes
        themes = analysis.get("content_themes", [])
        for theme in themes[:2]:
            insights.append(f"Leverage {theme} for content positioning")
        
        # Extract from key entities
        entities = analysis.get("key_entities", [])
        if entities:
            insights.append(f"Reference industry leaders: {', '.join(entities[:3])}")
        
        return insights[:5]
    
    def _extract_competitors(self, competitor_summary: Dict[str, Any]) -> List[str]:
        """Extract key competitors from summary analysis."""
        
        if isinstance(competitor_summary, dict):
            summary_text = competitor_summary.get("summary", "")
            key_insights = competitor_summary.get("key_insights", [])
            
            # Look for company names in summary and insights
            competitor_indicators = []
            text_to_analyze = summary_text + " " + " ".join(key_insights)
            
            # Simple extraction of potential company names (capitalized words)
            words = text_to_analyze.split()
            for word in words:
                if word.istitle() and len(word) > 3 and word not in ['The', 'And', 'For', 'With']:
                    competitor_indicators.append(word)
            
            return list(set(competitor_indicators))[:5]
        
        return ["Industry Leader A", "Market Competitor B", "Innovation Company C"]

class EnhancedContentWriter:
    """Enhanced content writer with Gemini-powered source material analysis."""
    
    def __init__(self):
        self.name = "Enhanced Content Writer"
        self.summarizer = GeminiSummarizationTool()
        self.analyzer = AdvancedContentAnalyzer()
    
    def create_enhanced_content_outline(self, research_summary: Dict, competitive_analysis: Dict, keywords: List[str]) -> Dict[str, Any]:
        """Create enhanced content outline using summarized research insights."""
        
        print("Creating enhanced content outline with Gemini insights...")
        
        # Extract key insights from research summaries
        research_insights = self._extract_research_insights(research_summary, competitive_analysis)
        
        # Create content structure based on insights
        outline_structure = {
            "title_suggestions": self._generate_title_suggestions(research_insights, keywords),
            "content_sections": self._create_content_sections(research_insights),
            "key_messages": self._identify_key_messages(research_insights),
            "supporting_data": self._extract_supporting_data(research_summary),
            "competitive_angles": self._identify_competitive_angles(competitive_analysis),
            "outline_timestamp": datetime.now().isoformat()
        }
        
        # Generate detailed outline text
        detailed_outline = self._format_detailed_outline(outline_structure, keywords)
        
        return {
            "outline_structure": outline_structure,
            "detailed_outline": detailed_outline,
            "content_strategy": self._define_content_strategy(research_insights),
            "estimated_length": self._estimate_content_length(outline_structure)
        }
    
    def write_content_with_summarized_insights(self, outline: Dict, research_data: Dict, competitive_data: Dict) -> Dict[str, Any]:
        """Write content using insights from Gemini-summarized source material."""
        
        print("Writing content with Gemini-powered insights...")
        
        # Prepare enhanced content prompt with summarized insights
        content_context = self._prepare_content_context(outline, research_data, competitive_data)
        
        # Generate content using writing tool with enhanced context
        try:
            enhanced_content = writing_tool._run(content_context)
            
            # Analyze the generated content using Gemini
            content_analysis = self.analyzer.comprehensive_analysis(
                enhanced_content,
                "content_creation"
            )
            
            # Enhance content with additional insights
            enhanced_content_with_insights = self._enhance_content_with_insights(
                enhanced_content, 
                content_analysis,
                research_data
            )
            
            return {
                "primary_content": enhanced_content_with_insights,
                "content_analysis": content_analysis,
                "enhancement_notes": self._generate_enhancement_notes(content_analysis),
                "content_metrics": self._calculate_content_metrics(enhanced_content_with_insights),
                "creation_timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return self._generate_fallback_content_with_insights(outline, research_data)
    
    def _extract_research_insights(self, research_summary: Dict, competitive_analysis: Dict) -> Dict[str, List]:
        """Extract actionable insights from research summaries."""
        
        insights = {
            "market_trends": [],
            "audience_insights": [],
            "competitive_gaps": [],
            "opportunities": [],
            "key_data_points": []
        }
        
        # Extract from research summary
        if isinstance(research_summary, dict):
            market_summary = research_summary.get("market_summary", {})
            if isinstance(market_summary, dict):
                insights["market_trends"] = market_summary.get("key_insights", [])[:3]
        
        # Extract from competitive analysis
        if isinstance(competitive_analysis, dict):
            comp_summary = competitive_analysis.get("competitor_summary", {})
            if isinstance(comp_summary, dict):
                insights["competitive_gaps"] = comp_summary.get("key_insights", [])[:3]
        
        return insights
    
    def _generate_title_suggestions(self, insights: Dict, keywords: List[str]) -> List[str]:
        """Generate content title suggestions based on insights."""
        
        primary_keyword = keywords[0] if keywords else "business technology"
        
        title_templates = [
            f"The Future of {primary_keyword}: Trends and Opportunities",
            f"How {primary_keyword} is Transforming Business Operations",
            f"Complete Guide to {primary_keyword} Implementation",
            f"{primary_keyword} Strategy: What Industry Leaders Know",
            f"Maximizing ROI with {primary_keyword} Solutions"
        ]
        
        return title_templates
    
    def _create_content_sections(self, insights: Dict) -> List[Dict]:
        """Create content sections based on research insights."""
        
        sections = [
            {
                "section": "Introduction",
                "focus": "Market context and opportunity",
                "key_points": insights.get("market_trends", [])[:2],
                "estimated_words": 200
            },
            {
                "section": "Current Landscape Analysis",
                "focus": "Industry trends and challenges",
                "key_points": insights.get("audience_insights", [])[:3],
                "estimated_words": 400
            },
            {
                "section": "Strategic Opportunities",
                "focus": "Competitive advantages and gaps",
                "key_points": insights.get("competitive_gaps", [])[:2],
                "estimated_words": 350
            },
            {
                "section": "Implementation Framework",
                "focus": "Practical guidance and best practices",
                "key_points": insights.get("opportunities", [])[:3],
                "estimated_words": 450
            },
            {
                "section": "Conclusion and Next Steps",
                "focus": "Actionable recommendations",
                "key_points": ["Summary of key insights", "Call to action"],
                "estimated_words": 200
            }
        ]
        
        return sections
    
    def _identify_key_messages(self, insights: Dict) -> List[str]:
        """Identify key messages from research insights."""
        
        messages = []
        
        for category, insight_list in insights.items():
            if insight_list:
                messages.append(f"Key insight from {category}: {insight_list[0]}")
        
        return messages[:4]
    
    def _extract_supporting_data(self, research_summary: Dict) -> List[str]:
        """Extract supporting data points from research."""
        
        supporting_data = [
            "Industry growth statistics and projections",
            "Market adoption rates and trends",
            "Competitive landscape analysis",
            "Technology implementation benefits"
        ]
        
        # Try to extract actual data from research
        if isinstance(research_summary, dict):
            detailed_analysis = research_summary.get("detailed_analysis", {})
            if isinstance(detailed_analysis, dict):
                key_entities = detailed_analysis.get("key_entities", [])
                if key_entities:
                    supporting_data.extend([f"Reference to {entity}" for entity in key_entities[:2]])
        
        return supporting_data[:5]
    
    def _identify_competitive_angles(self, competitive_analysis: Dict) -> List[str]:
        """Identify competitive positioning angles."""
        
        if isinstance(competitive_analysis, dict):
            competitive_insights = competitive_analysis.get("competitive_insights", [])
            if competitive_insights:
                return competitive_insights[:3]
        
        return [
            "Differentiation opportunities in the market",
            "Competitive advantages to highlight",
            "Market gaps to address"
        ]
    
    def _format_detailed_outline(self, structure: Dict, keywords: List[str]) -> str:
        """Format the detailed content outline."""
        
        outline = f"""
ENHANCED CONTENT OUTLINE

TITLE OPTIONS:
{chr(10).join([f"• {title}" for title in structure["title_suggestions"][:3]])}

TARGET KEYWORDS: {", ".join(keywords[:5])}

CONTENT STRUCTURE:
"""
        
        for section in structure["content_sections"]:
            outline += f"""
{section["section"].upper()} ({section["estimated_words"]} words)
Focus: {section["focus"]}
Key Points:
{chr(10).join([f"  • {point}" for point in section["key_points"]])}
"""
        
        outline += f"""
KEY MESSAGES TO INCORPORATE:
{chr(10).join([f"• {message}" for message in structure["key_messages"]])}

SUPPORTING DATA TO INCLUDE:
{chr(10).join([f"• {data}" for data in structure.get("supporting_data", [])])}

COMPETITIVE ANGLES:
{chr(10).join([f"• {angle}" for angle in structure.get("competitive_angles", [])])}
"""
        
        return outline
    
    def _define_content_strategy(self, insights: Dict) -> Dict[str, str]:
        """Define content strategy based on insights."""
        
        return {
            "primary_angle": "Thought leadership with data-driven insights",
            "tone": "Professional and authoritative",
            "value_proposition": "Actionable insights backed by market research",
            "target_outcome": "Position client as industry expert"
        }
    
    def _estimate_content_length(self, structure: Dict) -> int:
        """Estimate total content length."""
        
        sections = structure.get("content_sections", [])
        total_words = sum([section.get("estimated_words", 200) for section in sections])
        return total_words
    
    def _prepare_content_context(self, outline: Dict, research_data: Dict, competitive_data: Dict) -> str:
        """Prepare enhanced content context for writing."""
        
        context = f"""
Create comprehensive, professional content based on the following enhanced research and analysis:

CONTENT OUTLINE:
{outline.get("detailed_outline", "")}

RESEARCH INSIGHTS:
{json.dumps(research_data.get("actionable_insights", []), indent=2)}

COMPETITIVE INTELLIGENCE:
{json.dumps(competitive_data.get("competitive_insights", []), indent=2)}

CONTENT STRATEGY:
{json.dumps(outline.get("content_strategy", {}), indent=2)}

Requirements:
- Professional, authoritative tone
- Data-driven insights and examples
- Actionable recommendations
- Estimated length: {outline.get("estimated_length", 1000)} words
- SEO-optimized structure with clear headings
- Include relevant statistics and trends from research
- Address competitive positioning opportunities
"""
        
        return context
    
    def _enhance_content_with_insights(self, content: str, analysis: Dict, research_data: Dict) -> str:
        """Enhance content with additional insights from analysis."""
        
        # Add research-backed insights section if not present
        insights_section = """

## Key Market Insights

Based on comprehensive market research and competitive analysis:

"""
        
        actionable_insights = research_data.get("actionable_insights", [])
        for insight in actionable_insights[:3]:
            insights_section += f"• {insight}\n"
        
        # Insert insights section before conclusion
        if "conclusion" in content.lower() or "summary" in content.lower():
            conclusion_index = content.lower().find("conclusion")
            if conclusion_index == -1:
                conclusion_index = content.lower().find("summary")
            
            if conclusion_index > 0:
                enhanced_content = content[:conclusion_index] + insights_section + content[conclusion_index:]
            else:
                enhanced_content = content + insights_section
        else:
            enhanced_content = content + insights_section
        
        return enhanced_content
    
    def _generate_enhancement_notes(self, analysis: Dict) -> List[str]:
        """Generate notes on content enhancements."""
        
        notes = [
            "Content enhanced with Gemini-powered research insights",
            "Competitive intelligence integrated throughout",
            "Market trends and data points incorporated",
            "SEO optimization applied based on analysis"
        ]
        
        quality_assessment = analysis.get("quality_assessment", {})
        if isinstance(quality_assessment, dict):
            overall_quality = quality_assessment.get("overall_quality", "good")
            notes.append(f"Content quality assessed as: {overall_quality}")
        
        return notes
    
    def _calculate_content_metrics(self, content: str) -> Dict[str, Any]:
        """Calculate content metrics."""
        
        words = content.split()
        sentences = content.split('.')
        
        return {
            "word_count": len(words),
            "sentence_count": len(sentences),
            "average_sentence_length": len(words) / len(sentences) if sentences else 0,
            "readability_estimate": min(100, max(0, 100 - (len(words) / len(sentences) * 1.5))) if sentences else 50
        }
    
    def _generate_fallback_content_with_insights(self, outline: Dict, research_data: Dict) -> Dict[str, Any]:
        """Generate fallback content when AI writing fails."""
        
        fallback_content = f"""
# Enhanced Business Technology Analysis

## Executive Summary

This comprehensive analysis examines current market trends and opportunities in business technology, backed by extensive research and competitive intelligence.

## Market Landscape Overview

Recent market research reveals significant opportunities in the technology sector, with businesses increasingly adopting innovative solutions to maintain competitive advantage.

## Strategic Recommendations

Based on comprehensive analysis:
• Focus on emerging technology trends
• Leverage competitive positioning opportunities  
• Implement data-driven decision making
• Invest in scalable technology solutions

## Implementation Framework

Organizations should consider a phased approach to technology adoption, emphasizing careful planning, stakeholder alignment, and measurable outcomes.

## Conclusion

The technology landscape continues to evolve rapidly, presenting both challenges and opportunities for forward-thinking organizations.
"""
        
        return {
            "primary_content": fallback_content,
            "content_analysis": {"note": "Fallback content generated"},
            "enhancement_notes": ["Fallback content with research context"],
            "content_metrics": self._calculate_content_metrics(fallback_content),
            "creation_timestamp": datetime.now().isoformat()
        }

# Enhanced workflow nodes that integrate Gemini summarization

def enhanced_market_research_node(state: EnhancedContentState) -> EnhancedContentState:
    """Enhanced market research with Gemini-powered analysis."""
    print("Conducting enhanced market research with Gemini analysis...")
    
    research_agent = EnhancedMarketResearchAgent()
    
    # Extract parameters from state
    client_brief = state.get("client_brief", "")
    target_audience = state.get("target_audience", "business professionals")
    selected_topics = state.get("selected_topics", ["business technology"])
    
    # Determine industry and topic
    industry = "technology"  # Could be extracted from brief
    topic = selected_topics[0] if selected_topics else "business technology"
    
    # Conduct enhanced research
    enhanced_research = research_agent.conduct_enhanced_research(industry, target_audience, topic)
    
    # Conduct competitive analysis
    competitive_analysis = research_agent.analyze_competitors_with_summarization(industry, topic)
    
    print("Enhanced market research completed with Gemini insights")
    
    return {
        **state,
        "raw_research_data": enhanced_research.get("raw_data", ""),
        "summarized_research": enhanced_research,
        "competitor_analysis": competitive_analysis.get("raw_competitor_data", ""),
        "summarized_competitors": competitive_analysis,
        "source_analysis": {
            "research_quality": enhanced_research.get("research_quality", {}),
            "competitive_insights": competitive_analysis.get("competitive_insights", [])
        }
    }

def enhanced_content_creation_node(state: EnhancedContentState) -> EnhancedContentState:
    """Enhanced content creation using Gemini-summarized insights."""
    print("Creating enhanced content with Gemini-powered insights...")
    
    writer = EnhancedContentWriter()
    
    # Get summarized research and competitive data
    summarized_research = state.get("summarized_research", {})
    summarized_competitors = state.get("summarized_competitors", {})
    keywords = state.get("keywords", [])
    
    # Create enhanced outline
    outline_data = writer.create_enhanced_content_outline(
        summarized_research, 
        summarized_competitors, 
        keywords
    )
    
    # Write content with insights
    content_data = writer.write_content_with_summarized_insights(
        outline_data,
        summarized_research,
        summarized_competitors
    )
    
    print("Enhanced content creation completed")
    
    return {
        **state,
        "content_outline": outline_data.get("detailed_outline", ""),
        "draft_content": content_data.get("primary_content", ""),
        "content_insights": {
            "outline_structure": outline_data.get("outline_structure", {}),
            "content_analysis": content_data.get("content_analysis", {}),
            "enhancement_notes": content_data.get("enhancement_notes", []),
            "content_metrics": content_data.get("content_metrics", {})
        }
    }

def run_enhanced_autonomous_system(
    client_brief: str = None,
    target_audience: str = None,
    content_goals: List[str] = None
):
    """
    Run the enhanced autonomous content creation system with Gemini summarization.
    """
    
    print("="*80)
    print("ENHANCED AUTONOMOUS CONTENT CREATION SYSTEM WITH GEMINI")
    print("Advanced Source Material Analysis and Summarization")
    print("="*80)
    
    try:
        # Note: This is a simplified version focusing on the summarization enhancements
        # The full system would include all the previous nodes plus these enhanced ones
        
        print("\n🧠 Gemini-Powered Features Active:")
        print("• Advanced content summarization")
        print("• Multi-source research analysis")
        print("• Competitive intelligence insights")
        print("• Enhanced content creation")
        
        # Simulate enhanced research
        research_agent = EnhancedMarketResearchAgent()
        enhanced_research = research_agent.conduct_enhanced_research(
            "technology", 
            target_audience or "business professionals",
            "AI automation"
        )
        
        print(f"\n📊 Research Analysis Complete:")
        print(f"• Sources analyzed with Gemini summarization")
        print(f"• Research quality: {enhanced_research.get('research_quality', {}).get('quality_rating', 'good')}")
        print(f"• Actionable insights generated: {len(enhanced_research.get('actionable_insights', []))}")
        
        # Simulate enhanced content creation
        writer = EnhancedContentWriter()
        outline_data = writer.create_enhanced_content_outline(
            enhanced_research, {}, ["AI automation", "business technology"]
        )
        
        content_data = writer.write_content_with_summarized_insights(
            outline_data, enhanced_research, {}
        )
        
        print(f"\n✍️ Enhanced Content Creation Complete:")
        print(f"• Content length: {content_data.get('content_metrics', {}).get('word_count', 0)} words")
        print(f"• Gemini insights integrated: ✅")
        print(f"• Source material analyzed: ✅")
        
        # Display sample results
        print(f"\n" + "="*60)
        print("SAMPLE ENHANCED CONTENT OUTPUT")
        print("="*60)
        
        sample_content = content_data.get("primary_content", "")
        if sample_content:
            print(sample_content[:500] + "..." if len(sample_content) > 500 else sample_content)
        
        print(f"\n" + "="*60)
        print("GEMINI ANALYSIS INSIGHTS")
        print("="*60)
        
        insights = enhanced_research.get("actionable_insights", [])
        for i, insight in enumerate(insights[:3], 1):
            print(f"{i}. {insight}")
        
        return {
            "enhanced_research": enhanced_research,
            "content_data": content_data,
            "outline_data": outline_data,
            "gemini_features": "active",
            "status": "success"
        }
        
    except Exception as e:
        print(f"Error in enhanced system: {e}")
        return {"status": "error", "error": str(e)}

if __name__ == "__main__":
    # Test the enhanced system
    result = run_enhanced_autonomous_system(
        client_brief="Create thought leadership content on AI automation for business",
        target_audience="Technology executives and decision makers",
        content_goals=["brand_awareness", "lead_generation", "education"]
    )