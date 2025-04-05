from flask import Blueprint,request

from app.controllers.spells.spell_controller import SpellController

from app.routes.base_route import BaseRoute

spell_bp = Blueprint("spell",__name__)

spell_route = BaseRoute(spell_bp,SpellController())