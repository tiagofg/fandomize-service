from fastapi import FastAPI, Request, UploadFile, File, Form, HTTPException
from loguru import logger
from pydantic import BaseModel
from logger_setup import configure_logging
from service import EmptyUrlError, process_image, InvalidStyleError

configure_logging()
app = FastAPI()

class EditResponse(BaseModel):
    image: str

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

@app.post("/edit-image/", response_model=EditResponse)
async def edit_image(
    uploaded_image: UploadFile = File(...),
    image_style: str = Form(...),
    additional_details: str = Form(...)
):
    try:
        base64 = await process_image(
            uploaded_image.file,
            uploaded_image.filename,
            image_style,
            additional_details,
        )
    except InvalidStyleError as e:
        logger.error(f"Estilo inválido: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except EmptyUrlError as e:
        logger.error(f"Erro ao processar imagem: {e}")
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Erro interno: {e}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {e}")

    return EditResponse(image=base64)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
