from . import db
from datetime import datetime, timezone

class Comment(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(50), db.ForeignKey("users.username"), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), nullable=False)
    content = db.Column(db.String(500), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, nullable=True)
    status_id = db.Column(db.Integer, db.ForeignKey("status.id"), nullable=False)
    
    post = db.relationship('Post', back_populates='comments')
    writer = db.relationship('User', back_populates='comments')
    status = db.relationship('Status', back_populates='comments')