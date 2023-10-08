from flask import Blueprint, jsonify, abort, request
from sqlalchemy import update, select, delete, exists
from pyparsing import unicode
from data.__all_models import Users, Orders, sql_user_to_json, list_sql_users_to_json
import logging

from data import db_session

users_api = Blueprint("users_api", __name__)


@users_api.route("/users", methods=["GET"])
def get_users():
    db_sess = db_session.create_session()
    users = db_sess.execute(select(Users)).scalars().fetchall()  # getting orders from db
    logging.warning(users)
    return jsonify({"users": list_sql_users_to_json(users)})


@users_api.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    db_sess = db_session.create_session()
    user = db_sess.execute(select(Users).where(Users.id == user_id)).scalars().first()  # getting orders from db
    if isinstance(user, type(None)):
        return abort(404)
    logging.warning(sql_user_to_json(user))
    return jsonify({"user": sql_user_to_json(user)})


@users_api.route("/users/by_tg/<int:user_tg_id>", methods=["GET"])
def get_user_by_tg(user_tg_id):
    db_sess = db_session.create_session()
    user = db_sess.execute(select(Users).where(Users.tg_id == user_tg_id)).scalars().first()  # getting orders from db
    if isinstance(user, type(None)):
        return abort(404)
    logging.warning(sql_user_to_json(user))
    return jsonify({"user": sql_user_to_json(user)})


@users_api.route("/users", methods=["Post"])
def create_user():
    if not request.json:
        abort(400)
    db_sess = db_session.create_session()
    if "tg_id" not in request.json:
        abort(400)
    tg_id = request.json["tg_id"]
    if db_sess.execute(select(Users).where(Users.tg_id == tg_id)).scalars().first() is not None:
        abort(413)
    user = Users(tg_id=tg_id)
    db_sess.add(user)  # add record into db
    db_sess.commit()

    return jsonify({"result": ["Success", {"created_user": sql_user_to_json(user)}]})


@users_api.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    if not request.json:
        abort(400)
    db_sess = db_session.create_session()
    user = db_sess.execute(select(Users).where(Users.id == user_id)).scalars().first()
    if isinstance(user, type(None)):
        return abort(404)
    if "tg_id" in request.json:
        user2 = db_sess.execute(select(Users).where(Users.tg_id == request.json["tg_id"])).scalars().first()
        if not isinstance(user2, type(None)):
            return abort(413)
        user = db_sess.execute(update(Users).where(Users.id == user_id).values(tg_id=request.json["tg_id"]))
    if "orders_amount" in request.json:
        user = db_sess.execute(
            update(Users).where(Users.id == user_id).values(orders_amount=request.json["orders_amount"]))
    if "is_VIP" in request.json and type(request.json['is_VIP']) != unicode:
        user = db_sess.execute(update(Users).where(Users.id == user_id).values(is_VIP=request.json["is_VIP"]))
    db_sess.commit()
    user = db_sess.execute(select(Users).where(Users.id == user_id)).scalars().first()
    # update record in db
    return jsonify({"result": ["Success", {"updated_user": sql_user_to_json(user)}]})


@users_api.route("/users/by_tg/<int:user_tg_id>", methods=["PUT"])
def update_user_by_tg(user_tg_id):
    if not request.json:
        abort(400)
    db_sess = db_session.create_session()
    user = db_sess.execute(select(Users).where(Users.tg_id == user_tg_id)).scalars().first()
    if isinstance(user, type(None)):
        return abort(404)
    if "tg_id" in request.json:
        user2 = db_sess.execute(select(Users).where(Users.tg_id == request.json["tg_id"])).scalars().first()
        if not isinstance(user2, type(None)):
            return abort(413)
        user = db_sess.execute(update(Users).where(Users.tg_id == user_tg_id).values(tg_id=request.json["tg_id"]))
    if "orders_amount" in request.json:
        user = db_sess.execute(
            update(Users).where(Users.tg_id == user_tg_id).values(orders_amount=request.json["orders_amount"]))
    if "is_VIP" in request.json and type(request.json['is_VIP']) != unicode:
        user = db_sess.execute(update(Users).where(Users.tg_id == user_tg_id).values(is_VIP=request.json["is_VIP"]))
    db_sess.commit()
    user = db_sess.execute(select(Users).where(Users.tg_id == user_tg_id)).scalars().first()
    # update record in db
    return jsonify({"result": ["Success", {"updated_user": sql_user_to_json(user)}]})


@users_api.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    db_sess = db_session.create_session()
    user = db_sess.execute(select(Users).where(Users.id == user_id)).scalars().first()  # getting orders from db
    if isinstance(user, type(None)):
        return abort(404)
    # delete record from db
    db_sess.execute(delete(Orders).where(Orders.user_id == user_id))
    db_sess.execute(delete(Users).where(Users.id == user_id))
    db_sess.commit()
    return jsonify({"result": "Success"})


@users_api.route("/users/by_tg/<int:user_tg_id>", methods=["DELETE"])
def delete_user_by_tg(user_tg_id):
    db_sess = db_session.create_session()
    user_id = db_sess.execute(
        select(Users.id).where(Users.tg_id == user_tg_id)).scalars().first()  # getting orders from db
    if isinstance(user_id, type(None)):
        return abort(404)
    # delete record from db
    db_sess.execute(delete(Orders).where(Orders.user_id == user_id))
    db_sess.execute(delete(Users).where(Users.id == user_id))
    db_sess.commit()
    return jsonify({"result": "Success"})
