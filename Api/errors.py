from flask import Blueprint, jsonify, make_response

errors = Blueprint("errors", __name__)


@errors.errorhandler(404)
def not_found(error):
    return make_response(jsonify({"error": "Not found"}), 404)


@errors.errorhandler(400)
def not_found(error):
    return make_response(jsonify({"error": "Bad request"}), 400)

@errors.errorhandler(409)
def alredy_exist(error):
    return make_response(jsonify({"error": "Already exist"}), 409)