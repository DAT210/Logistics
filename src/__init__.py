import sys, os
sys.path.append('../')
from .models import db
from flask import Flask
from .views import ingredients, locations, web
import pymysql
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager

load_dotenv("../.env")

# Creates the flask application
def create_app(env):
    app = Flask(__name__, instance_relative_config=True)
    if env == 'dev':
        app.config['DEVELOPMENT'] = True
        app.config['DEBUG'] = True
        app.config['SECRET_KEY'] = 'develop'
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/developDB.db'
    
    elif env == 'test':
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/testDB'
        app.config['SECRET_KEY'] = 'testing'
    
    elif env == 'prod':
        # Checks if essential enviroment variables are set
        SECRET_KEY = os.environ.get('SECRET_KEY', default=None)
        if not SECRET_KEY:
            raise ValueError('No secret key set, check enviroment variable in os')
        db_username = os.environ.get('DB_USERNAME', default=None)
        if not db_username:
            raise ValueError('No username detected for database, check enviroment variable in os')
        db_pass = os.environ.get('DB_PASS', default=None)
        if not db_pass:
            raise ValueError('No password detected for database, check enviroment variable in os')

        app.config['SECRET_KEY'] = SECRET_KEY
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://' + db_username + ':' + db_pass + '@logistics_mysql/inventory'
    
    else:
        raise ValueError('No valid enviroment input')
    
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    app.config['JWT_SECRET_KEY'] = os.environ.get('SECRET_KEY', default="testing")
    jwt = JWTManager(app)

    app.register_blueprint(ingredients.bp)
    app.register_blueprint(locations.bp)
    app.register_blueprint(web.bp)

    return app
