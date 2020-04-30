from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)

    # Main webpage
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    # Import API
    from app.api import bp as api_bp
    app.register_blueprint(api_bp)

    return app, db


from app import models

