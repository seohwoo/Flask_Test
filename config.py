import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "my-secret-key")
    #SQLALCHEMY_DATABASE_URI = "sqlite:///board.db"
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:Tjguddn98%21@localhost:3306/flask-db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False   # SQLAlchemy에서 객체 변경 추적 기능을 비활성화