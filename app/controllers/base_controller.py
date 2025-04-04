from app import db
from app.error_handler import error_handler
from flask import Response,json


class BaseController:
    def __init__(self,model,defaults):
        self.__model = model
        self.__defaults = defaults
        
        self.session = db.session  
        
        
    def controller_get_all(self):
        _query = self.session.query(self.__model).all()
        return self.__return_json__(_query)
        
    
    def controller_register(self,data):
        
        if "id" in data:
            data["id"] = None
            
        try:
            new_data = self.__model(**{**self.__defaults,**data})
            self.session.add(new_data)
            self.session.commit()
            
        except Exception as e:
            self.session.rollback()
            return error_handler(e,"Error in commit")
        
        return self.__return_json__(self.session.query(self.__model).filter_by(id = new_data.id).all())
        
        
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
        
        return self.__return_json__(_query)
    
    def controller_delete(self,id):    
        _query = self.__query_id__(id)
        
        try:
            self.session.delete(_query)
            self.session.commit()
            
        except Exception as e:
            self.session.rollback()
            return error_handler(e,"Error in commit")
        
        return Response(status=204)


    def controller_get_by_id(self,id):
        return self.__return_json__(self.__query_id__(id))


    ### Helpers
    def __return_json__(self,items_query):
        _response = []
        try:
            if(isinstance(items_query,list) or isinstance(items_query,dict)):
                _response = [item.get_dict() for item in items_query]
            else:
                _response = [items_query.get_dict()]
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
            error = {
                "error": "Id Null",
                "message" : "Required id for search, id it's not given",
                "details" : ""
            }
            return error_handler(error,"Error in query")
        else:
            _query = self.session.query(self.__model).filter_by(id = _id).first()
            if not _query:
                return Response(response=json.dumps({}),status=404,mimetype="application/json")
            return _query