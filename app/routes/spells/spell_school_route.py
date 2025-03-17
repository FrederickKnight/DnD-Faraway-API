from flask import Blueprint,request


from app.controllers.spells.spell_school_controller import SpellSchoolController

spell_school_bp = Blueprint("spell_school",__name__)


@spell_school_bp.route("/",methods=["GET"])
def get_all_spell_school():
    return SpellSchoolController().controller_get_all()

@spell_school_bp.route("/add",methods=["POST"])
def add_spell_school():
    json_request = request.get_json()
    return SpellSchoolController().controller_register(json_request)

@spell_school_bp.route("/update",methods=["PUT"])
def update_spell_school():
    json_request = request.get_json()
    return SpellSchoolController().controller_update(data=json_request)

@spell_school_bp.route("/<int:id>/update",methods=["PUT"])
def update_by_id_spell_school(id):
    json_request = request.get_json()
    return SpellSchoolController().controller_update(id=id,data=json_request)


@spell_school_bp.route("/<int:id>/delete",methods=["DELETE"])
def delete_spell_school(id):
    return SpellSchoolController().controller_delete(id=id)

@spell_school_bp.route("/<int:id>",methods=["GET"])
def get_by_id_spell_school(id):
    return SpellSchoolController().controller_get_by_id(id=id)