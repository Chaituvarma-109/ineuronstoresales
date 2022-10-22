import sys


class SalesException(Exception):
    def __init__(self, error_message: Exception, error_detail: sys):
        super().__init__(error_message)
        self.error_message = SalesException.get_detailed_error_msg(error_message, error_detail)

    @staticmethod
    def get_detailed_error_msg(error_message, error_detail) -> str:
        """
        This function will return a detailed error message for a particular exception
        :param error_message: Exception object
        :param error_detail: object of sys module
        :return: error message
        """
        _, _, exec_tb = error_detail.exc_info()

        exception_block_line_number = exec_tb.tb_frame.tb_lineno
        try_block_line_num = exec_tb.tb_lineno
        file_name = exec_tb.tb_frame.f_code.co_filename

        error_message = f"Error occurred in script: {file_name} at try block line number: {try_block_line_num} and " \
                        f"exception block line num: {exception_block_line_number} error msg: {error_message} "
        return error_message

    def __str__(self):
        return self.error_message

    def __repr__(self):
        return str(SalesException.__name__)
