"""
Minimal Tool Integration: DuckDuckGo + SerpAPI
"""

import os
import requests
from typing import Dict, List, Any

try:
    from serpapi.google_search_results import GoogleSearchResults
    SERPAPI_AVAILABLE = True
except ImportError:
    try:
        from serpapi import GoogleSearch as GoogleSearchResults
        SERPAPI_AVAILABLE = True
    except ImportError:
        GoogleSearchResults = None
        SERPAPI_AVAILABLE = False

class DuckDuckGoTool:
    """Minimal DuckDuckGo search tool"""
    
    def __init__(self):
        self.base_url = "https://api.duckduckgo.com/"
    
    def search(self, query: str, max_results: int = 5) -> List[Dict[str, str]]:
        """Search using DuckDuckGo Instant Answer API"""
        try:
            params = {
                'q': query,
                'format': 'json',
                'no_redirect': '1',
                'no_html': '1',
                'skip_disambig': '1'
            }
            
            response = requests.get(self.base_url, params=params, timeout=10)
            data = response.json()
            
            results = []
            
            # Extract abstract
            if data.get('Abstract'):
                results.append({
                    'title': data.get('AbstractText', query),
                    'snippet': data.get('Abstract', ''),
                    'url': data.get('AbstractURL', ''),
                    'source': 'duckduckgo_abstract'
                })
            
            # Extract related topics
            for topic in data.get('RelatedTopics', [])[:max_results-1]:
                if isinstance(topic, dict) and topic.get('Text'):
                    results.append({
                        'title': topic.get('Text', '').split(' - ')[0],
                        'snippet': topic.get('Text', ''),
                        'url': topic.get('FirstURL', ''),
                        'source': 'duckduckgo_related'
                    })
            
            return results[:max_results]
            
        except Exception as e:
            return [{'title': f'Search error: {e}', 'snippet': '', 'url': '', 'source': 'error'}]

class SerpAPITool:
    """Minimal SerpAPI keyword research tool"""
    
    def __init__(self):
        if not SERPAPI_AVAILABLE:
            raise ValueError("SerpAPI package not available")
        
        self.api_key = os.getenv('SERPAPI_API_KEY')
        if not self.api_key:
            raise ValueError("SERPAPI_API_KEY environment variable required")
    
    def search_keywords(self, query: str, max_results: int = 5) -> List[Dict[str, Any]]:
        """Search for keywords and related terms"""
        try:
            search = GoogleSearchResults({
                "q": query,
                "api_key": self.api_key,
                "num": max_results,
                "hl": "en"
            })
            
            results = search.get_dict()
            
            formatted_results = []
            
            # Extract organic results
            for result in results.get("organic_results", [])[:max_results]:
                formatted_results.append({
                    'title': result.get('title', ''),
                    'snippet': result.get('snippet', ''),
                    'url': result.get('link', ''),
                    'source': 'serpapi_organic'
                })
            
            return formatted_results
            
        except Exception as e:
            return [{'title': f'SerpAPI error: {e}', 'snippet': '', 'url': '', 'source': 'error'}]
    
    def get_related_searches(self, query: str) -> List[str]:
        """Get related search terms"""
        try:
            search = GoogleSearchResults({
                "q": query,
                "api_key": self.api_key
            })
            
            results = search.get_dict()
            related = []
            
            # Extract related searches
            for item in results.get("related_searches", []):
                if item.get('query'):
                    related.append(item['query'])
            
            return related[:8]
            
        except Exception as e:
            return [f"Related search error: {e}"]

class IntegratedResearchTool:
    """Minimal integrated research tool combining both APIs"""
    
    def __init__(self):
        self.ddg = DuckDuckGoTool()
        try:
            self.serp = SerpAPITool()
            self.has_serpapi = True
        except ValueError:
            self.serp = None
            self.has_serpapi = False
    
    def comprehensive_search(self, query: str) -> Dict[str, Any]:
        """Perform comprehensive research using both tools"""
        
        results = {
            'query': query,
            'ddg_results': [],
            'serp_results': [],
            'related_keywords': [],
            'total_sources': 0
        }
        
        # DuckDuckGo search
        results['ddg_results'] = self.ddg.search(query, max_results=3)
        
        # SerpAPI search (if available)
        if self.has_serpapi:
            results['serp_results'] = self.serp.search_keywords(query, max_results=3)
            results['related_keywords'] = self.serp.get_related_searches(query)
        
        # Combine results
        all_results = results['ddg_results'] + results['serp_results']
        results['total_sources'] = len(all_results)
        
        return results

# =============================================================================
# TOOL INTEGRATION FUNCTIONS
# =============================================================================

