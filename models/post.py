from . import db
from datetime import datetime, timezone

class Post(db.Model):
    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(50), db.ForeignKey("users.username") ,nullable=False)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(500), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, nullable=True)
    status_id = db.Column(db.Integer, db.ForeignKey("status.id"),nullable=False)
    readcnt = db.Column(db.Integer, default=0)
    
    writer = db.relationship('User', back_populates='posts')
    status = db.relationship('Status', back_populates='posts')
    comments = db.relationship('Comment', back_populates='post')