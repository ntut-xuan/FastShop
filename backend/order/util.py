from typing import Any

from database import db
from models import Item, ItemOfOrder, Order


def flatten_order_payload(payload: dict[str, Any]) -> dict[str, Any]:
    flat_payload: dict[str, Any] = {
        "date": payload["date"],
        "note": payload["note"],
        "delivery_address": payload["delivery_info"]["address"],
        "phone": payload["delivery_info"]["phone_number"],
    }
    return flat_payload


def add_order_of_user(user_id: int, fields_and_values: dict[str, Any]) -> int:
    """Adds a new order of the user specified by `user_id`.

    Args:
        user_id: The id of the user which the new order belongs to.
        fields_and_values: All the fields that are necessary for the record of
            table "order" with user_id excluded.

    Returns:
        The id of the new order.
    """
    new_order = Order(**fields_and_values)
    new_order.user_id = user_id
    db.session.add(new_order)
    db.session.flush()
    order_id: int = new_order.order_id
    db.session.commit()
    return order_id


def has_count_larger_than_available(item_ids_and_counts: list[dict[str, int]]) -> bool:
    """Returns whether there exist any count of item that is larger than the count in the "item" table."""
    id_to_count: dict[int, int] = {}
    for item_id_and_count in item_ids_and_counts:
        id_to_count[item_id_and_count["item_id"]] = item_id_and_count["count"]
    specified_items: list[Item] = (
        db.session.execute(db.select(Item).where(Item.id.in_(id_to_count.keys())))
        .scalars()
        .all()
    )
    return any(id_to_count[item.id] > item.count for item in specified_items)


def add_items_of_order(
    order_id: int, item_ids_and_counts: list[dict[str, int]]
) -> None:
    for item_id_and_count in item_ids_and_counts:
        db.session.add(
            ItemOfOrder(
                order_id=order_id,
                item_id=item_id_and_count["id"],
                count=item_id_and_count["count"],
            )
        )
    db.session.commit()
