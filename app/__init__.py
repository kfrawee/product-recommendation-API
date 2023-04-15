import datetime
import logging
from http import HTTPStatus
from logging.config import dictConfig

from flask import Flask
from flask_appbuilder import AppBuilder
from flask_cors import CORS

from app.api.db_models import db
from config import get_config, get_env

stage = get_env() == "STAGE"
prod = get_env() == "PROD"


def configure_logging():
    """
    Logging configuration
    """
    config = get_config()["LOGGING"]
    level = config.get("level", "DEBUG")
    format_ = config.get(
        "format", "%%(asctime)s:%%(levelname)s:%%(name)s:%%(lineno)d:%%(message)s"
    )
    dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": True,
            "formatters": {
                "default": {"format": format_},
            },
            "handlers": {
                "console": {
                    "level": "DEBUG",
                    "class": "logging.StreamHandler",
                    "formatter": "default",
                    "stream": "ext://sys.stdout",
                }
            },
            "loggers": {
                "": {
                    "handlers": ["console"],
                    "level": level,
                    "propagate": False,
                },
            },
        }
    )


def register_app():
    app = Flask(__name__)
    # Means that `/predict` and `/predict/` are the same route.
    app.url_map.strict_slashes = False

    # TODO: consider enabling cookie encryption?
    app.config["JWT_COOKIE_CSRF_PROTECT"] = False

    CORS(app)
    app.config.from_object("config")

    return app


def register_routes(app, db):
    from app.api.views.predict import PredictAPIView

    logger = logging.getLogger(__name__)

    @app.errorhandler(404)
    def not_found_handler(_):
        return ({"error": "Resource not found"}, HTTPStatus.NOT_FOUND)

    @app.errorhandler(500)
    def internal_server_error_handler(_):
        logger.exception("Internal server error")
        return ({"error": "Internal server error"}, HTTPStatus.INTERNAL_SERVER_ERROR)

    appbuilder = AppBuilder(
        app,
        db.session,
    )
    appbuilder.add_api(PredictAPIView)
    db.create_all()


configure_logging()

app = register_app()
db.init_app(app)

with app.app_context():
    register_routes(app, db)
