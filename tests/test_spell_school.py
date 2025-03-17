from tests import BaseTesting
import pytest

@pytest.mark.order(1)
class TestSpellShool(BaseTesting):
    def setup_class(self):        
        data = {
            "description": "uuid",
            "is_homebrew": "bool",
            "name": "uuid",
            "version": "version"
        }
        super().setup_class(self,"api/spell-school", data)