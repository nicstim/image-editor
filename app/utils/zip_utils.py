import os
import shutil
from zipfile import ZipFile

import requests

from app.models import SessionLocal, ImageTask
from app.utils.img_utils import make_url_for_download


async def get_zip(task_id: str):
    db = SessionLocal()
    zip_filename = f"{task_id}_images.zip"
    images = db.query(ImageTask).filter(ImageTask.task_id == task_id).all()
    os.makedirs("temp_images", exist_ok=True)
    for image in images:
        response = requests.get(make_url_for_download(image.img_link))
        with open(f"temp_images/{image.img_link.split('/')[-1]}", "wb") as f:
            f.write(response.content)
    with ZipFile(zip_filename, 'w') as zipf:
        for image in images:
            zipf.write(f"temp_images/{image.img_link.split('/')[-1]}", arcname=f"{image.img_link.split('/')[-1]}")
    shutil.rmtree("temp_images")

    return zip_filename
