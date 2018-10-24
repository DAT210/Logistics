import os
class Config:
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database/developDB.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProductionConfig(Config):
    # Will be changed when MySQL is implemented
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database/developDB.db'

    SECRET_KEY = os.environ.get('INV_SECRET_KEY', default=None)
    if not SECRET_KEY:
        raise ValueError('No secret key set, check enviroment variable in os')

class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    SECRET_KEY = 'develop'

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database/testDB'
    SECRET_KEY = 'testing'
