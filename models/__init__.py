from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .user import User
from .post import Post
from .comment import Comment
from .auth import Auth
from .status import Status

__all__ = ['db', 'User', 'Post', 'Comment', 'Auth', 'Status']