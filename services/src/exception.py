import sys
from .logger import logging 

class CustomException(Exception):
    """ 
    Class to handle the custom exception.
    
    Args:
        Exception (class): The base class for all exceptions.
    """
    
    def __init__(self, error_message, error_detail: sys = sys):
        super().__init__(error_message)
        self.error_message = error_message_detail(error_message, error_detail)

    def __str__(self):
        return self.error_message
    

def error_message_detail(error, error_detail: sys = sys):
    """ 
    Function to get the details of the error message in desired format.
    
    Args:
        error (str): The error message.
        error_detail (sys): The error details.
    """
    exc_type, exc_value, exc_tb = error_detail.exc_info()
    
    if exc_tb is not None:
        file_name = exc_tb.tb_frame.f_code.co_filename
        line_number = exc_tb.tb_lineno
        error_message = (
            f"Error occurred in python script named: [{file_name}], "
            f"line number: [{line_number}], error message: [{str(error)}]"
        )
        logging.error(error_message)
        return error_message
    else:
        return str(error) 