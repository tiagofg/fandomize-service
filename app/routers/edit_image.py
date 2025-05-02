from fastapi import APIRouter, Depends, HTTPException
from loguru import logger

from app.exceptions.custom_exceptions import EmptyUrlError, InvalidStyleError
from app.models.edit_request import EditRequest
from app.models.edit_response import EditResponse
from app.services.image_service import process_image

router = APIRouter()

@router.post("/edit-image", response_model=EditResponse)
async def edit_image(request: EditRequest = Depends()):
    try:
        base64 = await process_image(
            request.uploaded_image.file,
            request.uploaded_image.filename,
            request.image_style,
            request.additional_details,
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
