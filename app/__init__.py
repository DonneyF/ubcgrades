from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from werkzeug.routing import BaseConverter, ValidationError
from werkzeug.exceptions import BadRequest

db = SQLAlchemy()
migrate = Migrate()


class YearSession:
    def __init__(self, year, session):
        self.year = year  # type:str
        self.session = session  # type:str

    def __repr__(self):
        return self.year + self.session


class YearSessionConverter(BaseConverter):
    """Converts yearsessions for flask URLs."""

    def to_python(self, value):
        """Called to convert a `value` to its python equivalent.
        """
        # Anytime an invalid value is provided, raise ValidationError.  Flask
        # will catch this, and continue searching the other routes.  First,
        # check that value is an integer, if not there is no way it could be
        # a user.
        if len(value) < 5:
            raise BadRequest()
        year = value[0:4]
        session = value[4]

        try:
            int(year)
        except ValueError:
            raise BadRequest()

        if session not in {'W', 'S'}:
            raise BadRequest()

        return YearSession(year, session)

    def to_url(self, value):
        # Convert the yearsession to string
        return str(value)


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    app.url_map.converters['yearsession'] = YearSessionConverter

    db.init_app(app)
    migrate.init_app(app, db)

    # Main webpage
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    # Import API
    from app.api import bp as api_bp
    app.register_blueprint(api_bp)

    CORS(app)

    return app, db


from app import models

