from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_admin import *
from flask_migrate import Migrate
from flask_admin.contrib.sqla import ModelView
from ModelsDataBase import *
import os

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = os.urandom(24)
# app.secret_key = os.urandom(24)
import psycopg2

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:beautifulQ@localhost:5432/world_in_spring'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['ORDERS'] = '/Orders.xlsx'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
admin = Admin(app)
admin.add_view(ModelView(User_Site, db.session))
login_manager = LoginManager(app)
login_manager.login_view = 'login'
db.init_app(app)

