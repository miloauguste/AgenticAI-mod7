"""
Human Feedback System for Content Enhancement
Innovate Marketing Solutions - Content Creation Platform
"""

import json
import os
import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum
import uuid

class FeedbackType(Enum):
    CONTENT_QUALITY = "content_quality"
    TONE_STYLE = "tone_style"
    ACCURACY = "accuracy"
    STRUCTURE = "structure"
    SEO_OPTIMIZATION = "seo_optimization"
    ENGAGEMENT = "engagement"
    BRANDING = "branding"
    TECHNICAL_ACCURACY = "technical_accuracy"

class FeedbackStatus(Enum):
    PENDING_REVIEW = "pending_review"
    IN_REVIEW = "in_review"
    REVISION_REQUESTED = "revision_requested"
    APPROVED = "approved"
    REJECTED = "rejected"
    REQUIRES_MAJOR_REVISION = "requires_major_revision"

@dataclass
class FeedbackItem:
    feedback_id: str
    content_id: str
    editor_name: str
    feedback_type: FeedbackType
    rating: int  # 1-5 scale
    comments: str
    specific_suggestions: List[str]
    highlighted_sections: List[Dict[str, str]]  # {"section": "text", "issue": "description"}
    timestamp: str
    priority: str  # "low", "medium", "high", "critical"
    
@dataclass
class ContentFeedback:
    content_id: str
    content_title: str
    original_content: str
    current_version: str
    status: FeedbackStatus
    overall_rating: float
    feedback_items: List[FeedbackItem]
    revision_history: List[Dict[str, Any]]
    created_at: str
    last_updated: str
    client_name: str
    content_type: str

