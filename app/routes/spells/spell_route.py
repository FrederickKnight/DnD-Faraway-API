from flask import Blueprint,request

from app.controllers.spells import SpellController

from app.routes.base_route import BaseRoute

class SpellRoute(BaseRoute):
    def __init__(self):
        spell_bp = Blueprint("spell",__name__)

        super().__init__(spell_bp,SpellController())
        
        self._add_routes()
        
    def _add_routes(self):
        
        @self._blueprint.route("/<int:id>/stats",methods=["GET"])
        def route_get_stats(id):
            return SpellController().controller_get_stats_from_id(id=id,request=request)
        
        @self._blueprint.route("/<int:id>/stats/components",methods=["GET"])
        def route_get_stats_components(id):
            return SpellController().controller_get_components_from_id(id=id,request=request)
        
        @self._blueprint.route("/<int:id>/stats/spell-school",methods=["GET"])
        def route_get_stats_spell_school(id):
            return SpellController().controller_get_spell_school_from_id(id=id,request=request)
        
        @self._blueprint.route("/<int:id>/stats/scaling",methods=["GET"])
        def route_get_stats_scaling(id):
            return SpellController().controller_get_scaling_from_id(id=id,request=request)