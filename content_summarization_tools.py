#!/usr/bin/env python3
"""
Content Summarization Tools using Gemini LLM
Enhanced source material analysis for autonomous content creation agents
"""

import os
import json
import time
from typing import Dict, List, Optional, Any
from datetime import datetime
import requests

class GeminiSummarizationTool:
    """Content summarization tool using Google Gemini LLM."""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
        self.model_name = "gemini-pro"
        
        if not self.api_key:
            print("Warning: GEMINI_API_KEY not found. Using mock summarization.")
            self.use_mock = True
        else:
            self.use_mock = False
    
    def summarize_content(self, content: str, summary_type: str = "general", max_length: int = 500) -> Dict[str, Any]:
        """
        Summarize content using Gemini LLM.
        
        Args:
            content: Source content to summarize
            summary_type: Type of summary (general, research, competitive, technical)
            max_length: Maximum length of summary in words
            
        Returns:
            Dictionary with summary and analysis
        """
        
        if self.use_mock:
            return self._mock_summarization(content, summary_type, max_length)
        
        try:
            # Create specialized prompt based on summary type
            prompt = self._create_summarization_prompt(content, summary_type, max_length)
            
            # Call Gemini API
            response = self._call_gemini_api(prompt)
            
            if response and "candidates" in response:
                summary_text = response["candidates"][0]["content"]["parts"][0]["text"]
                
                # Extract key insights using Gemini
                insights = self._extract_key_insights(content, summary_text)
                
                return {
                    "summary": summary_text,
                    "summary_type": summary_type,
                    "source_length": len(content.split()),
                    "summary_length": len(summary_text.split()),
                    "compression_ratio": len(content) / len(summary_text) if summary_text else 0,
                    "key_insights": insights,
                    "analysis_timestamp": datetime.now().isoformat(),
                    "model_used": self.model_name
                }
            else:
                return self._mock_summarization(content, summary_type, max_length)
                
        except Exception as e:
            print(f"Gemini summarization error: {e}")
            return self._mock_summarization(content, summary_type, max_length)
    
    def _create_summarization_prompt(self, content: str, summary_type: str, max_length: int) -> str:
        """Create specialized prompts for different summary types."""
        
        base_prompts = {
            "general": f"""
            Provide a comprehensive summary of the following content in approximately {max_length} words.
            Focus on the main points, key arguments, and important details.
            
            Content to summarize:
            {content}
            
            Summary:
            """,
            
            "research": f"""
            Analyze the following research content and provide a structured summary in approximately {max_length} words.
            Include: key findings, methodologies, data points, trends, and implications.
            
            Research content:
            {content}
            
            Research Summary:
            """,
            
            "competitive": f"""
            Analyze the following content for competitive intelligence in approximately {max_length} words.
            Focus on: competitor strategies, market positioning, strengths/weaknesses, opportunities, and threats.
            
            Content for competitive analysis:
            {content}
            
            Competitive Analysis Summary:
            """,
            
            "technical": f"""
            Provide a technical summary of the following content in approximately {max_length} words.
            Focus on: technical specifications, implementation details, architecture, performance, and technical implications.
            
            Technical content:
            {content}
            
            Technical Summary:
            """,
            
            "market": f"""
            Analyze the following market content and provide insights in approximately {max_length} words.
            Focus on: market trends, size, growth, opportunities, challenges, and key players.
            
            Market content:
            {content}
            
            Market Analysis Summary:
            """
        }
        
        return base_prompts.get(summary_type, base_prompts["general"])
    
    def _call_gemini_api(self, prompt: str) -> Optional[Dict]:
        """Make API call to Gemini."""
        
        headers = {
            "Content-Type": "application/json"
        }
        
        payload = {
            "contents": [{
                "parts": [{
                    "text": prompt
                }]
            }],
            "generationConfig": {
                "temperature": 0.3,
                "topK": 40,
                "topP": 0.95,
                "maxOutputTokens": 1024,
            },
            "safetySettings": [
                {
                    "category": "HARM_CATEGORY_HARASSMENT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                },
                {
                    "category": "HARM_CATEGORY_HATE_SPEECH", 
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                },
                {
                    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                },
                {
                    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                }
            ]
        }
        
        try:
            response = requests.post(
                f"{self.base_url}?key={self.api_key}",
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Gemini API error: {response.status_code} - {response.text}")
                return None
                
        except requests.RequestException as e:
            print(f"Gemini API request error: {e}")
            return None
    
    def _extract_key_insights(self, original_content: str, summary: str) -> List[str]:
        """Extract key insights from the summary using Gemini."""
        
        insights_prompt = f"""
        Based on the following summary, extract 3-5 key insights or actionable points:
        
        Summary: {summary}
        
        Please provide insights as a bulleted list focusing on the most important takeaways.
        """
        
        try:
            response = self._call_gemini_api(insights_prompt)
            if response and "candidates" in response:
                insights_text = response["candidates"][0]["content"]["parts"][0]["text"]
                # Parse insights into list
                insights = [line.strip() for line in insights_text.split('\n') if line.strip() and ('•' in line or '-' in line or line.startswith(('1.', '2.', '3.', '4.', '5.')))]
                return insights[:5]  # Limit to 5 insights
        except:
            pass
        
        # Fallback: extract basic insights
        return [
            "Key information identified in source material",
            "Important trends and patterns noted",
            "Relevant data points for content creation"
        ]
    
    def _mock_summarization(self, content: str, summary_type: str, max_length: int) -> Dict[str, Any]:
        """Provide mock summarization when Gemini API is not available."""
        
        words = content.split()
        source_length = len(words)
        
        # Create a basic extractive summary
        sentences = content.split('.')
        important_sentences = sentences[:min(3, len(sentences))]
        mock_summary = '. '.join(important_sentences).strip()
        
        if len(mock_summary.split()) > max_length:
            mock_summary = ' '.join(mock_summary.split()[:max_length])
        
        mock_insights = [
            f"Analysis of {summary_type} content reveals key information",
            "Important patterns and trends identified in source material",
            "Relevant data points extracted for content development",
            "Strategic insights derived from comprehensive analysis"
        ]
        
        return {
            "summary": mock_summary,
            "summary_type": summary_type,
            "source_length": source_length,
            "summary_length": len(mock_summary.split()),
            "compression_ratio": source_length / len(mock_summary.split()) if mock_summary else 1,
            "key_insights": mock_insights[:3],
            "analysis_timestamp": datetime.now().isoformat(),
            "model_used": "mock_summarizer"
        }

class AdvancedContentAnalyzer:
    """Advanced content analysis using multiple Gemini-powered tools."""
    
    def __init__(self, api_key: Optional[str] = None):
        self.summarizer = GeminiSummarizationTool(api_key)
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
    
    def comprehensive_analysis(self, content: str, analysis_focus: str = "content_creation") -> Dict[str, Any]:
        """
        Perform comprehensive content analysis for different purposes.
        
        Args:
            content: Source content to analyze
            analysis_focus: Focus area (content_creation, market_research, competitive_analysis)
        """
        
        analysis_results = {
            "analysis_focus": analysis_focus,
            "analysis_timestamp": datetime.now().isoformat(),
            "source_metadata": {
                "content_length": len(content),
                "word_count": len(content.split()),
                "estimated_reading_time": len(content.split()) // 200  # words per minute
            }
        }
        
        # Perform different types of summarization
        summary_types = self._get_summary_types_for_focus(analysis_focus)
        
        for summary_type in summary_types:
            analysis_results[f"{summary_type}_summary"] = self.summarizer.summarize_content(
                content, summary_type, max_length=300
            )
        
        # Extract content themes and topics
        analysis_results["content_themes"] = self._extract_themes(content)
        
        # Identify key entities and concepts
        analysis_results["key_entities"] = self._extract_key_entities(content)
        
        # Assess content quality and credibility
        analysis_results["quality_assessment"] = self._assess_content_quality(content)
        
        # Generate content creation recommendations
        analysis_results["recommendations"] = self._generate_recommendations(content, analysis_focus)
        
        return analysis_results
    
    def _get_summary_types_for_focus(self, analysis_focus: str) -> List[str]:
        """Get appropriate summary types based on analysis focus."""
        
        focus_mapping = {
            "content_creation": ["general", "research", "technical"],
            "market_research": ["market", "competitive", "research"],
            "competitive_analysis": ["competitive", "market", "technical"],
            "technical_analysis": ["technical", "research", "general"]
        }
        
        return focus_mapping.get(analysis_focus, ["general", "research"])
    
    def _extract_themes(self, content: str) -> List[str]:
        """Extract main themes from content using Gemini."""
        
        if not self.api_key:
            return ["Technology trends", "Business strategies", "Market dynamics"]
        
        themes_prompt = f"""
        Analyze the following content and identify the main themes and topics discussed.
        Provide 3-5 primary themes as a bulleted list.
        
        Content: {content[:1000]}...
        
        Main themes:
        """
        
        try:
            response = self.summarizer._call_gemini_api(themes_prompt)
            if response and "candidates" in response:
                themes_text = response["candidates"][0]["content"]["parts"][0]["text"]
                themes = [line.strip().replace('•', '').replace('-', '').strip() 
                         for line in themes_text.split('\n') if line.strip()]
                return themes[:5]
        except:
            pass
        
        return ["Primary content themes", "Key discussion topics", "Core subject areas"]
    
    def _extract_key_entities(self, content: str) -> List[str]:
        """Extract key entities (companies, people, technologies) from content."""
        
        if not self.api_key:
            return ["Key companies", "Industry leaders", "Technologies mentioned"]
        
        entities_prompt = f"""
        Extract key entities from the following content including:
        - Company names
        - Technology names
        - Industry terms
        - Important people/roles
        
        Content: {content[:1000]}...
        
        Key entities:
        """
        
        try:
            response = self.summarizer._call_gemini_api(entities_prompt)
            if response and "candidates" in response:
                entities_text = response["candidates"][0]["content"]["parts"][0]["text"]
                entities = [line.strip().replace('•', '').replace('-', '').strip() 
                           for line in entities_text.split('\n') if line.strip()]
                return entities[:10]
        except:
            pass
        
        return ["Industry entities", "Technology platforms", "Business organizations"]
    
    def _assess_content_quality(self, content: str) -> Dict[str, Any]:
        """Assess the quality and credibility of source content."""
        
        quality_metrics = {
            "content_depth": "high" if len(content.split()) > 500 else "medium",
            "technical_detail": "high" if any(term in content.lower() for term in ['implementation', 'architecture', 'framework', 'algorithm']) else "medium",
            "data_presence": "high" if any(char in content for char in ['%', '$', '€', '£']) else "low",
            "credibility_indicators": [],
            "content_freshness": "recent" if any(year in content for year in ['2024', '2023']) else "unknown"
        }
        
        # Check for credibility indicators
        credibility_indicators = [
            "research", "study", "analysis", "data", "survey", 
            "report", "findings", "statistics", "evidence"
        ]
        
        quality_metrics["credibility_indicators"] = [
            indicator for indicator in credibility_indicators 
            if indicator in content.lower()
        ]
        
        quality_metrics["overall_quality"] = self._calculate_overall_quality(quality_metrics)
        
        return quality_metrics
    
    def _calculate_overall_quality(self, metrics: Dict) -> str:
        """Calculate overall content quality score."""
        
        score = 0
        
        if metrics["content_depth"] == "high":
            score += 2
        elif metrics["content_depth"] == "medium":
            score += 1
        
        if metrics["technical_detail"] == "high":
            score += 2
        
        if metrics["data_presence"] == "high":
            score += 1
        
        if len(metrics["credibility_indicators"]) >= 3:
            score += 2
        elif len(metrics["credibility_indicators"]) >= 1:
            score += 1
        
        if score >= 6:
            return "excellent"
        elif score >= 4:
            return "good"
        elif score >= 2:
            return "fair"
        else:
            return "basic"
    
    def _generate_recommendations(self, content: str, analysis_focus: str) -> List[str]:
        """Generate recommendations based on content analysis."""
        
        if not self.api_key:
            return [
                "Leverage key insights for content development",
                "Focus on trending topics identified",
                "Incorporate data points and statistics",
                "Address identified market opportunities"
            ]
        
        recommendations_prompt = f"""
        Based on the analysis of the following content for {analysis_focus}, provide 4-5 specific recommendations for creating new content.
        
        Content summary: {content[:800]}...
        
        Recommendations for content creation:
        """
        
        try:
            response = self.summarizer._call_gemini_api(recommendations_prompt)
            if response and "candidates" in response:
                rec_text = response["candidates"][0]["content"]["parts"][0]["text"]
                recommendations = [line.strip().replace('•', '').replace('-', '').strip() 
                                 for line in rec_text.split('\n') if line.strip()]
                return recommendations[:5]
        except:
            pass
        
        return [
            f"Utilize insights for {analysis_focus}",
            "Incorporate trending themes identified",
            "Build upon key data points",
            "Address market gaps discovered"
        ]

class MultiSourceAnalyzer:
    """Analyze and summarize multiple sources for comprehensive research."""
    
    def __init__(self, api_key: Optional[str] = None):
        self.analyzer = AdvancedContentAnalyzer(api_key)
        self.summarizer = GeminiSummarizationTool(api_key)
    
    def analyze_multiple_sources(self, sources: List[Dict[str, str]], analysis_focus: str = "content_creation") -> Dict[str, Any]:
        """
        Analyze multiple content sources and create comprehensive summary.
        
        Args:
            sources: List of dictionaries with 'content' and 'source_type' keys
            analysis_focus: Focus for the analysis
        """
        
        multi_source_analysis = {
            "analysis_timestamp": datetime.now().isoformat(),
            "analysis_focus": analysis_focus,
            "total_sources": len(sources),
            "source_summaries": [],
            "comparative_analysis": {},
            "consolidated_insights": [],
            "recommendations": []
        }
        
        # Analyze each source individually
        for i, source in enumerate(sources):
            source_analysis = self.analyzer.comprehensive_analysis(
                source["content"], 
                analysis_focus
            )
            
            source_summary = {
                "source_id": i + 1,
                "source_type": source.get("source_type", "unknown"),
                "analysis": source_analysis
            }
            
            multi_source_analysis["source_summaries"].append(source_summary)
        
        # Perform comparative analysis
        multi_source_analysis["comparative_analysis"] = self._compare_sources(
            multi_source_analysis["source_summaries"]
        )
        
        # Consolidate insights from all sources
        multi_source_analysis["consolidated_insights"] = self._consolidate_insights(
            multi_source_analysis["source_summaries"]
        )
        
        # Generate comprehensive recommendations
        multi_source_analysis["recommendations"] = self._generate_multi_source_recommendations(
            multi_source_analysis["source_summaries"], 
            analysis_focus
        )
        
        return multi_source_analysis
    
    def _compare_sources(self, source_summaries: List[Dict]) -> Dict[str, Any]:
        """Compare multiple sources to identify patterns and differences."""
        
        comparison = {
            "common_themes": [],
            "unique_insights": [],
            "quality_comparison": {},
            "content_gaps": []
        }
        
        # Extract themes from all sources
        all_themes = []
        for summary in source_summaries:
            themes = summary["analysis"].get("content_themes", [])
            all_themes.extend(themes)
        
        # Find common themes
        theme_counts = {}
        for theme in all_themes:
            theme_counts[theme] = theme_counts.get(theme, 0) + 1
        
        comparison["common_themes"] = [
            theme for theme, count in theme_counts.items() 
            if count > 1
        ]
        
        # Quality comparison
        for summary in source_summaries:
            source_id = summary["source_id"]
            quality = summary["analysis"]["quality_assessment"]["overall_quality"]
            comparison["quality_comparison"][f"source_{source_id}"] = quality
        
        return comparison
    
    def _consolidate_insights(self, source_summaries: List[Dict]) -> List[str]:
        """Consolidate insights from multiple sources."""
        
        all_insights = []
        
        for summary in source_summaries:
            # Get insights from different summary types
            for key, value in summary["analysis"].items():
                if key.endswith("_summary") and isinstance(value, dict):
                    insights = value.get("key_insights", [])
                    all_insights.extend(insights)
        
        # Remove duplicates and return top insights
        unique_insights = list(set(all_insights))
        return unique_insights[:8]  # Return top 8 consolidated insights
    
    def _generate_multi_source_recommendations(self, source_summaries: List[Dict], analysis_focus: str) -> List[str]:
        """Generate recommendations based on multi-source analysis."""
        
        recommendations = [
            f"Synthesize insights from {len(source_summaries)} sources for comprehensive {analysis_focus}",
            "Leverage common themes identified across multiple sources",
            "Address content gaps discovered in comparative analysis",
            "Incorporate diverse perspectives from various source types",
            "Build content strategy on validated insights from multiple sources"
        ]
        
        return recommendations

# Example usage and testing
def test_summarization_tools():
    """Test the summarization tools with sample content."""
    
    sample_content = """
    Artificial Intelligence (AI) automation is revolutionizing business operations across industries. 
    Companies are implementing AI-powered solutions to streamline workflows, reduce manual tasks, 
    and improve efficiency. Recent studies show that businesses using AI automation see an average 
    of 30% improvement in operational efficiency and 25% reduction in costs. Key areas where AI 
    automation is making impact include customer service chatbots, predictive analytics, 
    supply chain optimization, and automated content generation. However, implementation challenges 
    include data quality issues, integration complexity, and the need for employee training. 
    Successful AI automation requires clear strategy, proper change management, and continuous 
    monitoring of performance metrics.
    """
    
    print("Testing Gemini Content Summarization Tools")
    print("=" * 50)
    
    # Test basic summarization
    summarizer = GeminiSummarizationTool()
    
    print("\n1. Basic Summarization:")
    general_summary = summarizer.summarize_content(sample_content, "general", 150)
    print(f"Summary: {general_summary['summary']}")
    print(f"Compression Ratio: {general_summary['compression_ratio']:.2f}")
    
    print("\n2. Research Summarization:")
    research_summary = summarizer.summarize_content(sample_content, "research", 150)
    print(f"Research Summary: {research_summary['summary']}")
    print(f"Key Insights: {research_summary['key_insights']}")
    
    # Test advanced analysis
    print("\n3. Advanced Content Analysis:")
    analyzer = AdvancedContentAnalyzer()
    analysis = analyzer.comprehensive_analysis(sample_content, "content_creation")
    print(f"Content Themes: {analysis['content_themes']}")
    print(f"Quality Assessment: {analysis['quality_assessment']['overall_quality']}")
    print(f"Recommendations: {analysis['recommendations'][:2]}")
    
    print("\n✅ Summarization tools test completed!")

if __name__ == "__main__":
    test_summarization_tools()