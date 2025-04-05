from flask import Blueprint

from app.controllers.spells import (
    SpellComponentsController,
    SpellController,
    SpellScalingController,
    SpellSchoolController,
    SpellStatsController,
    SpellUserCreationController
)

from app.routes.base_route import BaseRoute

# spell components
spell_components_bp = Blueprint("spell_components",__name__)
spell_components_route = BaseRoute(spell_components_bp,SpellComponentsController())

#spell
spell_bp = Blueprint("spell",__name__)
spell_route = BaseRoute(spell_bp,SpellController())

#spell scaling
spell_scaling_bp = Blueprint("spell_scaling",__name__)
spell_scaling_route = BaseRoute(spell_scaling_bp,SpellScalingController())

#spell school
spell_school_bp = Blueprint("spell_school",__name__)
spell_school_route = BaseRoute(spell_school_bp,SpellSchoolController())

#spell stats
spell_stats_bp = Blueprint("spell_stats",__name__)
spell_stats_route = BaseRoute(spell_stats_bp,SpellStatsController())

#spell user creation
spell_user_creation_bp = Blueprint("spell_user_creation",__name__)
spell_user_creation_route = BaseRoute(spell_user_creation_bp,SpellUserCreationController())