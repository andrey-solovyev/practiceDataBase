from flask_login import UserMixin, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
import psycopg2
from __init__ import db, login_manager


class UserSite(db.Model, UserMixin):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(100))
    password_hash = db.Column(db.String(100))
    role = db.Column(db.Integer, default=0)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Human(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    surname = db.Column(db.String(100))
    name = db.Column(db.String(30), nullable=False)
    middle_name = db.Column(db.String(30))
    date_of_birth = db.Column(db.DateTime())
    passport_data = db.Column(db.String(255), nullable=False)
    residence_address = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(60), nullable=False)


class Construction_position(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    number = db.Column(db.Integer)
    address = db.Column(db.String(255), nullable=False)


class Construction(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    position_id = db.Column(db.Integer, db.ForeignKey('construction.id'))
    type_build_id = db.Column(db.Integer)
    date_fundament = db.Column(db.DateTime)
    number_of_flats = db.Column(db.Integer)
    date_of_delivery = db.Column(db.DateTime)
    date_actual_delivery = db.Column(db.DateTime)
    heating = db.Column(db.Boolean)
    gas = db.Column(db.Boolean)


class Type_building(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    material = db.Column(db.String(30), nullable=False)


class Flat(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    construction_id = db.Column(db.Integer, db.ForeignKey('construction.id'))
    number_flat = db.Column(db.Integer)
    count_flat = db.Column(db.Integer)


class Plan_floor(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    construction_id = db.Column(db.Integer, db.ForeignKey('construction.id'))
    file_name = db.Column(db.String(255), nullable=False)


class Stage(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    construction_id = db.Column(db.Integer, db.ForeignKey('construction.id'))
    data_stage = db.Column(db.DateTime)
    description = db.Column(db.Text)


class Contract(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    human_id = db.Column(db.Integer, db.ForeignKey('human.id'))
    flat_id = db.Column(db.Integer, db.ForeignKey('flat.id'))
    date_contract = db.Column(db.DateTime)
    surname_employee = db.Column(db.String(255))
    downpayment = db.Column(db.Float)


@login_manager.user_loader
def load_user(user_id):
    return UserSite.query.get(user_id)
