from app import db
from app.error_handler import error_handler
from flask import Response,json,Request,request
import re

from app.controllers.versions import (
    JsonResponseV1,
    JsonResponseV2
)

class BaseController:
    def __init__(self,model,defaults):
        self.__model = model
        self.__defaults = defaults
        
        self.session = db.session  
        
        
    def controller_get_all(self,request:Request):
        
        version = request.headers.get("Accept")
        return self.__return_json__(self.__query_args__(self.__model,request.args),version)
        
    
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
        
        return self.__return_json__(self.session.query(self.__model).filter_by(id = new_data.id).first(),version)
        
        
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
        
        _query = self.session.query(self.__model).filter_by(id = _id)
        
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
        _query = self.session.query(self.__model).filter_by(id=id).first()
        
        try:
            self.session.delete(_query)
            self.session.commit()
            
        except Exception as e:
            self.session.rollback()
            return error_handler(e,"Error in commit")
        
        return Response(status=204)


    def controller_get_by_id(self,id,request:Request):
        version = request.headers.get("Accept")
        return self.__return_json__(self.__query_args__(self.__model,request.args,id),version)


    ### Helpers
    def __return_json__(self,items,version:str = None):
        if isinstance(items,Response):
            return items
        
        if isinstance(items,dict) or isinstance(items,list):
            _response = [item.get_dict() for item in items]

        else:
            _response = [items.get_dict()]
        
        #regex para versioning
        re_version = re.search(r'dndfaraway\.v(\d+)', version.lower())
        _version = f"v{re_version.group(1)}" if re_version else "v1"
        
        versions = {
            "v1" : JsonResponseV1,
            "v2" : JsonResponseV2
        }
        
        res_version = versions.get(_version,None)
        
        if res_version:
            return res_version(_response,self.__model).get_response()
            
        else:
            error = {
                "error": "Incorrect Version of API",
                "message": "The given Version of the API is incorrect or null",
                "details" : 'Expected dndfaraway.v[version] in header with keyword "Accept" with a correct version number'
            }
            return error_handler(error,"Error in Versioning")        
    
    def __query_args__(self,model,args = None,_id:int = None):
        _q = self.session.query(model)
        args = args if args else request.args
        
        if _id:
            if isinstance(_id,int):
                _q = _q.filter_by(id = _id)
            else:
                error = {
                    "error": "Invalid id",
                    "message" : "Required id for search, id it's not valid",
                    "details" : "Expected a number/interger id"
                }
                return error_handler(error,"Error in query")
        
        filter_field = args.get("filter_field", type=str, default=None)
        filter_value = args.get("filter_value", type=str, default=None)
        if filter_field and filter_value:
            #busca todos los field separados por . en la query de la url
            if "." in filter_field:
                attrs = filter_field.split(".")
                
                rel_chain = []
                current_model = self.__model
                
                #pasa por todos los atributos
                for attr in attrs[:-1]:
                    relation = getattr(current_model,attr)
                    related_model = relation.property.mapper.class_
                    rel_chain.append(relation)
                    current_model = related_model
            
                try:
                    final_attr = getattr(current_model,attrs[-1])
                     # junta los atributos con un join para el filtro
                    for rel in rel_chain:
                        _q = _q.join(rel)
                        
                    _q = _q.filter(final_attr == filter_value)
                    
                except:
                    error = {
                        "error": "Attribute Error",
                        "message" : "Invalid attribute in query",
                        "details" : "Expected a valid attribute"
                    }
                    return error_handler(error,"Error in given attribute")

            else:
                _q = _q.filter(getattr(model, filter_field) == filter_value)
        
        
        limit = args.get("limit",type=int,default=None)
        if limit is not None:
            _q = _q.limit(limit)
            
        offset = args.get("offset",type=int,default=0)
        if offset > 0:
            _q = _q.offset(offset)
            
        page = args.get("page",type=int,default=1)
        if page > 1:
            _p = (page - 1) * limit if limit else (page - 1)
            _q = _q.offset(_p)
            
        # return first or all
        first = args.get("first",type=bool,default=False)
        
        result = _q.first() if first else _q.all()
        
        if result:
            return result
        else:
            return Response(status=404)