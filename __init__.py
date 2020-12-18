from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_admin import Admin
import os
from flask_admin.contrib.sqla import ModelView

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = os.urandom(24)
# app.secret_key = os.urandom(24)
import psycopg2

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:beautifulQ@localhost:5432/world_in_spring'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'

db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = 'login_page'
db.init_app(app)
admin = Admin(app)
