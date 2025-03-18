from app import db
from app.error_handler import commit_error_handler
from app import bcrypt
from flask import Response,json


class AuthBaseController:
    def __init__(self,model,defaults):
        self.__model = model
        self.__defaults = defaults
        
        self.session = db.session  
        
        
    # def controller_get_all(self):
    #     _query = self.session.query(self.__model).all()
    #     return self.__return_json__(_query)
        
    
    def controller_register(self,data):
        
        if "id" in data:
            data["id"] = None
            
        if "password" in data:
            password = data["password"]
            data["password"] = bcrypt.generate_password_hash(password).decode("utf-8")     
            
            if self.__return_json__(self.__query_username__(data["username"])):
                res = {
                    "error":"User Already Exist"
                }
                return Response(response=json.dumps(res),status=400,mimetype="application/json")
                
                
            try:
                new_data = self.__model(**{**self.__defaults,**data})
                self.session.add(new_data)
                self.session.commit()
                
            except Exception as e:
                self.session.rollback()
                return commit_error_handler(e)
            
            return self.__return_json__(self.session.query(self.__model).filter_by(id = new_data.id).all())
        else:
            res = {
                    "error":"You need a password"
                }
            return Response(response=json.dumps(res),status=400,mimetype="application/json")
            
        
    def controller_update(self,id = None,data = None):
        if not id or not isinstance(id,int):
            if "id" in data:
                _id = data["id"]
            else:
                return Response(response=json.dumps({}),status=400,mimetype="application/json")
        else:
            _id = id
            if "id" in data:
                return Response(response=json.dumps({}),status=400,mimetype="application/json")
        
        self.__defaults["id"] = _id
        
        _query = self.__query_id__(_id)
        
        if not _query:
            return self.__return_json__(_query)
        
        new_data = {**self.__defaults,**data} 
        
        #haspassword
        new_data["password"] = bcrypt.generate_password_hash(new_data["password"]).decode("utf-8")
        
        try:
            for key,value in new_data.items():
                if hasattr(_query,key):
                    setattr(_query,key,value)
                    
            self.session.merge(_query)
            self.session.flush()
            self.session.commit()
            
        except Exception as e:
            self.session.rollback()
            return commit_error_handler(e)
        
        return self.__return_json__(_query)
    
    
    def controller_delete(self,id):    
        _query = self.__query_id__(id)
        
        try:
            self.session.delete(_query)
            self.session.commit()
            
        except Exception as e:
            self.session.rollback()
            return commit_error_handler(e)
        
        return Response(status=200)


    def controller_get_by_id(self,id):
        return self.__return_json__(self.__query_id__(id),False)


    def controller_authenticate(self,data):
        _query = self.__return_json__(self.__query_username__(data["username"]),False)
        isAuth = False
        
        if _query:
            isAuth = bcrypt.check_password_hash(_query["data"][0]["password"],data["password"])
        
        if isAuth:
            del _query["data"][0]["password"]
            return _query
        else:
            res = {
                "auth":isAuth,
                "error":"Incorret User or Password"
            }
            return Response(response=json.dumps(res),status=400,mimetype="application/json")


    ### Helpers
    def __return_json__(self,items_query,isSecret:bool = True):
        _response = []
        try:
            if(isinstance(items_query,list) or isinstance(items_query,dict)):
                _response = [item.get_dict() for item in items_query] if isSecret else [item.__get_secrets__() for item in items_query]
            else:
                _response = [items_query.get_dict()] if isSecret else [items_query.__get_secrets__()]
        except:
            return items_query
        
        return {
            "data":_response,
            "metadata":{
                "type":str(self.__model().__getClassName__()),
                "size":len(_response)
            }
        }
        
    def __query_id__(self,_id):
        if not _id or not isinstance(_id,int):
            return {
                "error":"No hay un id con el que buscar"
            }
        else:
            _query = self.session.query(self.__model).filter_by(id = _id).first()
            if not _query:
                return Response(response=json.dumps({}),status=404,mimetype="application/json")
            return _query
        
    def __query_username__(self,_username):
        _query = self.session.query(self.__model).filter_by(username = _username).first()
        return _query