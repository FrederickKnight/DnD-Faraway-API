from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_cors import CORS
import os
from dotenv import load_dotenv
from .error_handler import register_error_handlers

db = SQLAlchemy()

app = Flask(__name__)

register_error_handlers(app)
bcrypt = Bcrypt(app)
CORS(app)

def create_app():
    
    if os.environ.get("DB_URL") is None:
        load_dotenv()

    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DB_URL")
    db.init_app(app)
    
    from .models import (
        BaseCreatable,
        BaseModel
    )
    
    with app.app_context():
        db.create_all()

    define_routes()
    
    return app

def define_routes():
    # -------------------------------- Routes --------------------------------
    
    ## Spells Routes    
    from app.routes.spells import (
        SpellComponentsRoute,
        SpellSchoolRoute,
        SpellScalingRoute,
        SpellRoute,
        SpellStatsRoute,
        SpellUserCreationRoute
    )
    
    from app.routes.auth import (
        auth_route
    )
    
    #user & auth
    app.register_blueprint(auth_route.auth_bp,url_prefix="/api/auth/user")
    
    
    # spell routes
    app.register_blueprint(SpellSchoolRoute().get_blueprint(),url_prefix="/api/spell-school/")
    app.register_blueprint(SpellRoute().get_blueprint(),url_prefix="/api/spell/")
    app.register_blueprint(SpellStatsRoute().get_blueprint(),url_prefix="/api/spell-stats/")
    app.register_blueprint(SpellComponentsRoute().get_blueprint(),url_prefix="/api/spell-components/")
    app.register_blueprint(SpellScalingRoute().get_blueprint(),url_prefix="/api/spell-scaling/")
    
    
    # user relations
    app.register_blueprint(SpellUserCreationRoute().get_blueprint(),url_prefix="/api/user/spell")
    

def __return_json__(items_query):
        try:
            if(isinstance(items_query,list) or isinstance(items_query,dict)):
                return [item.get_dict() for item in items_query]
            else:
                return items_query.get_dict()
        except:
            return items_query