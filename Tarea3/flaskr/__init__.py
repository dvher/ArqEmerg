import os

from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv

def create_app(test_config=None):

    load_dotenv('.env')

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY', default='dev'),
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    CORS(app, resources={r"/api/*": {"origins": "*"}})

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db
    db.init_app(app)

    from . import api
    app.register_blueprint(api.v1)

    from . import api_admin
    app.register_blueprint(api_admin.v1_adm)

    return app
