from tests import BaseTesting
import pytest

from .test_spell_components import TestSpellComponents
from .test_spell_scaling import TestSpellScaling

@pytest.mark.order(4)
class TestSpellStats(BaseTesting):
    def setup_class(self):        
        data = {
            "level":"int",
            "is_ritual":"bool",
            "casting_time":"int",
            "casting_action_type":"uuid",
            "casting_description":"uuid",
            "duration_time":"int",
            "duration_time_type":"uuid",
            "duration_type":"uuid",
            "range_distance":"uuid",
            "range_type":"uuid",
            "area_distance":"uuid",
            "area_type":"uuid",
            "id_spell_school": "id_model_spell-school",
            "id_components": ("id_model_spell-components",TestSpellComponents),
            "id_scaling": ("id_model_spell-scaling",TestSpellScaling)
        }
        super().setup_class(self,"api/spell-stats", data)