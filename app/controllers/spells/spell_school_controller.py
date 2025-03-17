from app.models import (
    SpellSchool
)

from .base_controller import BaseController

class SpellSchoolController(BaseController):
    def __init__(self):
        defaults = {
            "name":None,
            "version":"0.0.0.0",
            "is_homebrew":False,
            "description":None
        }
        super().__init__(SpellSchool, defaults)