from uuid import uuid4

from flask_login import UserMixin
from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import validates
from werkzeug.security import generate_password_hash, check_password_hash

from flask_web import db
from flask_web import login
from flask_web.enums.Status import Status


@login.user_loader
def load_user(id):
    return User.query.get(int(id))

# TODO: Tests
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    external_id = db.Column(db.String(36), index=True, unique=True)
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __init__(self, email, first_name, last_name, plaintext_password):
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.password_hash = generate_password_hash(plaintext_password)

    def set_password(self, plaintext_password):
        self.password_hash = generate_password_hash(plaintext_password)

    @validates('email')
    def convert_lower(self, key, value):
        return value.lower()

    def __repr__(self):
        return '<User {} {}>'.format(self.first_name, self.last_name)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Stand(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    external_id = db.Column(db.String(36), index=True, unique=True)
    registration_id = db.Column(db.String(10), unique=True)
    name = db.Column(db.String(64))
    status = db.Column(db.String(64))
    status_date = db.Column(db.DateTime())
    history = relationship("StatusHistory", back_populates="stand")

    def __init__(self, name, current_date):
        self.external_id = str(uuid4())
        self.registration_id = str(uuid4().hex[:10])
        self.status = Status.low.value
        self.name = name
        self.status_date = current_date

    def add_history(self, status, status_date):
        history = StatusHistory(stand_id=self.id, status=status, status_date=status_date)
        self.history.append(history)

    def serialize(self):
        serialized_response = {
            "name": self.name,
            "status": self.status,
            "status_date": self.status_date.strftime("%Y-%m-%d %H:%M:%S"),
            "history": [x.serialize() for x in self.history]
        }

        return serialized_response

    def __repr__(self):
        return '<{} {} {} {} {} {} {}>'.format(self.id, self.external_id, self.registration_id, self.name, self.status, self.status_date, self.history)


class StatusHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    stand_id = db.Column(Integer, ForeignKey('stand.id'))
    stand = relationship("Stand", back_populates="history")
    status = db.Column(db.String(64))
    status_date = db.Column(db.DateTime())

    def __repr__(self):
        return '<{} {} {} {} {}>'.format(self.id, self.stand_id, self.stand, self.status, self.status_date)

    def serialize(self):
        serialized_response = {
            "status": self.status,
            "status_date": self.status_date.strftime("%Y-%m-%d %H:%M:%S")
        }

        return serialized_response