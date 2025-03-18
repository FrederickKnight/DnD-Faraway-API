from app.models import (
    SpellComponents
)

from app.controllers import BaseController

class SpellComponentsController(BaseController):
    def __init__(self):
        defaults = {
            "verbal":None,
            "somantic":None,
            "material":None,
            "special":None,
            "description":None
        }
        super().__init__(SpellComponents, defaults)