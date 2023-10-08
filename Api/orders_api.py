import logging

from flask import Blueprint, jsonify, abort, request
from sqlalchemy import update, select, delete
from data import db_session
from data.__all_models import Orders, Users, sql_order_to_json, list_sql_orders_to_json
import datetime

orders_api = Blueprint("orders_api", __name__)


@orders_api.route("/orders", methods=["GET"])
def get_orders():
    db_sess = db_session.create_session()
    orders = db_sess.execute(select(Orders)).scalars().fetchall()  # getting orders from db
    return jsonify({"orders": list_sql_orders_to_json(orders)})


@orders_api.route("/orders/<int:order_id>", methods=["GET"])
def get_order(order_id):
    db_sess = db_session.create_session()
    order = db_sess.execute(select(Orders).where(Orders.id == order_id)).scalars().first()  # getting orders from db
    if isinstance(order, type(None)):
        return abort(404)
    return jsonify({"order": sql_order_to_json(order)})


@orders_api.route("/orders/by_name/<string:order_name>", methods=["GET"])
def get_order_by_name(order_name):
    db_sess = db_session.create_session()
    order = db_sess.execute(
        select(Orders).where(Orders.name == order_name)).scalars().first()  # getting orders from db
    if isinstance(order, type(None)):
        return abort(404)
    return jsonify({"order": sql_order_to_json(order)})


@orders_api.route("/orders/by_id/<int:user_id>", methods=["GET"])
def get_orders_by_user_id(user_id):
    db_sess = db_session.create_session()
    user = db_sess.execute(select(Users).where(Users.id == user_id)).scalars().first()
    if isinstance(user, type(None)):
        return abort(404)
    orders = db_sess.execute(
        select(Orders).where(Orders.user_id == user_id)).scalars().first()  # getting orders from db
    return jsonify({"orders": list_sql_orders_to_json(orders)})


@orders_api.route("/orders/by_tg/<int:user_tg_id>", methods=["GET"])
def get_orders_by_user_tg(user_tg_id):
    db_sess = db_session.create_session()
    user_id = db_sess.execute(select(Users).where(Users.tg_id == user_tg_id)).scalars().first()
    if isinstance(user_id, type(None)):
        return abort(404)
    orders = db_sess.execute(
        select(Orders).where(Orders.user_id == user_id)).scalars().first()  # getting orders from db
    return jsonify({"orders": sql_order_to_json(orders)})


@orders_api.route("/orders", methods=["POST"])
def create_order():
    if not request.json:
        abort(400)
    db_sess = db_session.create_session()
    if "user_id" not in request.json and "user_tg_id" not in request.json:
        abort(400)
    if "name" not in request.json:
        abort(400)
    if "vk_group_id" not in request.json:
        abort(400)
    if "interval" not in request.json:
        abort(400)
    if "left_days" not in request.json:
        abort(400)
    if "last_post_id" not in request.json:
        abort(400)
    order2 = db_sess.execute(select(Orders).where(Orders.name == request.json["name"])).scalars().first()
    if not isinstance(order2, type(None)):
        return abort(413)
    user_id = None
    start_at = datetime.datetime.now()
    if "user_id" in request.json:
        user_id = request.json["user_id"]
        user = db_sess.execute(select(Users).where(Users.id == user_id)).scalars().first()
        if isinstance(user, type(None)):
            abort(400)
        orders_amount = db_sess.execute(select(Users.orders_amount).where(Users.id == user_id)).scalars().first()
        db_sess.execute(update(Users).values(orders_amount=orders_amount + 1))
        db_sess.commit()
    else:
        tg_id = request.json["user_tg_id"]
        user = db_sess.execute(select(Users).where(Users.tg_id == tg_id)).scalars().first()
        if isinstance(user, type(None)):
            abort(400)
        orders_amount = db_sess.execute(select(Users.orders_amount).where(Users.tg_id == tg_id)).scalars().first()
        db_sess.execute(update(Users).values(orders_amount=orders_amount + 1))
        db_sess.commit()
        user_id = db_sess.execute(select(Users.id).where(Users.tg_id == tg_id)).scalar()
    if "start_at" in request.json:
        start_at = request.json["start_at"]
    logging.warning(user_id)
    order = Orders(
        user_id=user_id,
        name=request.json["name"],
        vk_group_id=request.json["vk_group_id"],
        interval=request.json["interval"],
        left_days=request.json["left_days"],
        start_at=start_at,
        last_post_id=request.json["last_post_id"]
    )
    db_sess.add(order)  # add record into db
    db_sess.commit()
    return jsonify({"result": ["Success", {"created_order": sql_order_to_json(order)}]})


