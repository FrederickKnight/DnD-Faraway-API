from app.models import (
    User
)
from app.controllers import AuthBaseController

class AuthControllerUser(AuthBaseController):
    def __init__(self):
        defaults = {
            "username":None,
            "password":None,
            "auth_level":5
        }
        super().__init__(User, defaults)