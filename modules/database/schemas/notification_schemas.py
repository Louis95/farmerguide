"""Notification schema module."""
from datetime import datetime

from pydantic import BaseModel


class NotificationBase(BaseModel):
    message: str
    notification_type: str


class NotificationCreate(NotificationBase):
    user_id: int


class NotificationInDB(NotificationBase):
    id: int
    user_id: int
    is_read: bool
    created_at: datetime

    class Config:
        from_attributes = True
