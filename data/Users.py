from dataclasses import dataclass
import sqlalchemy
from data.db_session import SqlAlchemyBase


class Users(SqlAlchemyBase):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    tg_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=False, unique=True, index=True)
    orders_amount = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    is_VIP = sqlalchemy.Column(sqlalchemy.Boolean, default=False)


def sql_user_to_json(user: Users):
    jsonify = {
        "id": user.id,
        "tg_id": user.tg_id,
        "orders_amount": user.orders_amount,
        "is_VIP": user.is_VIP
    }
    return jsonify


def list_sql_users_to_json(users: list) -> list:
    jsonify_users = []
    for user in users:
        jsonify_users.append(sql_user_to_json(user))
    return jsonify_users
