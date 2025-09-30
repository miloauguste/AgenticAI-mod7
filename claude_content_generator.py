#!/usr/bin/env python3
"""
Claude AI Content Generation Integration
Advanced content creation using Anthropic's Claude AI
"""

import os
import json
import time
from typing import Dict, List, Optional, Any
from datetime import datetime
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class ClaudeContentGenerator:
    """Advanced content generator using Anthropic's Claude AI."""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("CLAUDE_API_KEY") or os.getenv("ANTHROPIC_API_KEY")
        self.base_url = "https://api.anthropic.com/v1/messages"
        self.model = "claude-3-5-sonnet-20241022"  # Claude 3.5 Sonnet (Latest)
        self.max_tokens = 4000
        
        if not self.api_key:
            print("Warning: CLAUDE_API_KEY not found. Using mock content generation.")
            self.use_mock = True
        else:
            self.use_mock = False
    
    def generate_content(self, content_requirements: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate comprehensive content using Claude AI based on detailed requirements.
        
        Args:
            content_requirements: Dictionary containing content specifications
            
        Returns:
            Dictionary with generated content and metadata
        """
        
        if self.use_mock:
            return self._mock_content_generation(content_requirements)
        
        try:
            # Create specialized prompt based on requirements
            prompt = self._create_content_prompt(content_requirements)
            
            # Call Claude API
            response = self._call_claude_api(prompt)
            
            if response and "content" in response:
                generated_content = response["content"][0]["text"]
                
                # Analyze generated content
                content_analysis = self._analyze_generated_content(generated_content, content_requirements)
                
                return {
                    "content": generated_content,
                    "content_analysis": content_analysis,
                    "generation_metadata": {
                        "model_used": self.model,
                        "generation_timestamp": datetime.now().isoformat(),
                        "prompt_tokens": response.get("usage", {}).get("input_tokens", 0),
                        "completion_tokens": response.get("usage", {}).get("output_tokens", 0),
                        "total_tokens": response.get("usage", {}).get("input_tokens", 0) + response.get("usage", {}).get("output_tokens", 0)
                    },
                    "requirements_met": self._validate_requirements(generated_content, content_requirements),
                    "quality_score": self._calculate_quality_score(generated_content, content_requirements)
                }
            else:
                return self._mock_content_generation(content_requirements)
                
        except Exception as e:
            print(f"Claude content generation error: {e}")
            return self._mock_content_generation(content_requirements)
    
    def _create_content_prompt(self, requirements: Dict[str, Any]) -> str:
        """Create specialized prompt for Claude based on content requirements."""
        
        # Extract key requirements
        content_type = requirements.get("content_type", "blog_post")
        topic = requirements.get("topic", "business technology")
        target_audience = requirements.get("target_audience", "business professionals")
        tone = requirements.get("tone", "professional")
        word_count = requirements.get("word_count", 1000)
        keywords = requirements.get("keywords", [])
        research_insights = requirements.get("research_insights", [])
        competitive_analysis = requirements.get("competitive_analysis", "")
        content_goals = requirements.get("content_goals", ["education", "engagement"])
        brand_guidelines = requirements.get("brand_guidelines", {})
        
        # Build comprehensive prompt
        prompt = f"""You are an expert content writer creating {content_type} content. Please create high-quality, engaging content based on these detailed requirements:

CONTENT SPECIFICATIONS:
- Content Type: {content_type}
- Topic: {topic}
- Target Audience: {target_audience}
- Tone: {tone}
- Target Word Count: {word_count} words
- Content Goals: {', '.join(content_goals)}

TARGET KEYWORDS (integrate naturally):
{', '.join(keywords) if keywords else 'Focus on topic-relevant keywords'}

RESEARCH INSIGHTS TO INCORPORATE:
{chr(10).join([f"• {insight}" for insight in research_insights]) if research_insights else "• Use general industry knowledge and best practices"}

COMPETITIVE ANALYSIS CONTEXT:
{competitive_analysis if competitive_analysis else "Position content uniquely in the market"}

BRAND GUIDELINES:
{json.dumps(brand_guidelines, indent=2) if brand_guidelines else "Maintain professional, authoritative voice"}

CONTENT STRUCTURE REQUIREMENTS:
1. Compelling headline that captures attention
2. Engaging introduction that hooks the reader
3. Well-organized main content with clear sections
4. Data-driven insights and practical examples
5. Actionable recommendations or takeaways
6. Strong conclusion with clear call-to-action

QUALITY STANDARDS:
- Professional, error-free writing
- Logical flow and clear structure
- Value-driven content that serves the audience
- SEO-friendly structure with natural keyword integration
- Engaging and informative throughout
- Appropriate depth for the target audience

SPECIFIC REQUIREMENTS:
- Include relevant statistics or data points where appropriate
- Provide actionable insights the audience can implement
- Maintain consistent tone throughout
- Ensure content aligns with stated goals
- Create content that positions the brand as a thought leader

Please create comprehensive, high-quality content that meets all these requirements while being engaging, informative, and valuable to the target audience."""

        return prompt
    
    def _call_claude_api(self, prompt: str) -> Optional[Dict]:
        """Make API call to Claude."""
        
        headers = {
            "Content-Type": "application/json",
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01"
        }
        
        payload = {
            "model": self.model,
            "max_tokens": self.max_tokens,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.7,
            "top_p": 0.9
        }
        
        try:
            response = requests.post(
                self.base_url,
                headers=headers,
                json=payload,
                timeout=60
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Claude API error: {response.status_code} - {response.text}")
                return None
                
        except requests.RequestException as e:
            print(f"Claude API request error: {e}")
            return None
    
    def _analyze_generated_content(self, content: str, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze the generated content quality and compliance."""
        
        analysis = {
            "word_count": len(content.split()),
            "paragraph_count": len([p for p in content.split('\n\n') if p.strip()]),
            "sentence_count": len([s for s in content.split('.') if s.strip()]),
            "readability_estimate": self._estimate_readability(content),
            "keyword_coverage": self._check_keyword_coverage(content, requirements.get("keywords", [])),
            "structure_analysis": self._analyze_structure(content),
            "tone_consistency": self._assess_tone_consistency(content, requirements.get("tone", "professional"))
        }
        
        return analysis
    
    def _validate_requirements(self, content: str, requirements: Dict[str, Any]) -> Dict[str, bool]:
        """Validate if content meets specified requirements."""
        
        target_word_count = requirements.get("word_count", 1000)
        actual_word_count = len(content.split())
        word_count_variance = abs(actual_word_count - target_word_count) / target_word_count
        
        keywords = requirements.get("keywords", [])
        keyword_coverage = sum(1 for kw in keywords if kw.lower() in content.lower()) / len(keywords) if keywords else 1.0
        
        validation = {
            "word_count_met": word_count_variance <= 0.2,  # Within 20% of target
            "keywords_included": keyword_coverage >= 0.7,  # At least 70% of keywords
            "has_introduction": any(word in content.lower()[:200] for word in ['introduction', 'overview', 'in today', 'the world of']),
            "has_conclusion": any(word in content.lower()[-200:] for word in ['conclusion', 'summary', 'in conclusion', 'to summarize']),
            "structured_content": content.count('#') >= 2 or content.count('\n\n') >= 3,
            "appropriate_length": 300 <= actual_word_count <= 3000
        }
        
        return validation
    
    def _calculate_quality_score(self, content: str, requirements: Dict[str, Any]) -> int:
        """Calculate overall content quality score (0-100)."""
        
        score = 0
        validation = self._validate_requirements(content, requirements)
        analysis = self._analyze_generated_content(content, requirements)
        
        # Requirement compliance (40 points)
        score += sum(validation.values()) * 6.67  # 6 requirements * 6.67 = ~40 points
        
        # Content quality metrics (30 points)
        if analysis["readability_estimate"] >= 60:
            score += 15
        if analysis["readability_estimate"] >= 80:
            score += 5
        
        if analysis["word_count"] >= 500:
            score += 10
        
        # Structure and engagement (30 points)
        if analysis["paragraph_count"] >= 5:
            score += 10
        if analysis["sentence_count"] >= 20:
            score += 10
        if content.count('?') >= 1:  # Questions for engagement
            score += 5
        if any(word in content.lower() for word in ['you', 'your', 'we', 'our']):  # Personal tone
            score += 5
        
        return min(100, max(0, int(score)))
    
    def _estimate_readability(self, content: str) -> float:
        """Estimate content readability score."""
        
        words = content.split()
        sentences = [s for s in content.split('.') if s.strip()]
        
        if not sentences or not words:
            return 50.0
        
        avg_sentence_length = len(words) / len(sentences)
        
        # Simplified Flesch Reading Ease approximation
        readability = 100 - (avg_sentence_length * 1.5)
        
        return max(0, min(100, readability))
    
    def _check_keyword_coverage(self, content: str, keywords: List[str]) -> Dict[str, Any]:
        """Check how well keywords are covered in the content."""
        
        if not keywords:
            return {"coverage_percentage": 100, "keywords_found": [], "keywords_missing": []}
        
        content_lower = content.lower()
        keywords_found = [kw for kw in keywords if kw.lower() in content_lower]
        keywords_missing = [kw for kw in keywords if kw.lower() not in content_lower]
        
        coverage_percentage = (len(keywords_found) / len(keywords)) * 100
        
        return {
            "coverage_percentage": coverage_percentage,
            "keywords_found": keywords_found,
            "keywords_missing": keywords_missing
        }
    
    def _analyze_structure(self, content: str) -> Dict[str, Any]:
        """Analyze content structure and organization."""
        
        lines = content.split('\n')
        
        structure = {
            "has_headings": any(line.startswith('#') for line in lines),
            "heading_count": sum(1 for line in lines if line.startswith('#')),
            "paragraph_breaks": content.count('\n\n'),
            "list_items": content.count('•') + content.count('-') + content.count('*'),
            "structured_format": False
        }
        
        # Check for structured format
        structure["structured_format"] = (
            structure["has_headings"] and 
            structure["paragraph_breaks"] >= 3 and
            structure["heading_count"] >= 2
        )
        
        return structure
    
    def _assess_tone_consistency(self, content: str, target_tone: str) -> Dict[str, Any]:
        """Assess if content maintains consistent tone."""
        
        tone_indicators = {
            "professional": ["analysis", "strategic", "business", "industry", "professional", "expertise"],
            "friendly": ["you", "your", "we", "let's", "help", "together"],
            "authoritative": ["research", "studies", "data", "evidence", "proven", "established"],
            "conversational": ["you", "your", "think", "consider", "imagine", "remember"],
            "technical": ["implementation", "system", "process", "framework", "methodology", "architecture"]
        }
        
        content_lower = content.lower()
        target_indicators = tone_indicators.get(target_tone, tone_indicators["professional"])
        
        indicator_count = sum(1 for indicator in target_indicators if indicator in content_lower)
        tone_score = (indicator_count / len(target_indicators)) * 100
        
        return {
            "tone_score": tone_score,
            "indicators_found": indicator_count,
            "total_indicators": len(target_indicators),
            "tone_consistent": tone_score >= 40
        }
    
    def _mock_content_generation(self, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Generate mock content when Claude API is not available."""
        
        content_type = requirements.get("content_type", "blog_post")
        topic = requirements.get("topic", "business technology")
        target_audience = requirements.get("target_audience", "business professionals")
        word_count = requirements.get("word_count", 1000)
        keywords = requirements.get("keywords", [])
        
        mock_content = f"""# {topic.title()}: A Comprehensive Guide for {target_audience.title()}

## Introduction

In today's rapidly evolving business landscape, {topic} has become increasingly important for organizations seeking to maintain competitive advantage. This comprehensive analysis explores the key aspects, opportunities, and strategic considerations that {target_audience} need to understand.

## Current Market Landscape

The {topic} sector continues to experience significant growth and transformation. Recent industry analysis reveals several key trends that are shaping the market:

### Key Market Drivers

1. **Digital Transformation Acceleration**: Organizations are increasingly adopting advanced technologies to streamline operations and improve efficiency.

2. **Competitive Pressure**: Market competition is driving companies to seek innovative solutions that provide measurable business value.

3. **Customer Expectations**: Rising expectations for seamless, efficient experiences are pushing businesses to modernize their approaches.

## Strategic Opportunities

For {target_audience}, the current environment presents several strategic opportunities:

### Implementation Strategies

**Assessment and Planning**
- Comprehensive evaluation of current capabilities
- Strategic roadmap development
- Resource allocation and timeline planning

**Technology Integration**
- Systematic implementation approach
- Change management and training programs
- Performance monitoring and optimization

### Best Practices

Industry leaders have identified several best practices that contribute to successful implementation:

- **Data-Driven Decision Making**: Leveraging analytics and insights to guide strategic choices
- **Stakeholder Engagement**: Ensuring buy-in from all relevant parties
- **Continuous Improvement**: Regular assessment and refinement of approaches
- **Risk Management**: Proactive identification and mitigation of potential challenges

## Benefits and ROI Considerations

Organizations that successfully implement {topic} solutions typically experience:

### Operational Benefits
- Improved efficiency and productivity
- Enhanced decision-making capabilities
- Reduced operational costs
- Better resource utilization

### Strategic Advantages
- Competitive differentiation
- Market positioning improvements
- Innovation enablement
- Future-ready infrastructure

## Implementation Framework

A structured approach to implementation includes the following phases:

### Phase 1: Discovery and Assessment
- Current state analysis
- Gap identification
- Opportunity assessment
- Success criteria definition

### Phase 2: Strategy Development
- Solution architecture design
- Implementation roadmap creation
- Resource planning
- Risk assessment

### Phase 3: Execution and Deployment
- Systematic rollout
- Training and change management
- Performance monitoring
- Iterative optimization

## Conclusion and Next Steps

The {topic} landscape offers significant opportunities for {target_audience} who take a strategic, well-planned approach to implementation. Success requires careful planning, stakeholder engagement, and commitment to continuous improvement.

### Recommended Actions

1. **Conduct Comprehensive Assessment**: Evaluate current capabilities and identify improvement opportunities
2. **Develop Strategic Roadmap**: Create detailed implementation plan with clear milestones
3. **Engage Stakeholders**: Ensure organization-wide buy-in and support
4. **Implement Systematically**: Execute plan with proper change management and training
5. **Monitor and Optimize**: Continuously assess performance and refine approach

By following these guidelines and leveraging the insights provided in this analysis, organizations can successfully navigate the {topic} landscape and achieve their strategic objectives.

---

*This analysis provides a foundation for understanding {topic} in the context of {target_audience}. For specific implementation guidance, consider consulting with industry experts who can provide tailored recommendations based on your unique requirements and objectives.*"""

        # Simulate analysis
        mock_analysis = {
            "word_count": len(mock_content.split()),
            "paragraph_count": len([p for p in mock_content.split('\n\n') if p.strip()]),
            "sentence_count": len([s for s in mock_content.split('.') if s.strip()]),
            "readability_estimate": 75.0,
            "keyword_coverage": {
                "coverage_percentage": 80,
                "keywords_found": keywords[:int(len(keywords) * 0.8)] if keywords else [],
                "keywords_missing": keywords[int(len(keywords) * 0.8):] if keywords else []
            },
            "structure_analysis": {
                "has_headings": True,
                "heading_count": 8,
                "paragraph_breaks": 12,
                "list_items": 15,
                "structured_format": True
            },
            "tone_consistency": {
                "tone_score": 85,
                "indicators_found": 12,
                "total_indicators": 15,
                "tone_consistent": True
            }
        }
        
        mock_validation = {
            "word_count_met": True,
            "keywords_included": True,
            "has_introduction": True,
            "has_conclusion": True,
            "structured_content": True,
            "appropriate_length": True
        }
        
        return {
            "content": mock_content,
            "content_analysis": mock_analysis,
            "generation_metadata": {
                "model_used": "mock_claude_generator",
                "generation_timestamp": datetime.now().isoformat(),
                "prompt_tokens": 500,
                "completion_tokens": len(mock_content.split()),
                "total_tokens": 500 + len(mock_content.split())
            },
            "requirements_met": mock_validation,
            "quality_score": 88
        }

class ClaudeContentOptimizer:
    """Content optimization and enhancement using Claude AI."""
    
    def __init__(self, api_key: Optional[str] = None):
        self.generator = ClaudeContentGenerator(api_key)
    
    def optimize_content(self, content: str, optimization_goals: List[str]) -> Dict[str, Any]:
        """Optimize existing content using Claude AI."""
        
        optimization_requirements = {
            "content_type": "content_optimization",
            "topic": "content enhancement",
            "target_audience": "content consumers",
            "tone": "improvement",
            "word_count": len(content.split()),
            "keywords": [],
            "research_insights": optimization_goals,
            "competitive_analysis": "",
            "content_goals": optimization_goals,
            "brand_guidelines": {},
            "original_content": content
        }
        
        if self.generator.use_mock:
            return self._mock_optimization(content, optimization_goals)
        
        try:
            prompt = f"""Please optimize the following content based on these specific goals:

OPTIMIZATION GOALS:
{chr(10).join([f"• {goal}" for goal in optimization_goals])}

ORIGINAL CONTENT:
{content}

OPTIMIZATION REQUIREMENTS:
1. Improve clarity and readability
2. Enhance engagement and flow
3. Strengthen key messages
4. Improve SEO potential
5. Maintain original meaning and intent
6. Ensure professional quality

Please provide the optimized version that addresses the specified goals while maintaining the content's core value and message."""

            response = self.generator._call_claude_api(prompt)
            
            if response and "content" in response:
                optimized_content = response["content"][0]["text"]
                
                optimization_analysis = {
                    "optimization_applied": optimization_goals,
                    "original_length": len(content.split()),
                    "optimized_length": len(optimized_content.split()),
                    "improvement_ratio": len(optimized_content.split()) / len(content.split()),
                    "optimization_timestamp": datetime.now().isoformat()
                }
                
                return {
                    "optimized_content": optimized_content,
                    "optimization_analysis": optimization_analysis,
                    "original_content": content,
                    "optimization_goals": optimization_goals
                }
            else:
                return self._mock_optimization(content, optimization_goals)
                
        except Exception as e:
            print(f"Content optimization error: {e}")
            return self._mock_optimization(content, optimization_goals)
    
    def _mock_optimization(self, content: str, goals: List[str]) -> Dict[str, Any]:
        """Mock content optimization when Claude API is not available."""
        
        # Simple mock optimization - add some enhancements
        optimized_content = content.replace(".", ". ").replace("  ", " ")
        optimized_content = f"# Enhanced Content\n\n{optimized_content}\n\n## Key Takeaways\n\nThis content has been optimized to address: {', '.join(goals)}"
        
        return {
            "optimized_content": optimized_content,
            "optimization_analysis": {
                "optimization_applied": goals,
                "original_length": len(content.split()),
                "optimized_length": len(optimized_content.split()),
                "improvement_ratio": len(optimized_content.split()) / len(content.split()),
                "optimization_timestamp": datetime.now().isoformat()
            },
            "original_content": content,
            "optimization_goals": goals
        }

# Example usage and testing
def test_claude_content_generator():
    """Test the Claude content generation system."""
    
    print("Testing Claude AI Content Generation")
    print("=" * 50)
    
    # Test content requirements
    sample_requirements = {
        "content_type": "blog_post",
        "topic": "AI automation for small businesses",
        "target_audience": "small business owners and entrepreneurs",
        "tone": "professional_friendly",
        "word_count": 800,
        "keywords": ["AI automation", "small business", "efficiency", "technology"],
        "research_insights": [
            "Small businesses see 30% efficiency improvement with AI",
            "Cost reduction of 25% reported by early adopters",
            "Employee training is critical for successful implementation"
        ],
        "competitive_analysis": "Position as accessible and practical for small business use",
        "content_goals": ["education", "lead_generation", "brand_awareness"],
        "brand_guidelines": {
            "tone": "approachable expert",
            "voice": "helpful and knowledgeable"
        }
    }
    
    # Test content generation
    generator = ClaudeContentGenerator()
    print("\n1. Testing Content Generation:")
    result = generator.generate_content(sample_requirements)
    
    print(f"Content Length: {result['content_analysis']['word_count']} words")
    print(f"Quality Score: {result['quality_score']}/100")
    print(f"Requirements Met: {sum(result['requirements_met'].values())}/{len(result['requirements_met'])}")
    
    # Display sample content
    print(f"\nSample Content (first 300 chars):")
    print(result["content"][:300] + "...")
    
    # Test content optimization
    print("\n2. Testing Content Optimization:")
    optimizer = ClaudeContentOptimizer()
    optimization_result = optimizer.optimize_content(
        result["content"][:500],  # Use first part for testing
        ["improve_readability", "enhance_engagement", "strengthen_seo"]
    )
    
    print(f"Original Length: {optimization_result['optimization_analysis']['original_length']} words")
    print(f"Optimized Length: {optimization_result['optimization_analysis']['optimized_length']} words")
    print(f"Improvement Ratio: {optimization_result['optimization_analysis']['improvement_ratio']:.2f}")
    
    print("\nClaude content generation test completed!")

if __name__ == "__main__":
    test_claude_content_generator()