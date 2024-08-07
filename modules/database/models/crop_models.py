from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from modules.database.models.utility_models import TimeStampMixin
from modules.utilities.database import Base


class Crop(Base, TimeStampMixin):
    __tablename__ = "crops"
    id = Column(Integer, primary_key=True, index=True)
    farm_id = Column(Integer, ForeignKey("farms.id", ondelete="CASCADE"))
    crop_type = Column(String)  # e.g., "banana", "maize"
    notes = Column(Text)
    planted_on = Column(DateTime(timezone=True), server_default=func.now())
    harvested_on = Column(DateTime(timezone=True), server_default=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    diagnoses = relationship("CropDiagnosis", back_populates="crop", cascade="all, delete-orphan")
    diseases = relationship("CropDisease", back_populates="crop", cascade="all, delete-orphan")
    farm = relationship("Farm")
