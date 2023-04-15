import datetime

from app.api.db_models import db
from config import get_config, get_env
import json
import logging
from logging.config import dictConfig

from http import HTTPStatus
from flask import Flask

from flask_appbuilder import AppBuilder
from flask_cors import CORS

# from flask_migrate import Migrate
# from app.api.constants.keys import LARK_STAGE_ERROR_WEBHOOK_URL, LARK_PROD_ERROR_WEBHOOK_URL


# import requests

# redis_connection = None  # TODO: Remove redis with chat
# migrate = Migrate()

stage = get_env() == "STAGE"
prod = get_env() == "PROD"

# TODO: Implement a better way to skip the error logging
# ERRORS_TO_IGNORE = [
#     "Need to login",
#     "No user found with this email, please sign up.",
#     "No user found for this account",
#     "Invalid invitation code",
#     "No booking information found",
# ]


# class HTTPSStageLarkHandler(logging.Handler):
#     def emit(self, record):
#         if isinstance(record.msg, str):
#             for err in ERRORS_TO_IGNORE:
#                 if err in record.msg:
#                     return
#         lark_data = {"msg_type": "text", "content": {"text": self.format(record)}}
#         response = requests.post(
#             LARK_STAGE_ERROR_WEBHOOK_URL, data=json.dumps(lark_data), headers={"Content-Type": "application/json"}
#         )
#         if response.status_code != 200:
#             raise ValueError(
#                 "Request to lark returned an error %s, the response is:\n%s" % (response.status_code, response.text)
#             )
#         return response


# class HTTPSProdLarkHandler(logging.Handler):
#     def emit(self, record):
#         if isinstance(record.msg, str):
#             for err in ERRORS_TO_IGNORE:
#                 if err in record.msg:
#                     return
#         lark_data = {"msg_type": "text", "content": {"text": self.format(record)}}
#         response = requests.post(
#             LARK_PROD_ERROR_WEBHOOK_URL, data=json.dumps(lark_data), headers={"Content-Type": "application/json"}
#         )
#         if response.status_code != 200:
#             raise ValueError(
#                 "Request to lark returned an error %s, the response is:\n%s" % (response.status_code, response.text)
#             )
#         return response


def configure_logging():
    """
    Logging configuration
    """
    config = get_config()["LOGGING"]
    level = config.get("level", "DEBUG")
    format_ = config.get(
        "format", "%(asctime)s:%(levelname)s in %(module)s:%(message)s"
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
                    "level": "INFO",
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
deploy_time = datetime.datetime.now()
db.init_app(app)

with app.app_context():
    register_routes(app, db)
