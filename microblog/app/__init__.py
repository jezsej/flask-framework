from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app =  Flask(__name__)
#add configuration file to app
app.config.from_object(Config)

#instantiate the application db
db = SQLAlchemy(app)
migrate = Migrate(app, db)

#Login logic for the app
login = LoginManager(app)
login.login_view = 'login'

from app import routes, models