def enhanced_research_with_tools(query: str) -> Dict[str, Any]:
    """Enhanced research function using integrated tools"""
    
    tool = IntegratedResearchTool()
    research_data = tool.comprehensive_search(query)
    
    # Extract keywords from all results
    all_text = ""
    for result in research_data['ddg_results'] + research_data['serp_results']:
        all_text += f"{result.get('title', '')} {result.get('snippet', '')} "
    
    # Simple keyword extraction
    words = all_text.lower().split()
    keywords = list(set([w for w in words if len(w) > 4 and w.isalpha()]))[:10]
    
    return {
        'search_results': research_data['ddg_results'] + research_data['serp_results'],
        'extracted_keywords': keywords,
        'related_keywords': research_data['related_keywords'],
        'research_confidence': min(1.0, research_data['total_sources'] / 5.0),
        'research_summary': f"Found {research_data['total_sources']} sources for '{query}'"
    }

def get_keyword_suggestions(topic: str) -> List[str]:
    """Get keyword suggestions for SEO optimization"""
    
    try:
        tool = IntegratedResearchTool()
        if tool.has_serpapi:
            related = tool.serp.get_related_searches(topic)
            return related[:5]
        else:
            # Fallback keyword generation
            base_words = topic.lower().split()
            suggestions = []
            for word in base_words:
                suggestions.extend([
                    f"{word} benefits",
                    f"{word} guide",
                    f"how to {word}",
                    f"{word} 2024"
                ])
            return suggestions[:5]
    except:
        return [f"{topic} guide", f"{topic} benefits"]

# =============================================================================
# INTEGRATION WITH EXISTING WORKFLOW
# =============================================================================

def integrated_research_agent(state):
    """Research agent using integrated tools"""
    
    print("🔍 RESEARCH AGENT WITH INTEGRATED TOOLS")
    
    try:
        # Build research query
        query = f"{state.topic} {state.content_type} {state.target_audience or ''}"
        
        # Use integrated tools
        research_results = enhanced_research_with_tools(query)
        
        # Update state
        state.search_results = research_results['search_results']
        state.extracted_keywords = research_results['extracted_keywords']
        state.research_confidence = research_results['research_confidence']
        state.research_summary = research_results['research_summary']
        
        # Get additional keyword suggestions
        keyword_suggestions = get_keyword_suggestions(state.topic)
        state.extracted_keywords.extend(keyword_suggestions)
        
        print(f"✅ Research complete: {len(state.search_results)} sources, confidence: {state.research_confidence:.2f}")
        
    except Exception as e:
        print(f"❌ Research failed: {e}")
        state.error_messages.append(f"Research error: {e}")
        state.research_confidence = 0.0
    
    return state

def integrated_seo_optimization(state):
    """SEO optimization using keyword tools"""
    
    print("🔍 SEO OPTIMIZATION WITH KEYWORD TOOLS")
    
    try:
        # Get additional keyword suggestions
        additional_keywords = get_keyword_suggestions(state.topic)
        
        # Combine with existing keywords
        all_keywords = list(set(state.primary_keywords + additional_keywords))
        state.primary_keywords = all_keywords[:5]
        
        # Apply basic SEO optimization
        content = state.draft_content
        keywords_str = ", ".join(state.primary_keywords)
        
        # Simple keyword integration
        optimized_content = content
        for keyword in state.primary_keywords[:3]:
            if keyword.lower() not in content.lower():
                optimized_content = f"{keyword} is important. {optimized_content}"
        
        state.optimized_content = optimized_content
        state.seo_score = min(100, 60 + len(state.primary_keywords) * 5)
        
        # Generate meta description
        first_sentences = ". ".join(content.split(". ")[:2])
        state.meta_description = first_sentences[:157] + "..."
        
        # Generate title suggestions
        state.title_suggestions = [
            f"{state.topic}: Complete Guide",
            f"How to {state.topic}",
            f"{state.topic} - Best Practices"
        ]
        
        print(f"✅ SEO optimization complete: Score {state.seo_score}/100")
        
    except Exception as e:
        print(f"❌ SEO optimization failed: {e}")
        state.optimized_content = state.draft_content
        state.seo_score = 50.0
    
    return state

if __name__ == "__main__":
    # Test tools
    print("Testing integrated research tools...")
    
    # Test DuckDuckGo
    ddg = DuckDuckGoTool()
    ddg_results = ddg.search("AI automation")
    print(f"DuckDuckGo results: {len(ddg_results)}")
    
    # Test comprehensive search
    research_tool = IntegratedResearchTool()
    results = research_tool.comprehensive_search("small business automation")
    print(f"Total sources: {results['total_sources']}")
    print(f"Has SerpAPI: {research_tool.has_serpapi}")