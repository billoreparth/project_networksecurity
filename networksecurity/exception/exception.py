import sys 
from networksecurity.logging import logger 

class NetworkSecurityException:
    def __init__(self,error_message,error_details:sys):
        self.error_message=error_message
        _,_,exc_tb=error_details.exc_info()
        self.line_no=exc_tb.tb_lineno
        self.file_name = exc_tb.tb_frame.f_code.co_filename

    def __str__(self):
        return "the error has occured in python script name {0} in line number {1} and error message is {2}".format(self.file_name,self.line_no,str(self.error_message))
    

# if __name__ == '__main__':
#     try:
#         logger.logging.info('try block testing')
#         a=1/0
#         print('cant',a)
#     except Exception as e :
#         raise TypeError(NetworkSecurityException(e,sys))
        