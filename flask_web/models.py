from flask_web import db


class Stand(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    external_id = db.Column(db.String(36), index=True, unique=True)
    registration_id = db.Column(db.String(10))
    name = db.Column(db.String(64))

    def __repr__(self):
        return '<Stand {} {}>'.format(self.registration_id, self.name)
