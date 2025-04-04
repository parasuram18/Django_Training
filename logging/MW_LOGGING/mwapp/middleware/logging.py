import logging
from django.http import JsonResponse
import traceback
import sys
logger = logging.getLogger("mwapp.views")

class loggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # redirect to next middleware or view function
        # it handles succesfull request/response
        response = self.get_response(request) 
        # log message for info level
        info_log = {
            "host":request.get_host(),
            "path":request.path,
            "url":request.build_absolute_uri(),
            "ip_address":request.META.get("REMOTE_ADDR"),
            "method":request.method,
            "status":response.status_code
        }
        logger.info(info_log)
        return response
    # This function captures the unhandled exceptions in every request
    def process_exception(self, request, exception):
        # get error details using traceback module

        ece_type, exc_value, tb_obj = sys.exc_info()
        traceback_info = traceback.extract_tb(exception.__traceback__)
        for trace in traceback_info:
            if "site-packages" not in trace.filename:
                tb = trace
                break
        # tb = traceback_info[-1]
        error_line_number = tb.lineno
        func_name = tb.name
        error_code = tb.line
        variables = tb.locals
        # log message for info level
        error_log = {
            "url":request.build_absolute_uri(),
            "method":request.method,
            "host":request.get_host(),
            "path":request.path,
            "ip_address":request.META.get("REMOTE_ADDR"),
            "func_name": func_name,
            "exception":ece_type.__name__,
            "error":str(exception),
            "error_line_no":error_line_number,
            "error_code":error_code,
            "variables":variables
        }

        logger.error(error_log)
        return JsonResponse({"status":"Error",'message':str(exception)},status=400)
    
