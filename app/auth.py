from app import db,Bcrypt
from flask import Response,json

from os import urandom
import binascii
from hashlib import sha256
from datetime import datetime,timedelta
import math

from .models import (
    User,
    UserSession
)

bcrypt = Bcrypt()

session = db.session

_user_defaults = {
    "username":None,
    "password":None,
    "auth_level":10
}

_sessions_defaults = {
    "id_user":None,
    "session":None,
    "expires_at":None
}

# --------- USER -------------

def register_user(data):
    if "id" in data:
        data["id"] = None
        
    user_already_exist = True if __query_username__(data["username"]) else False
    
    if not "password" in data:
        return Response(response=json.dumps({"error":"invalid given data, not password"}),status=400,mimetype="application/json")

    data["password"] = bcrypt.generate_password_hash(data["password"])
    
    if not user_already_exist:
        try:
            new_data = User(**{**_user_defaults,**data})
            session.add(new_data)
            session.commit()
            
        except Exception as e:
            session.rollback()
            raise e

        return __return_json__(session.query(User).filter_by(id = new_data.id).first())
    else:
        return Response(response=json.dumps({"error":"user already exist"}),status=400,mimetype="application/json")
    
def delete_user_by_id(id):
    
    _user = __query_id__(id)
        
    if _user != None:
        try:
            session.delete(_user)
            session.commit()
            
        except Exception as e:
            session.rollback()
            raise e
        
        return Response(status=204)
    else:
        return Response(response=json.dumps({"error":"User doesn't exist or invalid given data"}),status=400,mimetype="application/json")

        
# Update User later

def get_by_id(_id):
    _user = __query_id__(_id)
    
    if _user != None:
        return __return_json__(_user)
    else:
        return Response(response=json.dumps({"error":"User doesn't exist or invalid given data"}),status=400,mimetype="application/json")
        
def validate_user(data):
    if "username" in data and "password" in data:
        _user = __query_username__(data["username"])
        if _user == None:
            return Response(response=json.dumps({"error":"User doesn't exist or invalid given data"}),status=400,mimetype="application/json")
            
        data_pass = bcrypt.check_password_hash(_user.__get_secrets__()["password"],data["password"])
        
        if data_pass == False:
            return Response(response=json.dumps({"error":"Password is incorrect or invalid given data"}),status=400,mimetype="application/json")
            
        return __return_json__(_user)
    
    else:
        return Response(response=json.dumps({"error":"invalid given data"}),status=400,mimetype="application/json")
# --------- AUTH -------------
def generateSessionToken():
    bytes = urandom(20)
    token = binascii.hexlify(bytes).decode()
    return Response(response=json.dumps({"token":token}),status=200,mimetype="application/json")
    

def createSessionToken(_json,UserId:int):
    if not "token" in _json:
        return Response(response=json.dumps({"error":"there is no token"}),status=400,mimetype="application/json")
    
    token = _json["token"]    
    
    userSessionId = sha256(token.encode('utf-8'),usedforsecurity=True).hexdigest()
    expires_at = datetime.now() + timedelta(days=30)
    session_data = {
        "id_user":UserId,
        "session":userSessionId,
        "expires_at":math.floor(expires_at.timestamp())
    }
    
    try:
        new_session = UserSession(**{**_sessions_defaults,**session_data})
        session.add(new_session)
        session.commit()
        
    except Exception as e:
        session.rollback()
        raise e
    return Response(response=json.dumps(session_data),status=200,mimetype="application/json")
    
    
def validateSessionToken(token:str):
    userSessionId = sha256(token.encode('utf-8'),usedforsecurity=True).hexdigest()
    _query = session.query(UserSession).filter_by(session = userSessionId).first()
    
    sessionData = {
        "session":None,
        "user":None
    }
    
    if not _query:
        return {
        "session":None,
        "user":None
    }
    
    sessionJson = _query.get_json()    
    expiration_Date = datetime.fromtimestamp(sessionJson["expires_at"])
    
    if datetime.now() >= expiration_Date:
        # si expiro
        session.delete(_query)
        session.commit()
        return {
            "session":None,
            "user":None
        }
    
    if datetime.now() >= (expiration_Date - timedelta(days=-15)):
        # si es menor a 15 dias
        new_expires_at = datetime.now() + timedelta(days=30)
        _query.expires_at = new_expires_at
        session.merge(_query)
        session.flush()
        session.commit()
        
    id_user = sessionJson["user"]["id"]
    sessionData["user"] = sessionJson["user"]
    
    del sessionJson["user"]
    sessionJson["id_user"] = id_user
    sessionData["session"] = sessionJson
    return Response(response=json.dumps(sessionData),status=200,mimetype="application/json")

def invalidateSession(userSessionId:str):
    _query = session.query(UserSession).filter_by(session = userSessionId).first()
    if _query:
        session.delete(_query)
        session.commit()
        return Response(response=json.dumps({"message":"session succesfully deleted"}),status=200,mimetype="application/json")
    else:
        return Response(response=json.dumps({"error":"Invalid Session"}),status=400,mimetype="application/json")
        
    
#helpers
def __return_json__(items_query:User,isSecret:bool = True):
        _response = []
        try:
            if(isinstance(items_query,list) or isinstance(items_query,dict)):
                _response = [item.get_dict() for item in items_query] if isSecret else [item.__get_secrets__() for item in items_query]
            else:
                _response = [items_query.get_json()] if isSecret else [items_query.__get_secrets__()]
        except:
            return items_query
        
        return {
            "data":_response,
            "metadata":{
                "type":str(User().__getClassName__()),
                "size":len(_response)
            }
        }
        
def __query_id__(_id):
    if isinstance(_id,int):
        return session.query(User).filter_by(id = _id).first()
    else:
        return Response(response=json.dumps({"invalid given data"}),status=400,mimetype="application/json")

def __query_username__(_username):
    if isinstance(_username,str):
        return session.query(User).filter_by(username = _username).first()
    else:
        return Response(response=json.dumps({"error":"invalid given data"}),status=400,mimetype="application/json")

    
def __query_username__(_username):
    if isinstance(_username,str):
        return session.query(User).filter_by(username=_username).first()
    else:
        return None