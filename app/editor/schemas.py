from pydantic import BaseModel


class UploadResponse(BaseModel):
    task_id: str
    original_image_url: str
