from flask import Blueprint,request
from app.controllers import BaseController

class BaseRoute:
    def __init__(self,blueprint:Blueprint,controller:BaseController):
        self.__blueprint = blueprint
        self.__controller = controller
        
        self._create_routes()
        
        
    def _create_routes(self):
        
        @self.__blueprint.route("/",methods=["GET"])
        def route_get_all():
            return self.__controller.controller_get_all(request)

        @self.__blueprint.route("/",methods=["POST"])
        def route_add():
            return self.__controller.controller_register(request)

        @self.__blueprint.route("/",methods=["PUT"])
        def route_update():
            return self.__controller.controller_update(request=request)

        @self.__blueprint.route("/<int:id>",methods=["PUT"])
        def route_update_by_id(id):
            return self.__controller.controller_update(id=id,request=request)

        @self.__blueprint.route("/<int:id>",methods=["DELETE"])
        def route_delete_by_id(id):
            return self.__controller.controller_delete(id=id)

        @self.__blueprint.route("/<int:id>",methods=["GET"])
        def route_get_by_id(id):
            return self.__controller.controller_get_by_id(id=id,request=request)