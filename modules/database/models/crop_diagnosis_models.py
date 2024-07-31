from sqlalchemy import (
    ARRAY,
    BOOLEAN,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from modules.database.models.utility_models import TimeStampMixin
from modules.utilities import Base


class CropDiagnosis(Base, TimeStampMixin):
    __tablename__ = "crop_diagnosis"
    id = Column(Integer, primary_key=True, index=True)
    farm_id = Column(Integer, ForeignKey("farms.id"))
    is_infected = Column(BOOLEAN)
    crop_name = Column(String)
    crop_type = Column(String)
    disease_name = Column(String)
    treatment_recommendation = Column(Text)
    how_to_identify_disease = Column(Text)
    causes_of_disease = Column(Text)
    other_things_to_note = Column(Text)
    confidence_level = Column(Float)
    images = Column(ARRAY(String))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    farm = relationship("Farm", back_populates="crop_diagnosis")
