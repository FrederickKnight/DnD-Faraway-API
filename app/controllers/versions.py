from app.models import BaseModel
 
class JsonResponse:
    def __init__(self,response,model:BaseModel):
        self._response = response
        self._model = model()
        
        self.size = len(self._response)
        self.type = str(self._model.__getClassName__())

    def get_response(self):
        return {
            "response":["Base Response"],
            "metadata":{
                "type":"Base Response"
            }
        }

class JsonResponseV1(JsonResponse):
    def get_response(self):
        return {
                "data":self._response,
                "metadata":{
                    "type":self.type,
                    "size":self.size,
                    "api_version":"v1"
                }
            }

class JsonResponseV2(JsonResponse):
    def get_response(self):
        return {
                "response":self._response,
                "metadata":{
                    "type":self.type,
                    "size":self.size,
                    "response_id":self._response[0].get("id",None),
                    "api_version":"v2"
                }
            }