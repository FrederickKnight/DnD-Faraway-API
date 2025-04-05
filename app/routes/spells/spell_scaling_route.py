from flask import Blueprint,request

from app.controllers.spells.spell_scaling_controller import SpellScalingController

from app.routes.base_route import BaseRoute

spell_scaling_bp = Blueprint("spell_scaling",__name__)

spell_scaling_route = BaseRoute(spell_scaling_bp,SpellScalingController())