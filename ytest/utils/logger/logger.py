import logging
import os
import time
import inspect

class MyLog:
    def __init__(self, level='default', logger_name=__name__):
        self.path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
        self.log_file = os.path.join(self.path, 'Log', 'log.log')
        self.err_file = os.path.join(self.path, 'Log', 'err.log')
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        self.date = '%Y-%m-%d %H:%M:%S'
        self._create_file(self.log_file)
        self._create_file(self.err_file)

        self.handler = logging.FileHandler(self.log_file, encoding='utf-8')
        self.err_handler = logging.FileHandler(self.err_file, encoding='utf-8')
        self.handler.setLevel(logging.DEBUG)
        self.err_handler.setLevel(logging.ERROR)

        self.formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        self.handler.setFormatter(self.formatter)
        self.err_handler.setFormatter(self.formatter)

        self.logger.addHandler(self.handler)
        self.logger.addHandler(self.err_handler)

    def _create_file(self, filename):
        path = os.path.dirname(filename)
        if not os.path.isdir(path):
            os.makedirs(path)
        if not os.path.isfile(filename):
            with open(filename, mode='w', encoding='utf-8'):
                pass

    def debug(self, log_meg):
        self.logger.debug(log_meg)

    def info(self, log_meg):
        frame = inspect.currentframe().f_back
        func_name = frame.f_code.co_name
        line_no = frame.f_lineno
        log_msg = f"{func_name}:{line_no} {log_meg}"
        self.logger.info(log_msg)

    def warning(self, log_meg):
        frame = inspect.currentframe().f_back
        func_name = frame.f_code.co_name
        line_no = frame.f_lineno
        log_msg = f"{func_name}:{line_no} {log_meg}"
        self.logger.warning(log_msg)

    def error(self, log_meg):
        frame = inspect.currentframe().f_back
        func_name = frame.f_code.co_name
        line_no = frame.f_lineno
        log_msg = f"{func_name}:{line_no} {log_meg}"
        self.logger.error(log_msg)

    def critical(self, log_meg):
        frame = inspect.currentframe().f_back
        func_name = frame.f_code.co_name
        line_no = frame.f_lineno
        log_msg = f"{func_name}:{line_no} {log_meg}"
        self.logger.critical(log_msg)

    def __del__(self):
        self.logger.removeHandler(self.handler)
        self.logger.removeHandler(self.err_handler)



logger = MyLog(logger_name=__name__)

def some_function():
    logger.debug('This is a debug message')
    logger.info('This is an info message')
    logger.warning('This is a warning message')
    logger.error('This is an error message')
    logger.critical('This is a critical message')

if __name__ == "__main__":
    MyLog = MyLog()
    MyLog.debug("This is debug message")
    MyLog.info("This is info message")
    MyLog.warning("This is warning message")
    MyLog.error("This is error")
    MyLog.critical("This is critical message")
    some_function()
