from database import db


class User(db.Model):  # type: ignore
    uid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100), nullable=False)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.Integer, nullable=False)
    birthday = db.Column(db.Integer, nullable=False)  # timestamp

    __table_args__ = (db.CheckConstraint(gender.in_({0, 1})),)
