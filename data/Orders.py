import datetime
import sqlalchemy
from sqlalchemy import orm
from data.db_session import SqlAlchemyBase


class Orders(SqlAlchemyBase):
    __tablename__ = 'orders'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False, index=True, unique=True)
    vk_group_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    interval = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    left_days = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    start_at = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now())
    last_post_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)

    user = orm.relationship('Users')


def sql_order_to_json(order: Orders) -> dict:
    jsonify = {
        "id": order.id,
        "name": order.name,
        "user_id": order.user_id,
        "vk_group_id": order.vk_group_id,
        "interval": order.interval,
        "left_days": order.left_days,
        "start_at": order.start_at,
        "last_post_id": order.last_post_id,
    }
    return jsonify


def list_sql_orders_to_json(orders: list) -> list:
    jsonify_orders = []
    for order in orders:
        jsonify_orders.append(sql_order_to_json(order))
    return jsonify_orders
