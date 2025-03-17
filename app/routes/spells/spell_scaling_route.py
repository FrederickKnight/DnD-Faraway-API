from flask import Blueprint,request

from app.controllers.spells.spell_scaling_controller import SpellScalingController

spell_scaling_bp = Blueprint("spell_scaling",__name__)

@spell_scaling_bp.route("/",methods=["GET"])
def get_all_spell():
    return SpellScalingController().controller_get_all()

@spell_scaling_bp.route("/add",methods=["POST"])
def add_spell():
    json_request = request.get_json()
    return SpellScalingController().controller_register(json_request)

@spell_scaling_bp.route("/update",methods=["PUT"])
def update_spell():
    json_request = request.get_json()
    return SpellScalingController().controller_update(data=json_request)

@spell_scaling_bp.route("/<int:id>/update",methods=["PUT"])
def update_by_id_spell(id):
    json_request = request.get_json()
    return SpellScalingController().controller_update(id=id,data=json_request)

@spell_scaling_bp.route("/<int:id>/delete",methods=["DELETE"])
def delete_spell(id):
    return SpellScalingController().controller_delete(id)

@spell_scaling_bp.route("/<int:id>",methods=["GET"])
def get_by_id_spell(id):
    return SpellScalingController().controller_get_by_id(id)