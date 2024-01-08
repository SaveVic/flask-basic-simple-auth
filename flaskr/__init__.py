import os
from flask import Flask, render_template, g
from flaskr.service.session import load_from_session
from werkzeug.exceptions import HTTPException


def create_app(test_config=None) -> Flask:
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite')
    )

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from .blueprint import api
    app.register_blueprint(api.bp)

    from .blueprint import auth
    app.register_blueprint(auth.bp)

    @app.before_request
    def load_user():
        load_from_session()

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.errorhandler(HTTPException)
    def handle_exception(e: HTTPException):
        g.error = e
        return render_template('error.html')

    return app
