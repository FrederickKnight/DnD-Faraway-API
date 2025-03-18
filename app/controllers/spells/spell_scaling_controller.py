from app.models import (
    SpellScaling
)

from app.controllers import BaseController

class SpellScalingController(BaseController):
    def __init__(self):
        defaults = {
            "description":None
        }
        super().__init__(SpellScaling, defaults)