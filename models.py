from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# This file defines the database models for the application
# It's separate from app.py to keep the code organized
db = SQLAlchemy()

class Article(db.Model):
    """
    Article model corresponding to the articles table in the database
    """
    __tablename__ = 'articles'

    id = db.Column(db.String(36), primary_key=True)  # UUID for each record
    filename = db.Column(db.String(255), nullable=False)  # Original filename
    url = db.Column(db.Text)  # Content URL
    time_recorded = db.Column(db.String(20))  # Time of recording (formatted as YYYYMMDD.HHMMSS)
    language = db.Column(db.String(10))  # Language code (e.g., 'eng')
    title = db.Column(db.Text)  # Content title
    content = db.Column(db.Text)  # Content
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Record creation timestamp

    def __repr__(self):
        return f'<Article {self.id}: {self.title}>'

    def to_dict(self):
        """Convert the Article object to a dictionary"""
        return {
            'id': self.id,
            'filename': self.filename,
            'url': self.url,
            'time_recorded': self.time_recorded,
            'language': self.language,
            'title': self.title,
            'content': self.content,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }