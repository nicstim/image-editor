import uuid

from app.models import UserTask, SessionLocal


async def create_user_task(user_id: str, task_id: str, image_url: str) -> None:
    new_image = UserTask(
        id=str(uuid.uuid4()),
        task_id=task_id,
        user_id=user_id,
        image=image_url
    )
    db = SessionLocal()
    db.add(new_image)
    db.commit()
    db.refresh(new_image)
