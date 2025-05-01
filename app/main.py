from fastapi import FastAPI, Request
from loguru import logger

from app.core.logger_setup import configure_logging
from app.routers import edit_image

configure_logging()
app = FastAPI(title="Image Editor API")

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.bind(path=request.url.path, method=request.method).info("↗️  request received")

    try:
        response = await call_next(request)
        logger.bind(status=response.status_code).info("↘️  response sent")

        return response
    except Exception:
        logger.exception("Unhandled error processing request")
        raise

app.include_router(edit_image.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
