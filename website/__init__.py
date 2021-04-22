import os
import sys
from flask import Flask
from flask_assets import Environment, Bundle
from flask_caching import Cache
from flask_compress import Compress
from flask_restful import Api
from flask_cors import CORS

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
api = Api()
cache = Cache()
cors = CORS(resources=r'/api/*',
            origins='*',
            support_credentials=True,
            expose_headers='authorization')

assets = Environment()
compress = Compress()


def register_master_assets():
    all_js = Bundle('js/vue-build.js', output="main_bundle.js")
    assets.register('main_js', all_js)


def init_views(app):
    api_prefix = '/api/v1'
    from website.views import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    from website.braintree_payments.ep_braintree import braintree_bp
    app.register_blueprint(braintree_bp, url_prefix=api_prefix)
    
def create_app(config_name=None):
    app = Flask(__name__)
    with app.app_context():
        app.config.from_object('website.config.DevelopmentConfig')
        init_views(app=app)
        cache.init_app(app)
        assets.init_app(app)
        compress.init_app(app)
        cors.init_app(app)
        register_master_assets()
        return app
