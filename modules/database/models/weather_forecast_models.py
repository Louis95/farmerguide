from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from modules.utilities.database import Base


class WeatherForecast(Base):
    __tablename__ = "weather_forecasts"
    id = Column(Integer, primary_key=True, index=True)
    farm_id = Column(Integer, ForeignKey("farms.id"))
    date = Column(DateTime)
    temperature = Column(Float)
    humidity = Column(Float)
    precipitation = Column(Float)
    wind_speed = Column(Float)
    forecast_type = Column(String)  # e.g., "daily", "hourly"
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    farm = relationship("Farm")
