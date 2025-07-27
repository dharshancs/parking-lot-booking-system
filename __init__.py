#app factory
from flask import Flask
from controllers.base_views import u_view
from controllers.user_page import user_view
from controllers.admin_page import admin_view
from models.config import initialize_table


def create_app():
    app = Flask(__name__)
    app.jinja_env.globals.update(int=int)
    app.secret_key = 'dharshan'

    initialize_table()
    app.register_blueprint(u_view)
    app.register_blueprint(user_view)
    app.register_blueprint(admin_view)
    return app