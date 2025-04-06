from flask import Response,json

from sqlalchemy.exc import (
    IntegrityError
)

def error_handler(error,_context:str = ""):
    
    response_status = 400
    _error = "Unhandled Error"
    _message = "Something went wrong"
    
    if isinstance(error,dict):
        _error = error.get("error","Unknown Error")
        _message = error.get("message","No message provided")
        _details = error.get("details","No details provided")
        
    else:
        _details = str(error)
        if isinstance(error,IntegrityError):
            _error = "Integrity Error"
            _message = "Invalid given data or parameters"
            _details = str(error.orig) if hasattr(error,"orig") else str(error)
            
        elif isinstance(error,TypeError):
            _error = "Type Error"
            _message = "Invalid given data or parameters"
        
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