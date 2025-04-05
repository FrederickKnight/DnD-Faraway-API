from flask import Response,json

from sqlalchemy.exc import (
    IntegrityError
)

def error_handler(error,_context:str = ""):
    
    if isinstance(error,dict):
        _error = error["error"]
        _message = error["message"]
        _details = error["details"]
        
        response_status = 400
        
    else:
        if isinstance(error,IntegrityError):
            _error = "Integrity Error"
            _message = "Invalid given data or parameters"
            _details = str(error)
            
            response_status = 400
            
        if isinstance(error,TypeError):
            _error = "Type Error"
            _message = "Invalid given data or parameters"
            _details = str(error)
            
            response_status = 400
        
    schema_error = {
            "data":[],
            "metadata":{
                "context":_context,
                "error":_error,
                "message":_message,
                "details":_details,
            }
    }
        
    return Response(response=json.dumps(schema_error),status=response_status,mimetype="application/json")