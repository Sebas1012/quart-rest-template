from quart import Quart

# Import config
from .config import Config

# Import blueprints
from .routes.hello import hello_bp
from .routes.auth import auth_bp

# Import utils
from .utils.docs import schema
from .utils.jwt import jwt
from .utils.db import init_db

def create_app() -> Quart:
    app = Quart(__name__)
    app.config.from_object(Config)

    schema.init_app(app)
    jwt.init_app(app)
    init_db(app, db_url=app.config["TORTOISE_DATABASE_URI"])

    app.register_blueprint(hello_bp)
    app.register_blueprint(auth_bp)

    return app