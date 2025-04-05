from flask import Blueprint

from app.controllers.spells.spell_school_controller import SpellSchoolController

from app.routes.base_route import BaseRoute

spell_school_bp = Blueprint("spell_school",__name__)

spell_school_route = BaseRoute(spell_school_bp,SpellSchoolController())