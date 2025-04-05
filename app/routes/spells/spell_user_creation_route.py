from flask import Blueprint,request

from app.controllers.spells.spell_user_creation_controller import SpellUserCreationController

from app.routes.base_route import BaseRoute

spell_user_creation_bp = Blueprint("spell_user_creation",__name__)

spell_user_creation_route = BaseRoute(spell_user_creation_bp,SpellUserCreationController())