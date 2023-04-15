import os
from configparser import ConfigParser

from .env import *

__CONFIG = None


def maybe_load_config():
    global __CONFIG
    if __CONFIG is None:
        __CONFIG = ConfigParser()
        location = os.path.realpath(
            os.path.join(os.getcwd(), os.path.dirname(__file__))
        )
        with open(os.path.join(location, f"{get_env()}.conf"), "r") as handle:
            __CONFIG.read_file(handle)
    return __CONFIG


def get_config() -> ConfigParser:
    maybe_load_config()
    return __CONFIG


def key_into_config(default, *keys) -> str:
    config = get_config()
    for key in keys:
        if key in config:
            config = config[key]
        else:
            return default
    return config


basedir = os.path.abspath(os.path.dirname(__file__))

# App secret key
SECRET_KEY = get_config()["WEBSERVER"]["FLASK_KEY"]
JWT_SECRET_KEY = get_config()["WEBSERVER"]["JWT_KEY"]

# Database secrets
SQLALCHEMY_DATABASE_URI = get_config()["DATABASE"].get("SQLALCHEMY_DATABASE_URI", None)
if SQLALCHEMY_DATABASE_URI is None:
    username = get_config()["DATABASE"]["USER"]
    password = get_config()["DATABASE"]["PASS"]
    host = get_config()["DATABASE"]["HOST"]
    port = get_config()["DATABASE"].get("PORT", "5432")
    db = get_config()["DATABASE"]["DATABASE"]
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{db}"
    )

JWT_TOKEN_LOCATION = ("headers", "cookies")
JWT_ACCESS_COOKIE_NAME = "Authorization"
SQLALCHEMY_TRACK_MODIFICATIONS = False
