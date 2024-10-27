import asyncio
import os

from celery import Celery
from app.utils.img_utils import rotate_image, save_image_task, grayscale_image, resize_image, make_url_for_download
from app.config import settings

celery_app = Celery(
    "tasks",
    broker=os.getenv("CELERY_BROKER_URL", "redis://redis:6379/0"),
    backend=os.getenv("CELERY_RESULT_BACKEND", "redis://redis:6379/0")
)


@celery_app.task(bind=True)
def edit_image(self, image_url: str):
    task_id = str(self.request.id)
    asyncio.run(save_image_task(url=image_url, task_id=task_id))
    url_for_download = make_url_for_download(image_url)
    asyncio.run(rotate_image(original_url=url_for_download,
                             task_id=task_id))
    asyncio.run(grayscale_image(original_url=url_for_download,
                                task_id=task_id))
    asyncio.run(resize_image(original_url=url_for_download,
                             task_id=task_id))