class HumanFeedbackManager:
    def __init__(self, storage_path: str = "feedback_data"):
        self.storage_path = storage_path
        self.feedback_file = os.path.join(storage_path, "content_feedback.json")
        self._ensure_storage_directory()
        
    def _ensure_storage_directory(self):
        """Ensure the storage directory exists."""
        if not os.path.exists(self.storage_path):
            os.makedirs(self.storage_path)
            
    def _load_feedback_data(self) -> Dict[str, Dict]:
        """Load feedback data from storage."""
        if os.path.exists(self.feedback_file):
            try:
                with open(self.feedback_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading feedback data: {e}")
        return {}
    
    def _save_feedback_data(self, data: Dict[str, Dict]):
        """Save feedback data to storage."""
        try:
            with open(self.feedback_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False, default=str)
        except Exception as e:
            print(f"Error saving feedback data: {e}")
    
    def create_content_feedback(self, content_id: str, content_title: str, 
                              original_content: str, client_name: str, 
                              content_type: str) -> ContentFeedback:
        """Create a new content feedback record."""
        content_feedback = ContentFeedback(
            content_id=content_id,
            content_title=content_title,
            original_content=original_content,
            current_version=original_content,
            status=FeedbackStatus.PENDING_REVIEW,
            overall_rating=0.0,
            feedback_items=[],
            revision_history=[],
            created_at=datetime.datetime.now().isoformat(),
            last_updated=datetime.datetime.now().isoformat(),
            client_name=client_name,
            content_type=content_type
        )
        
        # Save to storage
        data = self._load_feedback_data()
        data[content_id] = asdict(content_feedback)
        self._save_feedback_data(data)
        
        return content_feedback
    
    def add_feedback(self, content_id: str, editor_name: str, 
                    feedback_type: FeedbackType, rating: int, comments: str,
                    specific_suggestions: List[str] = None, 
                    highlighted_sections: List[Dict[str, str]] = None,
                    priority: str = "medium") -> str:
        """Add feedback to a content item."""
        
        feedback_id = str(uuid.uuid4())
        
        feedback_item = FeedbackItem(
            feedback_id=feedback_id,
            content_id=content_id,
            editor_name=editor_name,
            feedback_type=feedback_type,
            rating=rating,
            comments=comments,
            specific_suggestions=specific_suggestions or [],
            highlighted_sections=highlighted_sections or [],
            timestamp=datetime.datetime.now().isoformat(),
            priority=priority
        )
        
        # Load and update data
        data = self._load_feedback_data()
        if content_id in data:
            data[content_id]['feedback_items'].append(asdict(feedback_item))
            data[content_id]['last_updated'] = datetime.datetime.now().isoformat()
            
            # Update overall rating
            feedback_items = data[content_id]['feedback_items']
            if feedback_items:
                total_rating = sum(item['rating'] for item in feedback_items)
                data[content_id]['overall_rating'] = total_rating / len(feedback_items)
            
            # Update status based on ratings and priority
            self._update_content_status(data[content_id])
            
            self._save_feedback_data(data)
        
        return feedback_id
    
    def _update_content_status(self, content_data: Dict):
        """Update content status based on feedback."""
        feedback_items = content_data['feedback_items']
        if not feedback_items:
            return
            
        avg_rating = content_data['overall_rating']
        has_critical = any(item['priority'] == 'critical' for item in feedback_items)
        has_high_priority = any(item['priority'] == 'high' for item in feedback_items)
        
        if has_critical or avg_rating < 2.0:
            content_data['status'] = FeedbackStatus.REQUIRES_MAJOR_REVISION.value
        elif avg_rating < 3.0 or has_high_priority:
            content_data['status'] = FeedbackStatus.REVISION_REQUESTED.value
        elif avg_rating >= 4.0:
            content_data['status'] = FeedbackStatus.APPROVED.value
        else:
            content_data['status'] = FeedbackStatus.IN_REVIEW.value
    
    def get_content_feedback(self, content_id: str) -> Optional[ContentFeedback]:
        """Get feedback for a specific content item."""
        data = self._load_feedback_data()
        if content_id in data:
            feedback_data = data[content_id]
            return ContentFeedback(**feedback_data)
        return None
    
    def update_content_version(self, content_id: str, new_content: str, 
                             revision_notes: str = "", editor_name: str = "Anonymous") -> bool:
        """Update the content version after revisions."""
        data = self._load_feedback_data()
        if content_id in data:
            # Add to revision history
            revision_entry = {
                "version": len(data[content_id]['revision_history']) + 1,
                "content": new_content,
                "timestamp": datetime.datetime.now().isoformat(),
                "notes": revision_notes,
                "editor_name": editor_name,
                "previous_content": data[content_id]['current_version'],
                "word_count": len(new_content.split()),
                "character_count": len(new_content),
                "changes_summary": self._analyze_content_changes(data[content_id]['current_version'], new_content)
            }
            
            data[content_id]['revision_history'].append(revision_entry)
            data[content_id]['current_version'] = new_content
            data[content_id]['last_updated'] = datetime.datetime.now().isoformat()
            
            self._save_feedback_data(data)
            return True
        return False
    
    def get_content_history(self, content_id: str) -> List[Dict[str, Any]]:
        """Get revision history for content."""
        data = self._load_feedback_data()
        if content_id in data:
            return data[content_id]['revision_history']
        return []
    
    def get_pending_reviews(self) -> List[ContentFeedback]:
        """Get all content items pending review."""
        data = self._load_feedback_data()
        pending_items = []
        
        for content_id, feedback_data in data.items():
            if feedback_data['status'] in [
                FeedbackStatus.PENDING_REVIEW.value,
                FeedbackStatus.IN_REVIEW.value,
                FeedbackStatus.REVISION_REQUESTED.value
            ]:
                pending_items.append(ContentFeedback(**feedback_data))
        
        return sorted(pending_items, key=lambda x: x.created_at, reverse=True)
    
    def get_feedback_analytics(self) -> Dict[str, Any]:
        """Get analytics on feedback data."""
        data = self._load_feedback_data()
        
        total_content = len(data)
        status_counts = {}
        avg_ratings = []
        feedback_type_counts = {}
        
        for content_id, feedback_data in data.items():
            status = feedback_data['status']
            status_counts[status] = status_counts.get(status, 0) + 1
            
            if feedback_data['overall_rating'] > 0:
                avg_ratings.append(feedback_data['overall_rating'])
            
            for feedback_item in feedback_data['feedback_items']:
                feedback_type = feedback_item['feedback_type']
                feedback_type_counts[feedback_type] = feedback_type_counts.get(feedback_type, 0) + 1
        
        return {
            "total_content_items": total_content,
            "status_distribution": status_counts,
            "average_rating": sum(avg_ratings) / len(avg_ratings) if avg_ratings else 0,
            "feedback_type_distribution": feedback_type_counts,
            "content_with_feedback": len([d for d in data.values() if d['feedback_items']]),
            "approval_rate": status_counts.get(FeedbackStatus.APPROVED.value, 0) / total_content if total_content > 0 else 0
        }
    
    def export_feedback_report(self, content_id: str = None) -> Dict[str, Any]:
        """Export detailed feedback report."""
        data = self._load_feedback_data()
        
        if content_id:
            # Single content report
            if content_id not in data:
                return {"error": "Content not found"}
            
            content_data = data[content_id]
            return {
                "content_id": content_id,
                "content_title": content_data['content_title'],
                "client_name": content_data['client_name'],
                "status": content_data['status'],
                "overall_rating": content_data['overall_rating'],
                "feedback_summary": self._generate_feedback_summary(content_data['feedback_items']),
                "revision_count": len(content_data['revision_history']),
                "created_at": content_data['created_at'],
                "last_updated": content_data['last_updated']
            }
        else:
            # Full report
            return {
                "report_generated": datetime.datetime.now().isoformat(),
                "analytics": self.get_feedback_analytics(),
                "content_items": [
                    {
                        "content_id": cid,
                        "title": cdata['content_title'],
                        "status": cdata['status'],
                        "rating": cdata['overall_rating'],
                        "feedback_count": len(cdata['feedback_items'])
                    }
                    for cid, cdata in data.items()
                ]
            }
    
    def _generate_feedback_summary(self, feedback_items: List[Dict]) -> Dict[str, Any]:
        """Generate a summary of feedback items."""
        if not feedback_items:
            return {"message": "No feedback available"}
        
        by_type = {}
        by_priority = {}
        common_issues = []
        
        for item in feedback_items:
            feedback_type = item['feedback_type']
            priority = item['priority']
            
            if feedback_type not in by_type:
                by_type[feedback_type] = []
            by_type[feedback_type].append(item)
            
            by_priority[priority] = by_priority.get(priority, 0) + 1
            
            if item['comments']:
                common_issues.append(item['comments'])
        
        return {
            "feedback_by_type": {k: len(v) for k, v in by_type.items()},
            "priority_distribution": by_priority,
            "total_feedback_items": len(feedback_items),
            "average_rating": sum(item['rating'] for item in feedback_items) / len(feedback_items)
        }

# Global feedback manager instance
feedback_manager = HumanFeedbackManager()

# Utility functions for easy integration
def create_content_for_review(content_id: str, title: str, content: str, 
                            client_name: str, content_type: str) -> ContentFeedback:
    """Convenience function to create content for review."""
    return feedback_manager.create_content_feedback(
        content_id, title, content, client_name, content_type
    )

def add_editor_feedback(content_id: str, editor_name: str, feedback_type: str,
                       rating: int, comments: str, suggestions: List[str] = None,
                       priority: str = "medium") -> str:
    """Convenience function to add editor feedback."""
    return feedback_manager.add_feedback(
        content_id, editor_name, FeedbackType(feedback_type), 
        rating, comments, suggestions, priority=priority
    )

def get_content_for_editing(content_id: str) -> Optional[ContentFeedback]:
    """Get content item for editing."""
    return feedback_manager.get_content_feedback(content_id)

def submit_revised_content(content_id: str, revised_content: str, notes: str = "") -> bool:
    """Submit revised content."""
    return feedback_manager.update_content_version(content_id, revised_content, notes)