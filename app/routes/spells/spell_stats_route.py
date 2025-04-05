from flask import Blueprint,request

from app.controllers.spells.spell_stats_controller import SpellStatsController

from app.routes.base_route import BaseRoute

spell_stats_bp = Blueprint("spell_stats",__name__)

spell_stats_route = BaseRoute(spell_stats_bp,SpellStatsController())