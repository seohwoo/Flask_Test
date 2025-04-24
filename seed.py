from app import app
from models import db, Status, Auth

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

    db.session.commit()
