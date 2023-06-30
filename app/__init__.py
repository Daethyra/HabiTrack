from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.logger import configure_logger

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('../config.py')

    db.init_app(app)
    migrate.init_app(app, db)

    configure_logger(app)

    from app import views
    app.register_blueprint(views.bp)

    return app
