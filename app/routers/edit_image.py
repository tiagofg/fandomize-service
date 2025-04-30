from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from loguru import logger

from exceptions.custom_exceptions import EmptyUrlError, InvalidStyleError
from models.edit_response import EditResponse
from services.image_service import process_image

router = APIRouter()

@router.post("/edit_image", response_model=EditResponse)
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
