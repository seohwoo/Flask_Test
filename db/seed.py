import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import app
from models import db, Status, Auth, User

with app.app_context():
    if not Status.query.first():
        statuses = [
            Status(name='문의'),
            Status(name='공지'),
            Status(name='삭제')
        ]
        db.session.add_all(statuses)

    if not Auth.query.first():
        auths = [
            Auth(name='관리자'),
            Auth(name='사용자'),
        ]
        db.session.add_all(auths)
        
    if not User.query.first():
        users = [
            User(username='admin', password='admin', auth_id=1)
        ]
        db.session.add_all(users)

    db.session.commit()
