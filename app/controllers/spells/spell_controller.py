from app.models import (
    Spell
)

from app.controllers import BaseController  

from app import db
from flask import Response,Request


class SpellController(BaseController):
    def __init__(self):
        defaults = {
            "name":None,
            "version":"0.0.0.0",
            "is_homebrew":False,
            "description":None,
            "id_stats":None
        }
        super().__init__(Spell, defaults)
        
    def controller_get_stats_from_id(self,id,request:Request):
        version = request.headers.get("Accept")
        _query = self.__query_id__(id)
        
        if isinstance(_query,Response):
            return _query

        return self.__return_json__(_query.stats,version)
        
    def controller_get_components_from_id(self,id,request:Request):
        version = request.headers.get("Accept")
        _query = self.__query_id__(id)
        
        if isinstance(_query,Response):
            return _query

        return self.__return_json__(_query.stats.components,version)
    
    def controller_get_spell_school_from_id(self,id,request:Request):
        version = request.headers.get("Accept")
        _query = self.__query_id__(id)
        
        if isinstance(_query,Response):
            return _query

        return self.__return_json__(_query.stats.spell_school,version)
    
    def controller_get_scaling_from_id(self,id,request:Request):
        version = request.headers.get("Accept")
        _query = self.__query_id__(id)
        
        if isinstance(_query,Response):
            return _query

        return self.__return_json__(_query.stats.scaling,version)
    
    def __query_id__(self,id):
        return self.session.query(self._model).filter_by(id = id).first()