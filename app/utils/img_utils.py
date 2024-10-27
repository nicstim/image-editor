import io
import logging
import uuid

import requests
from PIL import Image

from fastapi import UploadFile
from app.minio_config import minio_client
from app.config import settings
from app.models import ImageTask, SessionLocal


def make_url_for_download(url: str) -> str:
    url_for_download = url.replace(settings.MINIO_URL, settings.MINIO_ENDPOINT)
    if "http" not in url_for_download:
        url_for_download = "http://" + url_for_download

    return url_for_download


async def save_image_task(url: str, task_id: str) -> None:
    new_image = ImageTask(
        id=str(uuid.uuid4()),
        task_id=task_id,
        img_link=url
    )
    db = SessionLocal()
    db.add(new_image)
    db.commit()
    db.refresh(new_image)


async def resize_image(original_url: str, task_id: str) -> None:
    response = requests.get(original_url)
    img = Image.open(io.BytesIO(response.content))
    resized_img = img.resize((int(img.width * 2), int(img.height * 2)), Image.Resampling.LANCZOS)
    img_bytes = io.BytesIO()
    resized_img.save(img_bytes, format='PNG' if resized_img.mode == 'RGBA' else 'JPEG')
    img_bytes.seek(0)
    file_extension = original_url.split(".")[-1]
    unique_filename = f"{uuid.uuid4()}_scaled.{file_extension}"
    minio_client.put_object(
        settings.MINIO_BUCKET_NAME,
        unique_filename,
        data=img_bytes,
        length=img_bytes.getbuffer().nbytes,
        content_type="image/png" if resized_img.mode == 'RGBA' else "image/jpeg"
    )
    await save_image_task(url=f"{settings.MINIO_URL}/{settings.MINIO_BUCKET_NAME}/{unique_filename}", task_id=task_id)


async def grayscale_image(original_url: str, task_id: str) -> None:
    response = requests.get(original_url)
    img = Image.open(io.BytesIO(response.content))
    grayscale_img = img.convert("L")
    img_bytes = io.BytesIO()
    grayscale_img.save(img_bytes, format='PNG' if grayscale_img.mode == 'RGBA' else 'JPEG')
    img_bytes.seek(0)
    file_extension = original_url.split(".")[-1]
    unique_filename = f"{uuid.uuid4()}_gray.{file_extension}"
    minio_client.put_object(
        settings.MINIO_BUCKET_NAME,
        unique_filename,
        data=img_bytes,
        length=img_bytes.getbuffer().nbytes,
        content_type="image/png" if grayscale_img.mode == 'RGBA' else "image/jpeg"
    )
    await save_image_task(url=f"{settings.MINIO_URL}/{settings.MINIO_BUCKET_NAME}/{unique_filename}", task_id=task_id)


async def rotate_image(original_url: str, task_id: str) -> None:
    response = requests.get(original_url)
    img = Image.open(io.BytesIO(response.content))
    rotated_img = img.rotate(90, expand=True)
    img_bytes = io.BytesIO()
    rotated_img.save(img_bytes, format='PNG' if rotated_img.mode == 'RGBA' else 'JPEG')
    img_bytes.seek(0)
    file_extension = original_url.split(".")[-1]
    unique_filename = f"{uuid.uuid4()}_rotated.{file_extension}"
    minio_client.put_object(
        settings.MINIO_BUCKET_NAME,
        unique_filename,
        data=img_bytes,
        length=img_bytes.getbuffer().nbytes,
        content_type="image/png" if rotated_img.mode == 'RGBA' else "image/jpeg"
    )
    await save_image_task(url=f"{settings.MINIO_URL}/{settings.MINIO_BUCKET_NAME}/{unique_filename}", task_id=task_id)


async def upload_original_image(image_file: UploadFile) -> str:
    file_extension = image_file.filename.split(".")[-1]
    unique_filename = f"{uuid.uuid4()}_original.{file_extension}"
    image_data = await image_file.read()

    try:
        buffer = io.BytesIO(image_data)
        minio_client.put_object(
            settings.MINIO_BUCKET_NAME,
            unique_filename,
            data=buffer,
            length=len(image_data),
            content_type=image_file.content_type,
        )
    except Exception as exc:
        logging.error(f"Upload original image error: {exc}")
    return f"{settings.MINIO_URL}/{settings.MINIO_BUCKET_NAME}/{unique_filename}"
