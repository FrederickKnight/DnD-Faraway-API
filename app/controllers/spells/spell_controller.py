from app.models import (
    Spell
)

from .base_controller import BaseController  

class SpellController(BaseController):
    def __init__(self):
        defaults = {
            "name":None,
            "version":"0.0.0.0",
            "is_homebrew":False,
            "description":None,
            "id_stats":None
        }
        super().__init__(Spell, defaults)