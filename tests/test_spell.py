from tests import BaseTesting
import pytest

from .test_spell_stats import TestSpellStats


@pytest.mark.order(5)
class TestSpell(BaseTesting):
    def setup_class(self):        
        data = {
            "name":"uuid",
            "version":"version",
            "is_homebrew":"bool",
            "description":"uuid",
            "id_stats" : ("id_model_stats",TestSpellStats)
        }
        super().setup_class(self,"api/spell", data)