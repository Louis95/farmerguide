from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from modules.utilities.database import Base
from modules.database.models.utility_models import TimeStampMixin


class CropDisease(Base, TimeStampMixin):
    __tablename__ = "crop_diseases"
    id = Column(Integer, primary_key=True, index=True)
    farm_id = Column(Integer, ForeignKey("farms.id"))
    crop_type = Column(String)
    disease_name = Column(String)
    confidence = Column(Float)
    image_url = Column(String)
    treatment_recommendation = Column(Text)
    detected_at = Column(DateTime(timezone=True), server_default=func.now())
    farm = relationship("Farm", back_populates="crop_diseases")