@orders_api.route("/orders/<int:order_id>", methods=["PUT"])
def update_order(order_id):
    db_sess = db_session.create_session()
    order = db_sess.execute(select(Orders).where(Orders.id == order_id)).scalars().first()  # getting orders from db
    if isinstance(order, type(None)):
        return abort(404)
    # update record in db
    if "user_id" in request.json:
        user_id = request.json["user_id"]
        user = db_sess.execute(select(Users).where(Users.id == user_id)).scalars().first()
        if isinstance(user, type(None)):
            return abort(400)
        orders_amount_prev_user = db_sess.execute(
            select(Users.orders_amount).where(Users.id == order.user_id)).scalars().first()
        orders_amount_new_user = db_sess.execute(
            select(Users.orders_amount).where(Users.id == user_id)).scalars().first()
        db_sess.execute(
            update(Users).where(Users.id == order.user_id).values(orders_amount=orders_amount_prev_user - 1))
        db_sess.execute(update(Users).where(Users.id == user_id).values(orders_amount=orders_amount_new_user + 1))
        db_sess.commit()
        order = db_sess.execute(update(Orders).where(Orders.id == order_id).values(user_id=user_id))
    if "name" in request.json:
        order2 = db_sess.execute(select(Orders).where(Orders.name == request.json["name"])).scalars().first()
        if not isinstance(order2, type(None)):
            return (413)
        order = db_sess.execute(update(Orders).where(Orders.id == order_id).values(name=request.json["name"]))
    if "vk_group_id" in request.json:
        order = db_sess.execute(
            update(Orders).where(Orders.id == order_id).values(vk_group_id=request.json["vk_group_id"]))
    if "interval" in request.json:
        order = db_sess.execute(update(Orders).where(Orders.id == order_id).values(interval=request.json["interval"]))
    if "left_days" in request.json:
        order = db_sess.execute(update(Orders).where(Orders.id == order_id).values(left_days=request.json["left_days"]))
    if "start_at" in request.json:
        order = db_sess.execute(update(Orders).where(Orders.id == order_id).values(start_at=request.json["start_at"]))
    if "last_post_id" in request.json:
        order = db_sess.execute(
            update(Orders).where(Orders.id == order_id).values(last_post_id=request.json["last_post_id"]))
    db_sess.commit()
    order = db_sess.execute(select(Orders).where(Orders.id == order_id)).scalars().first()
    return jsonify({"result": ["Success", {"updated_order": sql_order_to_json(order)}]})


@orders_api.route("/orders/<string:order_name>", methods=["PUT"])
def update_order_by_name(order_name):
    db_sess = db_session.create_session()
    order = db_sess.execute(select(Orders).where(Orders.name == order_name)).scalars().first()  # getting orders from db
    if isinstance(order, type(None)):
        return abort(404)
    name = order_name
    # update record in db
    if "user_id" in request.json:
        user_id = request.json["user_id"]
        user = db_sess.execute(select(Users).where(Users.id == user_id)).scalars().first()
        if isinstance(user, type(None)):
            return abort(400)
        orders_amount_prev_user = db_sess.execute(
            select(Users.orders_amount).where(Users.id == order.user_id)).scalars().first()
        orders_amount_new_user = db_sess.execute(
            select(Users.orders_amount).where(Users.id == user_id)).scalars().first()
        db_sess.execute(
            update(Users).where(Users.id == order.user_id).values(orders_amount=orders_amount_prev_user - 1))
        db_sess.execute(update(Users).where(Users.id == user_id).values(orders_amount=orders_amount_new_user + 1))
        db_sess.commit()
        order = db_sess.execute(update(Orders).where(Orders.name == name).values(user_id=user_id))
    if "name" in request.json and request.json["name"] != order_name:
        name = request.json["name"]
        order2 = db_sess.execute(select(Orders).where(Orders.name == name)).scalars().first()
        if not isinstance(order2, type(None)):
            return abort(413)
        order = db_sess.execute(update(Orders).where(Orders.name == order_name).values(name=name))
    if "vk_group_id" in request.json:
        order = db_sess.execute(
            update(Orders).where(Orders.name == order_name).values(vk_group_id=request.json["vk_group_id"]))
    if "interval" in request.json:
        order = db_sess.execute(
            update(Orders).where(Orders.name == order_name).values(interval=request.json["interval"]))
    if "left_days" in request.json:
        order = db_sess.execute(
            update(Orders).where(Orders.name == order_name).values(left_days=request.json["left_days"]))
    if "start_at" in request.json:
        order = db_sess.execute(
            update(Orders).where(Orders.name == order_name).values(start_at=request.json["start_at"]))
    if "last_post_id" in request.json:
        order = db_sess.execute(
            update(Orders).where(Orders.name == order_name).values(last_post_id=request.json["last_post_id"]))
    db_sess.commit()
    order = db_sess.execute(select(Orders).where(Orders.name == name)).scalars().first()
    return jsonify({"result": ["Success", {"updated_order": sql_order_to_json(order)}]})


@orders_api.route("/orders/<int:order_id>", methods=["DELETE"])
def delete_order(order_id):
    db_sess = db_session.create_session()
    order = db_sess.execute(select(Orders).where(Orders.id == order_id)).scalars().first()  # getting orders from db
    if isinstance(order, type(None)):
        return abort(404)
    # delete record from db
    db_sess.execute(delete(Orders).where(Orders.id == order_id))
    db_sess.commit()
    return jsonify({"result": "Success"})


@orders_api.route("/orders/by_name/<string:order_name>", methods=["DELETE"])
def delete_order_by_name(order_name):
    db_sess = db_session.create_session()
    order = db_sess.execute(select(Orders).where(Orders.name == order_name)).scalars().first()  # getting orders from db
    if isinstance(order, type(None)):
        return abort(404)
    # delete record from db
    db_sess.execute(delete(Orders).where(Orders.name == order_name))
    db_sess.commit()
    return jsonify({"result": "Success"})
