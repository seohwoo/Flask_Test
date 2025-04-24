from flask import Flask, render_template, Blueprint
from config import Config
from views import blueprints
from flask_migrate import Migrate
from models import db, User, Post, Comment, Auth, Status

app = Flask("__name__")
app.config.from_object(Config)

db.init_app(app)

migrate = Migrate(app, db)

for bp in blueprints:
    app.register_blueprint(bp)

if "__name__" == "__main__":
    app.run(debug=True)