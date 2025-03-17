from flask import Response,json

from sqlalchemy.exc import (
    IntegrityError
)

def commit_error_handler(error):
    
    # if isinstance(error,IntegrityError):
    #     response_data = json.dumps({
    #         "error":"IntegrityError",
    #         "details":"Invalid given data or parameters"
    #     })
    #     response_status = 400
        
    # if isinstance(error,TypeError):
    #     response_data = json.dumps({
    #         "error":"TypeError",
    #         "details":"Invalid given data or parameters",
    #         "moredetails":str(error)
    #     })
    #     response_status = 400
    # else:
    raise error
        
    return Response(response=response_data,status=response_status,mimetype="application/json")