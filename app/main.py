from fastapi import FastAPI

from app.user.api import router as user_router
from app.editor.api import router as editor_router

app = FastAPI()

app.include_router(user_router, prefix="/api/v1/user")
app.include_router(editor_router, prefix="/api/v1/editor")
