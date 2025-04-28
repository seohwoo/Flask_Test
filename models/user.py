from . import db
from .auth import Auth
from flask_login import UserMixin
from datetime import datetime, timezone

class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    auth_id = db.Column(db.Integer, db.ForeignKey("auth.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, nullable=True)
    
    auth = db.relationship('Auth', back_populates='users')
    posts = db.relationship('Post', back_populates='users')
    comments = db.relationship('Comment', back_populates='users')
    
    def is_admin(self):
        stmt = db.select(Auth).where(Auth.name=="관리자")
        auth_id = db.session.execute(stmt).scalars().first().id
        return self.auth_id == auth_id