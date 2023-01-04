import enum

from database import db


class User(db.Model):  # type: ignore[name-defined]
    uid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(1000), nullable=False)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.Integer, nullable=False)
    birthday = db.Column(db.Integer, nullable=False)  # timestamp

    __table_args__ = (db.CheckConstraint(gender.in_({0, 1})),)


class Tag(db.Model):  # type: ignore[name-defined]
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), unique=True)


def same_as(column_name: str):
    def default_function(context):
        # context seems to be in type "sqlalchemy.engine.default.DefaultExecutionContext"
        # from the doc, but mypy says no
        # See https://docs.sqlalchemy.org/en/20/core/internals.html#sqlalchemy.engine.default.DefaultExecutionContext.current_parameters
        return context.current_parameters.get(column_name)

    return default_function


class Item(db.Model):  # type: ignore[name-defined]
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    count = db.Column(db.Integer, default=0, nullable=False)
    description = db.Column(db.Text)
    original = db.Column(db.Integer, nullable=False)
    discount = db.Column(
        db.Integer, default=same_as("original"), nullable=False
    )  # price after discounted
    avatar = db.Column(db.String(36))  # 36 character long uuid

    __table_args__ = (db.CheckConstraint(count > 0),)


class TagOfItem(db.Model):  # type: ignore[name-defined]
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


class ShoppingCart(db.Model):  # type: ignore[name-defined]
    user_id = db.Column(
        db.ForeignKey(User.uid, ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True,
    )
    item_id = db.Column(
        db.ForeignKey(Item.id, ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True,
    )
    count = db.Column(db.Integer, nullable=False)

    __table_args__ = (db.CheckConstraint(count > 0),)


@enum.unique
class OrderStatus(enum.Enum):
    CANCEL = enum.auto()
    CHECKING = enum.auto()
    OK = enum.auto()


@enum.unique
class DeliveryStatus(enum.Enum):
    DELIVERED = enum.auto()
    DELIVERING = enum.auto()
    PENDING = enum.auto()
    SKIP = enum.auto()


class Order(db.Model):  # type: ignore[name-defined]
    order_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(
        db.ForeignKey(User.uid, ondelete="CASCADE", onupdate="CASCADE"), nullable=False
    )
    date = db.Column(db.Integer, nullable=False)
    order_status = db.Column(db.Enum(OrderStatus), nullable=False)
    delivery_status = db.Column(db.Enum(DeliveryStatus), nullable=False)
    delivery_address = db.Column(db.Text, nullable=False)
    note = db.Column(db.Text)
    phone = db.Column(db.String(10), nullable=False)


class ItemOfOrder(db.Model):  # type: ignore[name-defined]
    """The records in the ShoppingCart are moved to this table when a new order is made from the cart."""

    order_id = db.Column(
        db.ForeignKey(Order.order_id, ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True,
    )
    item_id = db.Column(
        db.ForeignKey(Item.id, ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True,
    )
    count = db.Column(db.Integer, nullable=False)

    __table_args__ = (db.CheckConstraint(count > 0),)
