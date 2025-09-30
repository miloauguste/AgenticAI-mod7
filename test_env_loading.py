#!/usr/bin/env python3
"""
Test script to verify .env file loading and API key configuration
This script validates that all API keys are properly loaded from the .env file
"""

import os
from dotenv import load_dotenv

def test_env_loading():
    """Test that .env file is loaded and API keys are available."""
    print("🔧 TESTING .ENV FILE LOADING")
    print("=" * 50)
    
    # Load .env file
    load_dotenv()
    
    # Define expected API keys
    expected_keys = {
        'CLAUDE_API_KEY': 'Anthropic Claude API',
        'ANTHROPIC_API_KEY': 'Alternative Anthropic API key',
        'OPENAI_API_KEY': 'OpenAI GPT API',
        'SERPAPI_API_KEY': 'SerpAPI for Google Search',
        'GOOGLE_API_KEY': 'Google/Gemini API',
        'PINECONE_API_KEY': 'Pinecone Vector Database'
    }
    
    print("Checking API key availability:")
    print("-" * 35)
    
    loaded_keys = 0
    total_keys = len(expected_keys)
    
    for key_name, description in expected_keys.items():
        key_value = os.getenv(key_name)
        if key_value:
            # Mask the key for security (show first 10 and last 4 chars)
            if len(key_value) > 14:
                masked_key = key_value[:10] + "..." + key_value[-4:]
            else:
                masked_key = key_value[:6] + "..."
            
            print(f"✅ {key_name}: {masked_key}")
            loaded_keys += 1
        else:
            print(f"❌ {key_name}: NOT FOUND")
    
    print()
    print(f"API Keys Loaded: {loaded_keys}/{total_keys}")
    print(f"Success Rate: {(loaded_keys/total_keys)*100:.1f}%")
    
    return loaded_keys, total_keys

def test_claude_integration():
    """Test Claude AI integration with loaded API key."""
    print("\n🤖 TESTING CLAUDE AI INTEGRATION")
    print("=" * 40)
    
    try:
        from claude_content_generator import ClaudeContentGenerator
        
        claude_gen = ClaudeContentGenerator()
        
        print(f"Claude API Key Status: {'✅ LOADED' if not claude_gen.use_mock else '❌ NOT FOUND'}")
        print(f"Claude Model: {claude_gen.model}")
        print(f"Operation Mode: {'API' if not claude_gen.use_mock else 'Mock'}")
        
        if not claude_gen.use_mock:
            print("\n🎯 Testing content generation...")
            
            test_requirements = {
                'content_type': 'test_article',
                'topic': 'Environment configuration testing',
                'target_audience': 'developers',
                'tone': 'technical',
                'word_count': 150,
                'keywords': ['environment', 'configuration', 'API'],
                'content_goals': ['testing']
            }
            
            result = claude_gen.generate_content(test_requirements)
            
            if result and "content" in result:
                content_length = len(result["content"])
                quality_score = result.get("quality_score", 0)
                
                print(f"✅ Content generated: {content_length} characters")
                print(f"✅ Quality score: {quality_score}/100")
                print(f"✅ Model used: {result.get('generation_metadata', {}).get('model_used', 'unknown')}")
                
                return True
            else:
                print("❌ Content generation failed")
                return False
        else:
            print("⚠️ Running in mock mode - API key not available")
            return False
            
    except Exception as e:
        print(f"❌ Claude integration test failed: {e}")
        return False

def test_writing_tools():
    """Test writing tools with loaded API keys."""
    print("\n✍️ TESTING WRITING TOOLS")
    print("=" * 30)
    
    try:
        from writing_tool import claude_writing_tool, openai_writing_tool
        
        test_research = "Test research data about AI automation benefits for modern businesses."
        
        # Test Claude writing tool
        print("Testing Claude writing tool...")
        claude_result = claude_writing_tool._run(test_research)
        claude_success = len(claude_result) > 100
        print(f"Claude tool: {'✅ SUCCESS' if claude_success else '❌ FAILED'} ({len(claude_result)} chars)")
        
        # Test OpenAI writing tool  
        print("Testing OpenAI writing tool...")
        openai_result = openai_writing_tool._run(test_research)
        openai_success = len(openai_result) > 100
        print(f"OpenAI tool: {'✅ SUCCESS' if openai_success else '❌ FAILED'} ({len(openai_result)} chars)")
        
        return claude_success and openai_success
        
    except Exception as e:
        print(f"❌ Writing tools test failed: {e}")
        return False

def test_research_tools():
    """Test research tools with loaded API keys."""
    print("\n🔍 TESTING RESEARCH TOOLS")
    print("=" * 30)
    
    try:
        from research_tool import research_tool
        
        print(f"Available engines: {research_tool.get_available_engines()}")
        
        # Test research functionality
        print("Testing research query...")
        result = research_tool._run("AI automation trends 2024")
        
        research_success = len(result) > 50
        print(f"Research tool: {'✅ SUCCESS' if research_success else '❌ FAILED'} ({len(result)} chars)")
        
        return research_success
        
    except Exception as e:
        print(f"❌ Research tools test failed: {e}")
        return False

def run_comprehensive_test():
    """Run comprehensive test of all components."""
    print("🧪 COMPREHENSIVE .ENV LOADING TEST")
    print("=" * 50)
    print("Testing environment variable loading and API integration")
    print()
    
    try:
        # Test 1: Environment loading
        loaded_keys, total_keys = test_env_loading()
        env_success = loaded_keys >= 4  # At least 4 keys should be loaded
        
        # Test 2: Claude integration
        claude_success = test_claude_integration()
        
        # Test 3: Writing tools
        writing_success = test_writing_tools()
        
        # Test 4: Research tools
        research_success = test_research_tools()
        
        # Final results
        print("\n🏆 FINAL TEST RESULTS")
        print("=" * 30)
        print(f"Environment Loading: {'✅ PASS' if env_success else '❌ FAIL'}")
        print(f"Claude Integration: {'✅ PASS' if claude_success else '❌ FAIL'}")
        print(f"Writing Tools: {'✅ PASS' if writing_success else '❌ FAIL'}")
        print(f"Research Tools: {'✅ PASS' if research_success else '❌ FAIL'}")
        
        overall_success = env_success and claude_success and writing_success and research_success
        
        print()
        if overall_success:
            print("🎉 ALL TESTS PASSED!")
            print("✅ .env file loading is working correctly")
            print("✅ API keys are properly configured")
            print("✅ All components are operational")
        else:
            print("⚠️ SOME TESTS FAILED")
            print("Please check your .env file configuration")
            
        print()
        print("=" * 50)
        print("Environment configuration test completed!")
        
        return overall_success
        
    except Exception as e:
        print(f"❌ Comprehensive test failed: {e}")
        return False

if __name__ == "__main__":
    run_comprehensive_test()