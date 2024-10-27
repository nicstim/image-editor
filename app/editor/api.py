from celery.result import AsyncResult
from fastapi import APIRouter, Depends, HTTPException, File, HTTPException, UploadFile
from fastapi.responses import FileResponse
from app.tasks import edit_image, celery_app
from app.utils.img_utils import upload_original_image
from app.utils.task_utils import create_user_task
from app.utils.zip_utils import get_zip
from app.utils.jwt_utils import get_current_user

router = APIRouter()


@router.post("/upload/")
async def upload_image(file: UploadFile = File(...), current_user: dict = Depends(get_current_user)):
    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(status_code=400, detail="JPG and PNG only.")
    file_url = await upload_original_image(file)
    task = edit_image.delay(image_url=file_url)
    await create_user_task(current_user.get("id"), str(task.id), file_url)
    return {"task_id": str(task.id), "original_image_url": file_url}


@router.get("/task/{task_id}/")
async def get_image_zip(task_id: str, current_user: dict = Depends(get_current_user)):
    zip_filename = await get_zip(task_id=task_id)
    return FileResponse(zip_filename, media_type='application/zip', filename=zip_filename)


@router.get("/status/{task_id}/")
async def get_task_status(task_id: str, current_user: dict = Depends(get_current_user)):
    task_result = AsyncResult(task_id, app=celery_app)
    return {
        "task_id": task_id,
        "status": task_result.status
    }
