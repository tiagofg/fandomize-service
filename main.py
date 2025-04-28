import uvicorn

from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from pydantic import BaseModel
from service import EmptyUrlError, process_image, InvalidStyleError

app = FastAPI()

class EditResponse(BaseModel):
    image: str

@app.post("/edit-image/", response_model=EditResponse)
async def edit_image(
    uploaded_image: UploadFile = File(...),
    image_style: str = Form(...),
    additional_details: str = Form(...),
):
    """
    Controller que delega a lógica para service.process_image.
    """
    try:
        base64 = await process_image(
            uploaded_image.file,
            uploaded_image.filename,
            image_style,
            additional_details,
        )

    except InvalidStyleError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except EmptyUrlError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {e}")

    return EditResponse(image=base64)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
