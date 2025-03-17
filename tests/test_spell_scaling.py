from tests import BaseTesting
import pytest

@pytest.mark.order(3)
class TestSpellScaling(BaseTesting):
    def setup_class(self):        
        data = {
            "description":"uuid"
        }
        super().setup_class(self,"api/spell-scaling", data)
        