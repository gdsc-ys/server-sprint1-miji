import os

from dotenv import load_dotenv
from flask import Flask

import redis

load_dotenv()  # loads variables from .env file into environment

db = redis.Redis('localhost')


def create_app():
    app = Flask(__name__)

    from .views import mijitel_view, redis_view

    app.register_blueprint(mijitel_view.bp)
    app.register_blueprint(redis_view.bp)

    return app
