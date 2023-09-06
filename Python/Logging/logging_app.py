import logging
import os

logger = logging.getLogger("my_logger")

console_handler = logging.StreamHandler()
file_handler = logging.FileHandler(os.path.basename(__file__) + ".log")

logger.setLevel(logging.DEBUG)

console_handler.setLevel(logging.WARNING)
file_handler.setLevel(logging.INFO)

console_formatter = logging.Formatter(fmt = "%(asctime)s %(levelname)s %(filename)s:%(lineno)d %(message)s")

file_formatter = logging.Formatter(fmt = "%(asctime)s %(levelname)s %(filename)s:%(lineno)d %(message)s",
                                      datefmt="%Y-%m-%d HH:MM:SS")

console_handler.setFormatter(console_formatter)
file_handler.setFormatter(file_formatter)

logger.handlers = [console_handler,file_handler]


logger.debug("This is Debug Message")
logger.info("This is Info Message")
logger.warning("This is Warning Message")
logger.error("This is Error Message")
logger.critical("This is Critical Message")