from flask import Blueprint,request

from app.controllers.spells.spell_stats_controller import SpellStatsController

spell_stats_bp = Blueprint("spell_stats",__name__)


@spell_stats_bp.route("/",methods=["GET"])
def get_all_spell_stats():
    return SpellStatsController().controller_get_all()

@spell_stats_bp.route("/add",methods=["POST"])
def add_spell_stats():
    json_request = request.get_json()
    return SpellStatsController().controller_register(json_request)

@spell_stats_bp.route("/update",methods=["PUT"])
def update_spell_stats():
    json_request = request.get_json()
    return SpellStatsController().controller_update(data=json_request)

@spell_stats_bp.route("/<int:id>/update",methods=["PUT"])
def update_by_id_spell_stats(id):
    json_request = request.get_json()
    return SpellStatsController().controller_update(id=id,data=json_request)

@spell_stats_bp.route("/<int:id>/delete",methods=["DELETE"])
def delete_spell_stats(id):
    return SpellStatsController().controller_delete(id)

@spell_stats_bp.route("/<int:id>",methods=["GET"])
def get_by_id_spell_stats(id):
    return SpellStatsController().controller_get_by_id(id)