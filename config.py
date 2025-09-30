"""
Configuration settings for Innovate Marketing Solutions Content Creation System
"""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuration class for the content creation system"""
    
    # API Keys
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")
    
    # Content Settings
    MIN_WORD_COUNT = 300
    MAX_WORD_COUNT = 1500
    TARGET_WORD_COUNT = 800
    
    # Quality Thresholds
    MIN_QUALITY_SCORE = 80
    REVISION_THRESHOLD = 70
    
    # SEO Settings
    TARGET_KEYWORDS = [
        "AI", "automation", "technology", "startups", 
        "digital marketing", "small business", "innovation"
    ]
    
    # Content Types
    CONTENT_TYPES = {
        "blog_post": {
            "min_words": 800,
            "max_words": 1500,
            "target_audience": "technology professionals and startup founders"
        },
        "social_media": {
            "min_words": 50,
            "max_words": 280,
            "target_audience": "general tech-savvy audience"
        },
        "website_copy": {
            "min_words": 200,
            "max_words": 500,
            "target_audience": "potential clients and customers"
        }
    }
    
    # Industry Focus Areas
    FOCUS_AREAS = [
        "Artificial Intelligence",
        "Machine Learning", 
        "Digital Transformation",
        "Startup Growth",
        "Technology Trends",
        "Business Automation",
        "SaaS Solutions",
        "Fintech Innovation"
    ]
    
    @classmethod
    def validate_config(cls):
        """Validate that required configuration is present"""
        missing_keys = []
        
        if not cls.OPENAI_API_KEY:
            missing_keys.append("OPENAI_API_KEY")
        
        if not cls.SERPAPI_API_KEY:
            missing_keys.append("SERPAPI_API_KEY")
        
        if missing_keys:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_keys)}")
        
        return True

# Validate configuration on import
try:
    Config.validate_config()
    print("✅ Configuration validated successfully")
except ValueError as e:
    print(f"❌ Configuration error: {e}")
    print("Please check your .env file contains the required API keys")