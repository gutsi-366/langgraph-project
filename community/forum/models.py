"""
Community Forum Models
=====================

Database models for the community forum including:
- User profiles and authentication
- Discussion threads and posts
- Analytics insights sharing
- Template reviews and ratings
- Community challenges and events
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import json

Base = declarative_base()

class User(Base):
    """User model for community members."""
    
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(100))
    company = Column(String(100))
    role = Column(String(50))  # analyst, developer, business_owner, etc.
    bio = Column(Text)
    avatar_url = Column(String(255))
    is_verified = Column(Boolean, default=False)
    is_moderator = Column(Boolean, default=False)
    reputation_score = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_active = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    posts = relationship("Post", back_populates="author")
    replies = relationship("Reply", back_populates="author")
    template_reviews = relationship("TemplateReview", back_populates="author")
    insights = relationship("AnalyticsInsight", back_populates="author")
    challenge_submissions = relationship("ChallengeSubmission", back_populates="author")

class Category(Base):
    """Forum categories for organizing discussions."""
    
    __tablename__ = 'categories'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    slug = Column(String(100), unique=True, nullable=False)
    color = Column(String(7))  # Hex color code
    icon = Column(String(50))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    threads = relationship("Thread", back_populates="category")

class Thread(Base):
    """Discussion thread model."""
    
    __tablename__ = 'threads'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    slug = Column(String(250), unique=True, nullable=False)
    content = Column(Text, nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)
    author_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    is_pinned = Column(Boolean, default=False)
    is_locked = Column(Boolean, default=False)
    is_featured = Column(Boolean, default=False)
    view_count = Column(Integer, default=0)
    reply_count = Column(Integer, default=0)
    like_count = Column(Integer, default=0)
    tags = Column(Text)  # JSON array of tags
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    category = relationship("Category", back_populates="threads")
    author = relationship("User")
    posts = relationship("Post", back_populates="thread")
    replies = relationship("Reply", back_populates="thread")

class Post(Base):
    """Post model for thread responses."""
    
    __tablename__ = 'posts'
    
    id = Column(Integer, primary_key=True)
    content = Column(Text, nullable=False)
    thread_id = Column(Integer, ForeignKey('threads.id'), nullable=False)
    author_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    is_solution = Column(Boolean, default=False)
    like_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    thread = relationship("Thread", back_populates="posts")
    author = relationship("User", back_populates="posts")
    replies = relationship("Reply", back_populates="post")

class Reply(Base):
    """Reply model for post responses."""
    
    __tablename__ = 'replies'
    
    id = Column(Integer, primary_key=True)
    content = Column(Text, nullable=False)
    post_id = Column(Integer, ForeignKey('posts.id'), nullable=False)
    thread_id = Column(Integer, ForeignKey('threads.id'), nullable=False)
    author_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    parent_reply_id = Column(Integer, ForeignKey('replies.id'))  # For nested replies
    like_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    post = relationship("Post", back_populates="replies")
    thread = relationship("Thread", back_populates="replies")
    author = relationship("User", back_populates="replies")
    parent_reply = relationship("Reply", remote_side=[id])

class AnalyticsInsight(Base):
    """Model for sharing analytics insights."""
    
    __tablename__ = 'analytics_insights'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    insight_type = Column(String(50))  # discovery, technique, tool, etc.
    industry = Column(String(50))
    data_source = Column(String(100))
    methodology = Column(Text)
    key_findings = Column(Text)  # JSON array
    visualizations = Column(Text)  # JSON array of image URLs
    code_snippets = Column(Text)  # JSON array
    tags = Column(Text)  # JSON array
    author_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    is_featured = Column(Boolean, default=False)
    view_count = Column(Integer, default=0)
    like_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    author = relationship("User", back_populates="insights")

class TemplateReview(Base):
    """Model for template reviews and ratings."""
    
    __tablename__ = 'template_reviews'
    
    id = Column(Integer, primary_key=True)
    template_id = Column(String(100), nullable=False)
    template_name = Column(String(200), nullable=False)
    author_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    rating = Column(Float, nullable=False)  # 1.0 to 5.0
    title = Column(String(200))
    review_text = Column(Text)
    pros = Column(Text)  # JSON array
    cons = Column(Text)  # JSON array
    use_case = Column(String(100))
    industry = Column(String(50))
    is_verified_purchase = Column(Boolean, default=False)
    helpful_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    author = relationship("User", back_populates="template_reviews")

class Challenge(Base):
    """Model for community challenges and competitions."""
    
    __tablename__ = 'challenges'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    challenge_type = Column(String(50))  # data_analysis, visualization, prediction, etc.
    dataset_url = Column(String(500))
    evaluation_criteria = Column(Text)
    prize_description = Column(Text)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    is_active = Column(Boolean, default=True)
    max_participants = Column(Integer)
    created_by = Column(Integer, ForeignKey('users.id'))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    submissions = relationship("ChallengeSubmission", back_populates="challenge")

class ChallengeSubmission(Base):
    """Model for challenge submissions."""
    
    __tablename__ = 'challenge_submissions'
    
    id = Column(Integer, primary_key=True)
    challenge_id = Column(Integer, ForeignKey('challenges.id'), nullable=False)
    author_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    methodology = Column(Text)
    results = Column(Text)  # JSON object
    code_url = Column(String(500))
    presentation_url = Column(String(500))
    score = Column(Float)
    ranking = Column(Integer)
    is_winner = Column(Boolean, default=False)
    submitted_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    challenge = relationship("Challenge", back_populates="submissions")
    author = relationship("User", back_populates="challenge_submissions")

class Event(Base):
    """Model for community events (webinars, meetups, etc.)."""
    
    __tablename__ = 'events'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    event_type = Column(String(50))  # webinar, meetup, workshop, conference
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    timezone = Column(String(50))
    location = Column(String(200))
    virtual_link = Column(String(500))
    max_attendees = Column(Integer)
    registration_required = Column(Boolean, default=False)
    is_featured = Column(Boolean, default=False)
    organizer_id = Column(Integer, ForeignKey('users.id'))
    created_at = Column(DateTime, default=datetime.utcnow)

class Notification(Base):
    """Model for user notifications."""
    
    __tablename__ = 'notifications'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    type = Column(String(50), nullable=False)  # mention, reply, like, etc.
    title = Column(String(200), nullable=False)
    message = Column(Text)
    related_entity_type = Column(String(50))  # thread, post, reply, etc.
    related_entity_id = Column(Integer)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class Tag(Base):
    """Model for tags used across the platform."""
    
    __tablename__ = 'tags'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(Text)
    usage_count = Column(Integer, default=0)
    is_trending = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class Like(Base):
    """Model for likes on various entities."""
    
    __tablename__ = 'likes'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    entity_type = Column(String(50), nullable=False)  # thread, post, reply, insight, etc.
    entity_id = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class Bookmark(Base):
    """Model for user bookmarks."""
    
    __tablename__ = 'bookmarks'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    entity_type = Column(String(50), nullable=False)  # thread, post, insight, template, etc.
    entity_id = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class AnalyticsTemplate(Base):
    """Model for community-shared analytics templates."""
    
    __tablename__ = 'analytics_templates'
    
    id = Column(Integer, primary_key=True)
    template_id = Column(String(100), unique=True, nullable=False)
    name = Column(String(200), nullable=False)
    description = Column(Text)
    category = Column(String(50))
    industry = Column(String(50))
    complexity_level = Column(String(20))  # beginner, intermediate, advanced
    author_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    template_data = Column(Text)  # JSON configuration
    code_examples = Column(Text)  # JSON array
    documentation = Column(Text)
    download_count = Column(Integer, default=0)
    rating_avg = Column(Float, default=0.0)
    rating_count = Column(Integer, default=0)
    is_featured = Column(Boolean, default=False)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    author = relationship("User")

class UserActivity(Base):
    """Model for tracking user activity."""
    
    __tablename__ = 'user_activity'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    activity_type = Column(String(50), nullable=False)
    entity_type = Column(String(50))
    entity_id = Column(Integer)
    metadata = Column(Text)  # JSON object
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User")

# Helper functions for JSON serialization
def serialize_json_field(value):
    """Serialize value to JSON string."""
    if isinstance(value, (list, dict)):
        return json.dumps(value)
    return value

def deserialize_json_field(value):
    """Deserialize JSON string to object."""
    if isinstance(value, str):
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return value
    return value
