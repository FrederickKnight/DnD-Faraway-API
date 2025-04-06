from flask import Blueprint

from app.controllers.spells import SpellScalingController

from app.routes.base_route import BaseRoute

class SpellScalingRoute(BaseRoute):
    def __init__(self):
        spell_scaling_bp = Blueprint("spell_scaling",__name__)
        
        super().__init__(spell_scaling_bp,SpellScalingController())