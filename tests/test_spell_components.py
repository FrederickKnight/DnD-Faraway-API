from tests import BaseTesting
import pytest

@pytest.mark.order(2)
class TestSpellComponents(BaseTesting):
    def setup_class(self):        
        data = {
            "verbal":"bool",
            "somantic":"bool",
            "material":"bool",
            "special":"bool",
            "description":"uuid"
        }
        super().setup_class(self,"api/spell-components", data)