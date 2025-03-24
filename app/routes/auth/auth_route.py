from flask import Blueprint,request

from app.auth import (
    register_user,
    get_by_id,
    validate_user,
    delete_user_by_id,
    generateSessionToken,
    createSessionToken,
    validateSessionToken,
    invalidateSession
)

auth_bp = Blueprint("auth",__name__)

@auth_bp.route("/register",methods=["POST"])
def route_register_user():
    json_request = request.get_json()
    return register_user(json_request)

@auth_bp.route("/<int:id>/search",methods=["GET"])
def route_get_by_id_user(id):
    return get_by_id(id)

@auth_bp.route("/user-validation",methods=["POST"])
def route_user_validation_user():
    json_request = request.get_json()
    return validate_user(json_request)

@auth_bp.route("/<int:id>/delete",methods=["DELETE"])
def route_delete_by_id(id):
    return delete_user_by_id(id)

@auth_bp.route("/session-token",methods=["GET"])
def route_session_token():
    return generateSessionToken()

@auth_bp.route("/create-session/<int:id>",methods=["POST"])
def route_test_user(id):
    json_request = request.get_json()
    return createSessionToken(json_request,id)

@auth_bp.route("/session-validation",methods=["POST"])
def route_test_validation_user():
    json_request = request.get_json()
    return validateSessionToken(json_request["token"])

@auth_bp.route("/session-invalidation",methods=["POST"])
def route_test_invalidation_user():
    json_request = request.get_json()
    return invalidateSession(json_request["session"])