from flask import Blueprint,request

from app.controllers.spells.spell_components_controller import SpellComponentsController

spell_components_bp = Blueprint("spell_components",__name__)

@spell_components_bp.route("/",methods=["GET"])
def get_all_spell():
    return SpellComponentsController().controller_get_all()

@spell_components_bp.route("/add",methods=["POST"])
def add_spell():
    json_request = request.get_json()
    return SpellComponentsController().controller_register(json_request)

@spell_components_bp.route("/update",methods=["PUT"])
def update_spell():
    json_request = request.get_json()
    return SpellComponentsController().controller_update(data=json_request)

@spell_components_bp.route("/<int:id>/update",methods=["PUT"])
def update_by_id_spell(id):
    json_request = request.get_json()
    return SpellComponentsController().controller_update(id=id,data=json_request)

@spell_components_bp.route("/<int:id>/delete",methods=["DELETE"])
def delete_spell(id):
    return SpellComponentsController().controller_delete(id)

@spell_components_bp.route("/<int:id>",methods=["GET"])
def get_by_id_spell(id):
    return SpellComponentsController().controller_get_by_id(id)