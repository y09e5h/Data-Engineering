import logging

logging.basicConfig(level=logging.INFO, filename="app.log",
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logging.info("This is info message")
logging.warning("This is warning message")
logging.error("This is error message")
logging.critical("This is critical message")
logging.debug("This is debug message")

logger = logging.getLogger("TESTLOGGER")
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler = logging.FileHandler("app.log")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.critical("This is critical message")
logging.info("This is info message")
logging.warning("This is warning message")
logging.error("This is error message")
logging.critical("This is critical message")