from app.models import (
    SpellScaling
)

from .base_controller import BaseController

class SpellScalingController(BaseController):
    def __init__(self):
        defaults = {
            "description":None
        }
        super().__init__(SpellScaling, defaults)