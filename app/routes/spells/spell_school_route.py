from flask import Blueprint

from app.controllers.spells import SpellSchoolController

from app.routes.base_route import BaseRoute

class SpellSchoolRoute(BaseRoute):
    def __init__(self):
        spell_school_bp = Blueprint("spell_school",__name__)
        
        super().__init__(spell_school_bp,SpellSchoolController())