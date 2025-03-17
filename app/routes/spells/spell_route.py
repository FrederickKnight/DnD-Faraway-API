from flask import Blueprint,request

from app.controllers.spells.spell_controller import SpellController

spell_bp = Blueprint("spell",__name__)


@spell_bp.route("/",methods=["GET"])
def get_all_spell():
    return SpellController().controller_get_all()

@spell_bp.route("/add",methods=["POST"])
def add_spell():
    json_request = request.get_json()
    return SpellController().controller_register(json_request)

@spell_bp.route("/update",methods=["PUT"])
def update_spell():
    json_request = request.get_json()
    return SpellController().controller_update(data=json_request)

@spell_bp.route("/<int:id>/update",methods=["PUT"])
def update_by_id_spell(id):
    json_request = request.get_json()
    return SpellController().controller_update(id=id,data=json_request)

@spell_bp.route("/<int:id>/delete",methods=["DELETE"])
def delete_spell(id):
    return SpellController().controller_delete(id)

@spell_bp.route("/<int:id>",methods=["GET"])
def get_by_id_spell(id):
    return SpellController().controller_get_by_id(id)