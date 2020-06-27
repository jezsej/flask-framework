import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    #secret key configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-cant-touch-this'

    #Database connection
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///'+ os.path.join(basedir, 'app.db')

    #Database chaneg alerts
    SQLALCHEMY_TRACK_MODIFICATIONS = False