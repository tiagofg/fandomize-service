from fastapi import UploadFile, File, Form

class EditRequest:
    def __init__(
        self,
        uploaded_image: UploadFile = File(...),
        image_style: str       = Form(...),
        additional_details: str = Form(...)
    ):
        self.uploaded_image     = uploaded_image
        self.image_style        = image_style
        self.additional_details = additional_details
