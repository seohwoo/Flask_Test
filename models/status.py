from . import db

class Status(db.Model):
    __tablename__ = "status"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    
    posts = db.relationship('Post', back_populates='status')
    comments = db.relationship('Comment', back_populates='status')