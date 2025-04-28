import logging, sys, os
from loguru import logger

def _setup():                           # func interna
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
    def sink_flush(msg):
        sys.stdout.write(msg)
        sys.stdout.flush()

    logger.remove()
    logger.add(
        sink_flush,
        level=LOG_LEVEL,
        backtrace=True,
        diagnose=True,
        colorize=False,
        format="<green>{time:HH:mm:ss.SSS}</green> | "
               "<level>{level:<8}</level> | "
               "<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
               "<level>{message}</level>",
    )

    class Intercept(logging.Handler):
        def emit(self, record):
            logger.bind(module=record.name).log(record.levelno, record.getMessage())

    logging.basicConfig(handlers=[Intercept()], level=0)

# ————— expõe a função que o index.py espera
def configure_logging():
    _setup()
