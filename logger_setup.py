import logging, sys, os
from loguru import logger

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

class Intercept(logging.Handler):
    def emit(self, record):
        logger.bind(module=record.name).log(record.levelno, record.getMessage())

def configure_logging():
    logger.remove()
    logger.add(
        sys.stdout,
        level=LOG_LEVEL,
        backtrace=True,
        diagnose=True,
        autocommit=True,       
        format="<green>{time:HH:mm:ss.SSS}</green> | "
               "<level>{level: <8}</level> | "
               "<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
               "<level>{message}</level>",
    )
    logging.basicConfig(handlers=[Intercept()], level=0)
