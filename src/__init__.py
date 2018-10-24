import sys, os
sys.path.append('../')
from .models import db
from flask import Flask
from .views import ingredients, locations

# Creates the flask application
def create_app(env):
    app = Flask(__name__, instance_relative_config=True)
    # Change the login to use enviroment variables for db and secret key
    
    if env == 'dev':
        app.config.from_object('src.config.DevelopmentConfig')
    elif env == 'test':
        app.config.from_object('src.config.TestingConfig')
    elif env == 'prod':
        app.config.from_object('src.config.ProductionConfig')
    else:
        raise ValueError('No valid enviroment input')
    
    db.init_app(app)

    app.register_blueprint(ingredients.bp)
    app.register_blueprint(locations.bp)

    return app
