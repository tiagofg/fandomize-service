import sys, logging, os
from loguru import logger

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

def _sink_with_flush(message):
    sys.stdout.write(message)
    sys.stdout.flush()                 #  <-- descarrega imediatamente

logger.remove()
logger.add(
    _sink_with_flush,                 # usa função que força flush
    level=LOG_LEVEL,
    backtrace=True,
    diagnose=True,
    colorize=False,
    format="<green>{time:HH:mm:ss.SSS}</green> | "
           "<level>{level: <8}</level> | "
           "<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
           "<level>{message}</level>",
)

class Intercept(logging.Handler):
    def emit(self, record):
        logger.bind(module=record.name).log(record.levelno, record.getMessage())

logging.basicConfig(handlers=[Intercept()], level=0)
