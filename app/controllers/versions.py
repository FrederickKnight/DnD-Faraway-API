from app.models import BaseModel
 
class JsonResponse:
    def __init__(self,response,model:BaseModel):
        self._model = model()
        if isinstance(response,dict) or isinstance(response,list):
            self._response = response
            self.size = len(self._response)
        else:
            self._response = response.get_json()
            self.size = len([self._response])

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
        schema =  {
                "response":self._response,
                "metadata":{
                    "type":self.type,
                    "size":self.size,
                    "api_version":"v2",
                    "type_response":"list" if isinstance(self._response,list) else "dict",
                }
            }
        
        if not isinstance(self._response,list):
            schema["metadata"]["response_id"] = self._response["id"]
        return schema