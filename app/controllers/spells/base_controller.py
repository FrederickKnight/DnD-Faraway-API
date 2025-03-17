from app import db
from app.error_handler import commit_error_handler
from flask import Response,json

session = db.session  

class BaseController:
    def __init__(self,model,defaults):
        self.__model = model
        self.__defaults = defaults
        
    def controller_get_all(self):
        _query = session.query(self.__model).all()
        return self.__return_json__(_query)
        
    
    def controller_register(self,data):
        
        if "id" in data:
            data["id"] = None
            
        try:
            new_data = self.__model(**{**self.__defaults,**data})
            session.add(new_data)
            session.commit()
            
        except Exception as e:
            session.rollback()
            return commit_error_handler(e)
        
        return self.__return_json__(session.query(self.__model).filter_by(id = new_data.id).all())
        
        
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
                    
            session.merge(_query)
            session.flush()
            session.commit()
            
        except Exception as e:
            session.rollback()
            return commit_error_handler(e)
        
        return self.__return_json__(_query)
    
    def controller_delete(self,id):    
        _query = self.__query_id__(id)
        
        try:
            session.delete(_query)
            session.commit()
            
        except Exception as e:
            session.rollback()
            return commit_error_handler(e)
        
        return Response(status=200)


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
            return {
                "error":"No hay un id con el que buscar"
            }
        else:
            _query = session.query(self.__model).filter_by(id = _id).first()
            if not _query:
                return Response(response=json.dumps({}),status=404,mimetype="application/json")
            return _query