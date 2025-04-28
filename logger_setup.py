from loguru import logger
import sys
import os

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO") 

def configure_logging():
    logger.remove() 
    logger.add(
        sys.stdout,
        level=LOG_LEVEL,
        backtrace=True,   
        diagnose=True,      
        enqueue=True,        
        format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
               "<level>{level: <8}</level> | "
               "<cyan>{name}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    )

    class InterceptHandler:
        def emit(self, record):
            logger_opt = logger.bind(module=record.name)
            logger_opt.log(record.levelno, record.getMessage())

    import logging
    logging.basicConfig(handlers=[InterceptHandler()], level=0)

configure_logging()
