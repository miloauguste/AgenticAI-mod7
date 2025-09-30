import os
import openai
from claude_content_generator import ClaudeContentGenerator
from typing import Dict, Any, Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class ContentGeneratorTool:
    def __init__(self, openai_api_key=None, claude_api_key=None, preferred_model="openai"):
        self.name = "Enhanced Content Generator Tool"
        self.description = "A tool for generating high-quality written content using OpenAI GPT or Claude AI."
        self.preferred_model = preferred_model
        
        # OpenAI setup
        if openai_api_key:
            openai.api_key = openai_api_key
            self._has_openai_key = True
        else:
            self._has_openai_key = False
        
        # Claude setup
        self.claude_generator = ClaudeContentGenerator(claude_api_key)
        self._has_claude_key = not self.claude_generator.use_mock

    def _run(self, research_data: str) -> str:
        """Generate content using the preferred AI model."""
        try:
            # Try Claude first if preferred or if OpenAI is not available
            if self.preferred_model == "claude" or not self._has_openai_key:
                return self._generate_with_claude(research_data)
            # Otherwise use OpenAI
            else:
                return self._generate_with_openai(research_data)
        except Exception as e:
            return self._generate_fallback_content(research_data, str(e))
    
    def _generate_with_claude(self, research_data: str) -> str:
        """Generate content using Claude AI."""
        try:
            # Parse research data to extract content requirements
            content_requirements = self._parse_research_to_requirements(research_data)
            
            # Generate content with Claude
            result = self.claude_generator.generate_content(content_requirements)
            
            if result and "content" in result:
                return result["content"]
            else:
                # Fallback to OpenAI if Claude fails
                if self._has_openai_key:
                    return self._generate_with_openai(research_data)
                else:
                    return self._generate_fallback_content(research_data, "Claude generation failed")
                    
        except Exception as e:
            # Fallback to OpenAI if Claude fails
            if self._has_openai_key:
                return self._generate_with_openai(research_data)
            else:
                return self._generate_fallback_content(research_data, str(e))
    
    def _generate_with_openai(self, research_data: str) -> str:
        """Generate content using OpenAI GPT."""
        try:
            if not self._has_openai_key:
                return self._generate_fallback_content(research_data, "No OpenAI API key")

            # Add uniqueness factors
            import random
            import datetime
            
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            perspectives = [
                "industry expert", "business analyst", "technology consultant", 
                "innovation strategist", "market researcher", "thought leader"
            ]
            writing_styles = [
                "analytical and data-driven", "engaging and conversational", 
                "authoritative and comprehensive", "practical and actionable",
                "forward-thinking and innovative", "strategic and insightful"
            ]
            
            selected_perspective = random.choice(perspectives)
            selected_style = random.choice(writing_styles)
            
            prompt = f"""
            You are a {selected_perspective} writing content in a {selected_style} style. 
            
            Create a unique, comprehensive article based on this research data:
            {research_data}
            
            Important: Make this content UNIQUE and specific. Include:
            - A compelling headline that reflects current trends (generated at {current_time})
            - An engaging introduction with fresh perspective
            - 3-4 main sections with detailed analysis
            - Specific insights and actionable recommendations
            - Current market context and future outlook
            - A strong conclusion with clear next steps
            
            Writing guidelines:
            - Tone: {selected_style}
            - Perspective: {selected_perspective}
            - Length: 900-1200 words
            - Include specific examples and data points where possible
            - Make it unique - avoid generic statements
            - Focus on practical value and fresh insights
            """

            completion = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1500,
                temperature=0.8  # Increased for more creativity
            )

            return completion.choices[0].message.content
        except Exception as e:
            return self._generate_fallback_content(research_data, str(e))
    
    def _parse_research_to_requirements(self, research_data: str) -> Dict[str, Any]:
        """Parse research data into content requirements for Claude."""
        
        # Extract topic from research data
        lines = research_data.split('\n')
        topic = "business technology"
        
        for line in lines[:5]:
            if line.strip() and len(line.strip()) > 10:
                topic = line.strip()[:100]
                break
        
        # Determine content type based on research data
        content_type = "blog_post"
        if "analysis" in research_data.lower():
            content_type = "analysis_report"
        elif "whitepaper" in research_data.lower():
            content_type = "whitepaper"
        elif "case study" in research_data.lower():
            content_type = "case_study"
        
        # Extract keywords from research data
        common_business_terms = [
            "technology", "business", "strategy", "innovation", "digital", 
            "transformation", "automation", "AI", "efficiency", "growth"
        ]
        
        keywords = []
        research_lower = research_data.lower()
        for term in common_business_terms:
            if term in research_lower:
                keywords.append(term)
        
        # Default keywords if none found
        if not keywords:
            keywords = ["business", "technology", "innovation"]
        
        return {
            "content_type": content_type,
            "topic": topic,
            "target_audience": "business professionals",
            "tone": "professional",
            "word_count": 1000,
            "keywords": keywords[:5],
            "research_insights": self._extract_insights_from_research(research_data),
            "content_goals": ["education", "engagement", "thought_leadership"],
            "brand_guidelines": {
                "tone": "professional and authoritative",
                "voice": "knowledgeable expert"
            }
        }
    
    def _extract_insights_from_research(self, research_data: str) -> list:
        """Extract key insights from research data."""
        insights = []
        
        # Look for sentences with data points
        sentences = research_data.split('.')
        for sentence in sentences:
            if any(indicator in sentence for indicator in ['%', '$', 'study', 'research', 'analysis']):
                insights.append(sentence.strip())
        
        # If no specific insights found, create generic ones
        if not insights:
            insights = [
                "Market research indicates growing demand",
                "Industry analysis shows positive trends",
                "Data suggests significant opportunities"
            ]
        
        return insights[:3]
    
    def _generate_fallback_content(self, research_data: str, error_msg: str) -> str:
        """Generate enhanced fallback content when AI services fail."""
        import random
        import datetime
        
        current_time = datetime.datetime.now().strftime("%B %d, %Y")
        session_id = str(random.randint(1000, 9999))
        
        # Extract topic from research data
        topic = "business technology"
        if research_data:
            lines = research_data.split('\n')
            for line in lines[:3]:
                if line.strip() and len(line.strip()) > 10:
                    topic = line.strip()[:50]
                    break
        
        # Randomized content templates
        insights = random.choice([
            ["Market dynamics continue to evolve rapidly", "Technology adoption rates are accelerating", "Strategic positioning becomes increasingly important"],
            ["Industry transformation is driving new opportunities", "Digital innovation is reshaping business models", "Competitive advantage requires continuous adaptation"],
            ["Emerging technologies are creating market disruption", "Organizations are prioritizing efficiency and growth", "Data-driven strategies are becoming essential"]
        ])
        
        recommendations = random.choice([
            ["Assessment: Evaluate current market position", "Strategy Development: Create targeted action plans", "Execution: Implement systematic improvements"],
            ["Research: Analyze competitive landscape", "Planning: Develop comprehensive roadmap", "Implementation: Execute strategic initiatives"],
            ["Discovery: Identify key opportunities", "Design: Create innovative solutions", "Deployment: Launch strategic programs"]
        ])
        
        conclusion_variant = random.choice([
            "The current business environment presents both challenges and opportunities for forward-thinking organizations.",
            "Today's market conditions require organizations to balance innovation with operational excellence.",
            "Success in the modern business landscape demands both strategic vision and tactical execution."
        ])
        
        return f"""# {topic.title()}: Strategic Analysis and Market Insights

*Analysis Date: {current_time} | Report ID: FB-{session_id}*

## Executive Summary

Based on comprehensive research and market analysis, this report examines the current landscape of {topic.lower()} and identifies key trends shaping the industry's future direction.

## Market Intelligence

Our analysis reveals significant developments in the {topic.lower()} sector, with organizations increasingly focusing on innovation, efficiency, and sustainable growth strategies.

### Key Market Findings

- {insights[0]}
- {insights[1]} 
- {insights[2]}
- Regulatory changes are influencing strategic decisions
- Investment patterns indicate strong sector confidence

## Strategic Framework

Organizations seeking to capitalize on current market conditions should consider a multi-faceted approach that addresses both immediate opportunities and long-term positioning.

### Recommended Implementation Strategy

1. **{recommendations[0].split(':')[0]}**: {recommendations[0].split(':')[1].strip()}
2. **{recommendations[1].split(':')[0]}**: {recommendations[1].split(':')[1].strip()}
3. **{recommendations[2].split(':')[0]}**: {recommendations[2].split(':')[1].strip()}
4. **Monitoring**: Establish metrics and feedback loops for continuous improvement

## Industry Outlook

Market indicators suggest continued growth and evolution in the {topic.lower()} space. Organizations that proactively adapt their strategies while maintaining operational excellence are positioned for sustained success.

## Conclusion

{conclusion_variant} The insights presented in this analysis provide a foundation for informed decision-making and strategic planning.

---

*Research Context: {research_data[:150] if research_data else 'Comprehensive market research conducted'}...*

*Analysis generated using enhanced fallback methodology | Session: {session_id}*
*Technical Note: {error_msg}*"""

# Enhanced content generation function to support different AI models
def create_content_generator(preferred_model="auto"):
    """Create a content generator with specified model preference."""
    openai_api_key = os.getenv("OPENAI_API_KEY")
    claude_api_key = os.getenv("CLAUDE_API_KEY") or os.getenv("ANTHROPIC_API_KEY")
    
    # Auto-select model based on available API keys
    if preferred_model == "auto":
        if claude_api_key:
            preferred_model = "claude"
        elif openai_api_key:
            preferred_model = "openai"
        else:
            preferred_model = "fallback"
    
    return ContentGeneratorTool(
        openai_api_key=openai_api_key,
        claude_api_key=claude_api_key,
        preferred_model=preferred_model
    )

# Instantiate the tool with auto-selection
writing_tool = create_content_generator()

# Alternative instantiations for specific models
claude_writing_tool = create_content_generator("claude")
openai_writing_tool = create_content_generator("openai")
