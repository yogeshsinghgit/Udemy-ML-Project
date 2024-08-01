import sys
from src.logger import *

def error_message_details(error, error_detail:sys):
    _, _, exc_tb = error_detail.exc_info()

    file_name = exc_tb.tb_frame.f_code.co_filename
    error_line = exc_tb.tb_lineno
    message = str(error)

    error_message = "Error In Script Name [{0}] Line [{1}] Message [{2}]".format( 
        file_name,
        error_line,
        message
    )
    return error_message

class CustomException(Exception):
    def __init__(self, error_message, error_detail:sys):
        super().__init__(error_message)

        self.error_message = error_message_details(error_message, error_detail=error_detail)

    def __str__(self) -> str:
        return self.error_message

        