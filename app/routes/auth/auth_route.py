from flask import Blueprint,request

from app.controllers.auth.auth_controller import AuthControllerUser

auth_user_bp = Blueprint("auth_user",__name__)

# @auth_user_bp.route("/",methods=["GET"])
# def get_all_user():
#     return AuthControllerUser().controller_get_all()

@auth_user_bp.route("/register",methods=["POST"])
def add_user():
    json_request = request.get_json()
    return AuthControllerUser().controller_register(json_request)

@auth_user_bp.route("/update",methods=["PUT"])
def update_user():
    json_request = request.get_json()
    return AuthControllerUser().controller_update(data=json_request)

@auth_user_bp.route("/<int:id>/update",methods=["PUT"])
def update_by_id_user(id):
    json_request = request.get_json()
    return AuthControllerUser().controller_update(id=id,data=json_request)

@auth_user_bp.route("/<int:id>/delete",methods=["DELETE"])
def delete_user(id):
    return AuthControllerUser().controller_delete(id)

@auth_user_bp.route("/<int:id>",methods=["GET"])
def get_by_id_user(id):
    return AuthControllerUser().controller_get_by_id(id)

@auth_user_bp.route("/authenticate",methods=["POST"])
def auth_user():
    json_request = request.get_json()
    return AuthControllerUser().controller_authenticate(json_request)

