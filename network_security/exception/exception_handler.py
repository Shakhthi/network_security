import sys

class NetworksecurityException(Exception):
    def __init__(self, message, error_detail:sys):
        self.message = message
        _, _, exec_tb = error_detail.exc_info()

        self.line_number = exec_tb.tb_lineno
        self.file_name = exec_tb.tb_frame.f_code.co_filename

    def __str__(self):
        return f"Error occured in python filename [{self.file_name}] at line number [{self.line_number}] with message [{self.message}]"

""" if __name__ == "__main__":
    try:
        a = 1/0
        print("this cant be done man", a)
    except Exception as e:
        raise NetworksecurityException(e, sys)
 """
    