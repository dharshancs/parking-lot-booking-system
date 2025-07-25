#app factory
from flask import Flask
from controllers.views import view
from models.config import initialize_table


def create_app():
    app = Flask(__name__)

    initialize_table()
    app.register_blueprint(view)

    return app