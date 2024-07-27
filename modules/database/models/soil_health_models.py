from sqlalchemy import Column, Integer, ForeignKey, DateTime, Float, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from modules.utilities.database import Base


class SoilHealth(Base):
    __tablename__ = "soil_health"
    id = Column(Integer, primary_key=True, index=True)
    farm_id = Column(Integer, ForeignKey("farms.id"))
    ph_level = Column(Float)
    nitrogen_level = Column(Float)
    phosphorus_level = Column(Float)
    potassium_level = Column(Float)
    organic_matter = Column(Float)
    analysis_date = Column(DateTime(timezone=True), server_default=func.now())
    recommendations = Column(Text)
    farm = relationship("Farm", back_populates="soil_health_records")
