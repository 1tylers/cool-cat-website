# import flask
from flask import Flask

def create_app():
    app = Flask(__name__)

    app.secret_key = ('')

    from .views import views

    app.register_blueprint(views, url_prefix='/')

    app.debug = False

    return app


