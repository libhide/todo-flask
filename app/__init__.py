import os
from flask import Flask
from flask.ext.navigation import Navigation
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager

app = Flask(__name__)
app.config.from_object('config')
nav = Navigation(app)
db = SQLAlchemy(app)

lm = LoginManager()
lm.init_app(app)

from app import views, models
