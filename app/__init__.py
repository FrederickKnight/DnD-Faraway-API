from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_cors import CORS
import os

db = SQLAlchemy()

DB_NAME = os.environ["DB_NAME"]

app = Flask(__name__)

bcrypt = Bcrypt(app)
CORS(app)

def create_app():
    
    app.config['SECRET_KEY'] = os.environ["SECRET_KEY"]
    
    app.config["SQLALCHEMY_DATABASE_URI"] = f'sqlite:///{DB_NAME}'
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
        spell_school_route,
        spell_route,
        spell_stats_route,
        spell_components_route,
        spell_scaling_route,
        spell_user_creation_route
    )
    
    from app.routes.auth import (
        auth_route
    )
    
    #user & auth
    app.register_blueprint(auth_route.auth_bp,url_prefix="/api/auth/user")
    
    
    app.register_blueprint(spell_school_route.spell_school_bp,url_prefix="/api/spell-school/")
    app.register_blueprint(spell_route.spell_bp,url_prefix="/api/spell/")
    app.register_blueprint(spell_stats_route.spell_stats_bp,url_prefix="/api/spell-stats/")
    app.register_blueprint(spell_components_route.spell_components_bp,url_prefix="/api/spell-components/")
    app.register_blueprint(spell_scaling_route.spell_scaling_bp,url_prefix="/api/spell-scaling/")
    
    
    # user relations
    app.register_blueprint(spell_user_creation_route.spell_user_creation_bp,url_prefix="/api/user/spell")
    

def __return_json__(items_query):
        try:
            if(isinstance(items_query,list) or isinstance(items_query,dict)):
                return [item.get_dict() for item in items_query]
            else:
                return items_query.get_dict()
        except:
            return items_query