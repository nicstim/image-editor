from sqlalchemy import Column, String, DateTime, create_engine, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

from sqlalchemy.orm import sessionmaker, relationship

from app.config import settings

Base = declarative_base()
engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)

    task = relationship("UserTask", back_populates="user")


class ImageTask(Base):
    __tablename__ = "image_tasks"

    id = Column(String, primary_key=True, index=True)
    task_id = Column(String, index=True)
    img_link = Column(String, unique=True, index=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class UserTask(Base):
    __tablename__ = "user_tasks"

    id = Column(String, primary_key=True, index=True)
    task_id = Column(String)
    user_id = Column(String, ForeignKey('users.id'), nullable=False)
    image = Column(String, unique=True, index=True, nullable=False)

    user = relationship("User", back_populates="task")
