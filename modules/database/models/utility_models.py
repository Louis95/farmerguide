"""Models defining various utility models, including Enums and utility Mixins."""
import enum

from sqlalchemy import Column, func
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import declarative_mixin


@declarative_mixin
class TimeStampMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    created_at = Column(TIMESTAMP(precision=6), server_default=func.now())
    updated_at = Column(TIMESTAMP(precision=6), server_default=func.now(), onupdate=func.now())
