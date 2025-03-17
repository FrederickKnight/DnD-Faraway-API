from app.models import (
    SpellStats
)

from .base_controller import BaseController

class SpellStatsController(BaseController):
    def __init__(self):
        defaults = {
            "level":0,
            "is_ritual":0,
            "casting_time":None,
            "casting_action_type":None,
            "casting_description":None,
            "duration_time":None,
            "duration_time_type":None,
            "range_distance":None,
            "range_type":None,
            "area_distance":None,
            "area_type":None,
            "id_spell_school":None,
            "id_components":None,
            "id_scaling":None
        }
        super().__init__(SpellStats, defaults)
