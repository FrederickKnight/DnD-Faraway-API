from app import db
from app.error_handler import error_handler
from flask import Response,json,Request


class BaseController:
    def __init__(self,model,defaults):
        self.__model = model
        self.__defaults = defaults
        
        self.session = db.session  
        
        
    def controller_get_all(self,request:Request):
        
        version = request.headers.get("Accept")
        
        _query = self.session.query(self.__model).all()
        return self.__return_json__(_query,version)
        
    
    def controller_register(self,request:Request):
        
        json_request = request.get_json()
        version = request.headers.get("Accept")
        
        if "id" in json_request:
            json_request["id"] = None
            
        try:
            new_data = self.__model(**{**self.__defaults,**json_request})
            self.session.add(new_data)
            self.session.commit()
            
        except Exception as e:
            self.session.rollback()
            return error_handler(e,"Error in commit")
        
        return self.__return_json__(self.session.query(self.__model).filter_by(id = new_data.id).all(),version)
        
        
    def controller_update(self,id = None,request:Request = None):
        
        json_request = request.get_json()
        version = request.headers.get("Accept")
        
        if not id or not isinstance(id,int):
            if "id" in json_request:
                _id = json_request["id"]
            else:
                return Response(response=json.dumps({"message":"Not id in data"}),status=400,mimetype="application/json")
        else:
            _id = id
            if "id" in json_request:
                return Response(response=json.dumps({"message":"id in data and url"}),status=400,mimetype="application/json")
        
        self.__defaults["id"] = _id
        
        _query = self.__query_id__(_id)
        
        if not _query:
            return self.__return_json__(_query,version)
        
        new_data = {**self.__defaults,**json_request} 
        
        try:
            for key,value in new_data.items():
                if hasattr(_query,key):
                    setattr(_query,key,value)
                    
            self.session.merge(_query)
            self.session.flush()
            self.session.commit()
            
        except Exception as e:
            self.session.rollback()
            return error_handler(e,"Error in commit")
        
        return self.__return_json__(_query,version)
    
    def controller_delete(self,id):
        _query = self.__query_id__(id)
        
        try:
            self.session.delete(_query)
            self.session.commit()
            
        except Exception as e:
            self.session.rollback()
            return error_handler(e,"Error in commit")
        
        return Response(status=204)


    def controller_get_by_id(self,id,request:Request):
        version = request.headers.get("Accept")
        return self.__return_json__(self.__query_id__(id),version)


    ### Helpers
    def __return_json__(self,items,version:str = None):
        _version = version if version != None else "v1"
    
        if isinstance(items,Response):
            return items
        
        if isinstance(items,dict) or isinstance(items,list):
            _response = [item.get_dict() for item in items]

        else:
            _response = [items.get_dict()]
        
        if "dndfaraway.v1" in _version:
            return {
                "data":_response,
                "metadata":{
                    "type":str(self.__model().__getClassName__()),
                    "size":len(_response)
                }
            }
            
        if "dndfaraway.v2" in _version:
            return {
                "response":_response,
                "metadata":{
                    "type":str(self.__model().__getClassName__()),
                    "size":len(_response),
                    "api_version":"v2"
                }
            }
            
        else:
            error = {
                "error": "Incorrect Version of API",
                "message": "The given Version of the API is incorrect or null",
                "details" : "Expected dndfaraway.[version]"
            }
            return error_handler(error,"Error in Versioning")
        
        
    def __query_id__(self,_id):
        if not _id or not isinstance(_id,int):
            error = {
                "error": "Id Null",
                "message" : "Required id for search, id it's not given",
                "details" : ""
            }
            return error_handler(error,"Error in query")
        else:
            _query = self.session.query(self.__model).filter_by(id = _id).first()
            if not _query:
                return Response(status=404)
            return _query