from flask import Blueprint

from app.controllers.spells import SpellComponentsController

from app.routes.base_route import BaseRoute

class SpellComponentsRoute(BaseRoute):
    def __init__(self):
        spell_components_bp = Blueprint("spell_components",__name__)
        
        super().__init__(spell_components_bp,SpellComponentsController())