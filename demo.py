"""
Demo script for Innovate Marketing Solutions Multi-Agent Content Creation System
"""
import sys
import time
from config import Config
from main import run_content_pipeline
from langgraph_workflow import run_langgraph_pipeline

def print_header():
    """Print a nice header for the demo"""
    print("="*80)
    print("🚀 INNOVATE MARKETING SOLUTIONS")
    print("   Multi-Agent Content Creation System Demo")
    print("="*80)

def demo_crewai_workflow():
    """Demonstrate the CrewAI-based workflow"""
    print("\n📋 DEMO 1: CrewAI Multi-Agent Workflow")
    print("-" * 50)
    
    topics = [
        "AI-powered customer service automation",
        "Blockchain technology for small businesses", 
        "Remote work productivity tools for startups"
    ]
    
    for i, topic in enumerate(topics, 1):
        print(f"\n🎯 Example {i}: {topic}")
        print("⏳ Running CrewAI pipeline...")
        
        try:
            result = run_content_pipeline(
                topic=topic,
                content_type="blog_post"
            )
            
            if result:
                print("✅ CrewAI pipeline completed successfully")
                print(f"📊 Result preview: {str(result)[:200]}...")
            else:
                print("❌ CrewAI pipeline failed")
                
        except Exception as e:
            print(f"❌ Error in CrewAI demo: {e}")
        
        if i < len(topics):
            print("\n⏱️ Waiting 3 seconds before next example...")
            time.sleep(3)

def demo_langgraph_workflow():
    """Demonstrate the LangGraph-based workflow"""
    print("\n🔗 DEMO 2: LangGraph State-Based Workflow")
    print("-" * 50)
    
    topics = [
        "Machine learning for marketing optimization",
        "Cybersecurity essentials for tech startups"
    ]
    
    for i, topic in enumerate(topics, 1):
        print(f"\n🎯 Example {i}: {topic}")
        print("⏳ Running LangGraph pipeline...")
        
        try:
            result = run_langgraph_pipeline(topic)
            
            if "error" not in result:
                print("✅ LangGraph pipeline completed successfully")
                print(f"📊 Quality Score: {result.get('quality_score', 0)}/100")
                print(f"📝 Word Count: {result.get('metadata', {}).get('final_word_count', 0)}")
                print(f"🔍 Content preview: {result.get('final_content', '')[:200]}...")
            else:
                print(f"❌ LangGraph pipeline failed: {result['error']}")
                
        except Exception as e:
            print(f"❌ Error in LangGraph demo: {e}")
        
        if i < len(topics):
            print("\n⏱️ Waiting 3 seconds before next example...")
            time.sleep(3)

def interactive_demo():
    """Run an interactive demo where user can input topics"""
    print("\n🎮 INTERACTIVE DEMO")
    print("-" * 50)
    print("Enter your own topic for content creation!")
    
    while True:
        try:
            topic = input("\n💭 Enter a topic (or 'quit' to exit): ").strip()
            
            if topic.lower() in ['quit', 'exit', 'q']:
                print("👋 Thanks for using the demo!")
                break
            
            if not topic:
                print("⚠️ Please enter a valid topic")
                continue
            
            print("\n🔧 Choose workflow:")
            print("1. CrewAI (sequential agents)")
            print("2. LangGraph (state-based)")
            
            choice = input("Enter choice (1 or 2): ").strip()
            
            if choice == "1":
                print(f"\n🚀 Running CrewAI workflow for: {topic}")
                result = run_content_pipeline(topic=topic, content_type="blog_post")
                print("✅ CrewAI workflow completed")
                
            elif choice == "2":
                print(f"\n🚀 Running LangGraph workflow for: {topic}")
                result = run_langgraph_pipeline(topic)
                
                if "error" not in result:
                    print("✅ LangGraph workflow completed")
                    print(f"Quality Score: {result.get('quality_score', 0)}/100")
                else:
                    print(f"❌ Error: {result['error']}")
                    
            else:
                print("⚠️ Invalid choice. Please enter 1 or 2.")
                
        except KeyboardInterrupt:
            print("\n👋 Demo interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error in interactive demo: {e}")

def main():
    """Main demo function"""
    print_header()
    
    # Check configuration
    try:
        Config.validate_config()
        print("✅ Configuration check passed")
    except ValueError as e:
        print(f"❌ Configuration error: {e}")
        print("\n📋 Setup Instructions:")
        print("1. Create a .env file in this directory")
        print("2. Add your API keys:")
        print("   OPENAI_API_KEY=your_openai_key_here")
        print("   SERPAPI_API_KEY=your_serpapi_key_here")
        print("3. Run pip install -r requirements.txt")
        return
    
    print("\n🎯 This demo showcases two different multi-agent approaches:")
    print("   1. CrewAI: Sequential agent collaboration")
    print("   2. LangGraph: State-based workflow orchestration")
    
    demo_choice = input("\n🔧 Run full demo? (y/n): ").strip().lower()
    
    if demo_choice in ['y', 'yes']:
        demo_crewai_workflow()
        demo_langgraph_workflow()
    
    interactive_choice = input("\n🎮 Try interactive demo? (y/n): ").strip().lower()
    
    if interactive_choice in ['y', 'yes']:
        interactive_demo()
    
    print("\n🎉 Demo completed! Thank you for exploring our multi-agent content creation system.")
    print("\n📚 System Features:")
    print("   • Automated topic research and trend analysis")
    print("   • AI-powered content generation for multiple formats")
    print("   • SEO optimization and keyword integration")
    print("   • Quality assurance and content review")
    print("   • Scalable workflows for high-volume content needs")

if __name__ == "__main__":
    main()