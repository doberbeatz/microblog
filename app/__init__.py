import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_openid import OpenID
from config import basedir

# Init Flask
app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

# Init LoginManager
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'

from app import views, models
