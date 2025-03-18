from app.models import (
    UserSpell
)

from app.controllers import BaseController

class SpellUserCreationController(BaseController):
    def __init__(self):
        defaults = {
            "id_spell":None,
            "id_user":None
        }
        super().__init__(UserSpell, defaults)