from datetime import datetime
from sqlalchemy import Integer, ForeignKey
from flask_web import db
from uuid import uuid4
from flask_web.enums.Status import Status


class Stand(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    external_id = db.Column(db.String(36), index=True, unique=True)
    registration_id = db.Column(db.String(10), unique=True)
    name = db.Column(db.String(64))
    status = db.Column(db.String(64))
    status_date = db.Column(db.DateTime())

    def __init__(self, name):
        self.external_id = str(uuid4())
        self.registration_id = str(uuid4().hex[:10])
        self.status = Status.low.value
        self.name = name
        self.status_date = datetime.now()

    def serialize(self):
        return {
            "name": self.name,
            "status": self.status,
            "status_date": self.status_date.strftime("%Y-%m-%d %H:%M:%S")
        }


class StatusHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    stand_id = db.Column(Integer, ForeignKey('stand.id'))
    status = db.Column(db.String(64))
    status_date = db.Column(db.DateTime())
