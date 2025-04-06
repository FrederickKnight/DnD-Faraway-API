from flask import Blueprint

from app.controllers.spells import SpellStatsController

from app.routes.base_route import BaseRoute

class SpellStatsRoute(BaseRoute):
    def __init__(self):
        spell_stats_bp = Blueprint("spell_stats",__name__)
        
        super().__init__(spell_stats_bp,SpellStatsController())