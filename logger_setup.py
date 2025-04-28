import logging
import sys
from loguru import logger
import os

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

class InterceptHandler(logging.Handler):
    """Encaminha logs da stdlib para o Loguru."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  

    def emit(self, record: logging.LogRecord):
        logger_opt = logger.bind(module=record.name)
        logger_opt.log(record.levelno, record.getMessage())

def configure_logging():
    logger.remove()          
    logger.add(              
        sys.stdout,
        level=LOG_LEVEL,
        backtrace=True,
        diagnose=True,
        format=(
            "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{line}</cyan> - "
            "<level>{message}</level>"
        ),
    )

    # Redireciona toda a stdlib para o Loguru
    logging.basicConfig(handlers=[InterceptHandler()], level=0)

# configure no import de módulo principal
configure_logging()
