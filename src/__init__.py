import sys
sys.path.append('../')
from .models import db
from flask import Flask
from .views import inventories, locations

# Creates the flask application
def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    app.register_blueprint(inventories.bp)
    app.register_blueprint(locations.bp)

    return app
