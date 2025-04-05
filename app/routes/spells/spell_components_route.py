from flask import Blueprint

from app.controllers.spells.spell_components_controller import SpellComponentsController

from app.routes.base_route import BaseRoute

spell_components_bp = Blueprint("spell_components",__name__)

spell_components_route = BaseRoute(spell_components_bp,SpellComponentsController())