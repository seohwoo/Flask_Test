from flask import Flask
from config import Config
from views import blueprints
from flask_migrate import Migrate
from models import db
from auth import init_login

app = Flask("__name__")
app.config.from_object(Config)

db.init_app(app)
init_login(app)

migrate = Migrate(app, db)

for bp, prefix in blueprints:
    app.register_blueprint(bp, url_prefix=prefix)

if "__name__" == "__main__":
    app.run(debug=True)