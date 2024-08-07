from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from modules.database.models.utility_models import TimeStampMixin
from modules.utilities.database import Base


class FarmingAdvice(Base, TimeStampMixin):
    __tablename__ = "farming_advice"
    id = Column(Integer, primary_key=True, index=True)
    crop_id = Column(Integer, ForeignKey("crop.id"))
    advice_type = Column(String)  # e.g., "crop selection", "pest management"
    advice = Column(Text)
    other_things_to_note = Column(Text)
    duration = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    crop = relationship("Crop")
