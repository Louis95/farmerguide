from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from modules.utilities.database import Base
from modules.database.models.utility_models import TimeStampMixin


class FarmingAdvice(Base, TimeStampMixin):
    __tablename__ = "farming_advice"
    id = Column(Integer, primary_key=True, index=True)
    farm_id = Column(Integer, ForeignKey("farms.id"))
    advice_type = Column(String)  # e.g., "crop selection", "pest management"
    content = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    farm = relationship("Farm")
