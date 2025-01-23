import logging
import os
import time
import inspect


class MyLog:
    def __init__(self, level="default", logger_name=__name__):
        """
        创建一个用于记录日志的类。

        :param level: 日志级别，默认为"default"
        :param logger_name: 日志器的名称，默认为当前文件的名称
        """

        # 确定日志文件的路径
        self.path = os.path.abspath(os.getcwd())
        self.log_file = os.path.join(self.path, "log", "log.log")  # 模块日志文件
        self.err_file = os.path.join(self.path, "log", "err.log")  # 错误日志文件

        # 创建日志器
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(logging.DEBUG)  # 设置日志级别为DEBUG

        # 设置日期格式
        self.date = "%Y-%m-%d %H:%M:%S"

        # 确保目录和文件存在
        self._create_file(self.log_file)
        self._create_file(self.err_file)

        # 添加文件处理器
        self.handler = logging.FileHandler(self.log_file, encoding="utf-8")
        self.err_handler = logging.FileHandler(self.err_file, encoding="utf-8")
        self.handler.setLevel(logging.DEBUG)  # 设置日志为DEBUG级别
        self.err_handler.setLevel(logging.ERROR)  # 设置错误日志为ERROR级别

        # 设置格式化过的日志格式
        self.formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
        self.handler.setFormatter(self.formatter)
        self.err_handler.setFormatter(self.formatter)

        # 添加日志处理器到日志器
        self.logger.addHandler(self.handler)
        self.logger.addHandler(self.err_handler)

    def _create_file(self, filename):
        """
        确保文件路径和文件存在，如果不存在，则创建目录和空文件
        :param filename: 文件名
        """
        path = os.path.dirname(filename)
        if not os.path.isdir(path):
            os.makedirs(path)  # 创建目录
        if not os.path.isfile(filename):
            with open(filename, mode="w", encoding="utf-8"):
                pass  # 创建文件

    def debug(self, log_msg):
        """记录DEBUG级别的日志"""
        self.logger.debug(log_msg)

    def info(self, log_msg):
        """记录INFO级别的日志"""
        frame = inspect.currentframe().f_back
        func_name = frame.f_code.co_name
        line_no = frame.f_lineno
        log_msg = f"{func_name}:{line_no} {log_msg}"
        self.logger.info(log_msg)

    def warning(self, log_msg):
        """记录WARNING级别的日志"""
        frame = inspect.currentframe().f_back
        func_name = frame.f_code.co_name
        line_no = frame.f_lineno
        log_msg = f"{func_name}:{line_no} {log_msg}"
        self.logger.warning(log_msg)

    def error(self, log_msg):
        """记录ERROR级别的日志"""
        frame = inspect.currentframe().f_back
        func_name = frame.f_code.co_name
        line_no = frame.f_lineno
        log_msg = f"{func_name}:{line_no} {log_msg}"
        self.logger.error(log_msg)

    def critical(self, log_msg):
        """记录CRITICAL级别的日志"""
        frame = inspect.currentframe().f_back
        func_name = frame.f_code.co_name
        line_no = frame.f_lineno
        log_msg = f"{func_name}:{line_no} {log_msg}"
        self.logger.critical(log_msg)

    def __del__(self):
        """从日志器中移除所有处理器"""
        self.logger.removeHandler(self.handler)
        self.logger.removeHandler(self.err_handler)


if __name__ == "__main__":
    logger = MyLog(logger_name=__name__)
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    logger.critical("This is a critical message")
