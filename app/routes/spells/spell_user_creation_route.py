from flask import Blueprint,request

from app.controllers.spells.spell_user_creation_controller import SpellUserCreationController

spell_user_creation_bp = Blueprint("spell_user_creation",__name__)

@spell_user_creation_bp.route("/",methods=["GET"])
def get_all_spell_creation():
    return SpellUserCreationController().controller_get_all()

@spell_user_creation_bp.route("/add",methods=["POST"])
def add_spell_creation():
    json_request = request.get_json()
    return SpellUserCreationController().controller_register(json_request)

@spell_user_creation_bp.route("/update",methods=["PUT"])
def update_spell_creation():
    json_request = request.get_json()
    return SpellUserCreationController().controller_update(data=json_request)

@spell_user_creation_bp.route("/<int:id>/update",methods=["PUT"])
def update_by_id_spell_creation(id):
    json_request = request.get_json()
    return SpellUserCreationController().controller_update(id=id,data=json_request)

@spell_user_creation_bp.route("/<int:id>/delete",methods=["DELETE"])
def delete_spell_creation(id):
    return SpellUserCreationController().controller_delete(id)

@spell_user_creation_bp.route("/<int:id>",methods=["GET"])
def get_by_id_spell_creation(id):
    return SpellUserCreationController().controller_get_by_id(id)