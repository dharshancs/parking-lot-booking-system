#app factory
from flask import Flask
from controllers.basic_views import b_view
from controllers.user_views import u_view
from models.config import initialize_table


def create_app():
    app = Flask(__name__)

    initialize_table()
    app.register_blueprint(b_view)
    app.register_blueprint(u_view)
    return app