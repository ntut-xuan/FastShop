from database import db

from sqlalchemy.engine.default import DefaultExecutionContext


class User(db.Model):  # type: ignore
    uid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(1000), nullable=False)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.Integer, nullable=False)
    birthday = db.Column(db.Integer, nullable=False)  # timestamp

    __table_args__ = (db.CheckConstraint(gender.in_({0, 1})),)


class Tag(db.Model):  # type: ignore
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)


def same_as(column_name: str):
    def default_function(context: DefaultExecutionContext):
        return context.current_parameters.get(column_name)

    return default_function


class Item(db.Model):  # type: ignore
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    count = db.Column(db.Integer, default=0, nullable=False)
    original = db.Column(db.Integer, nullable=False)
    discount = db.Column(
        db.Integer, default=same_as("original"), nullable=False
    )  # price after discounted
    avatar = db.Column(db.String(36))  # 36 character long uuid

    __table_args__ = (db.CheckConstraint(count > 0),)


class TagOfItem(db.Model):  # type: ignore
    item_id = db.Column(
        db.ForeignKey(
            Item.id,
            ondelete="CASCADE",
            onupdate="CASCADE",
        ),
        primary_key=True,
    )
    tag_id = db.Column(
        db.ForeignKey(
            Tag.id,
            ondelete="CASCADE",
            onupdate="CASCADE",
        ),
        primary_key=True,
    )
