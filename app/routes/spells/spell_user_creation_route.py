from flask import Blueprint

from app.controllers.spells import SpellUserCreationController

from app.routes.base_route import BaseRoute

class SpellUserCreationRoute(BaseRoute):
    def __init__(self):
        spell_user_creation_bp = Blueprint("spell_user_creation",__name__)
        
        super().__init__(spell_user_creation_bp,SpellUserCreationController())