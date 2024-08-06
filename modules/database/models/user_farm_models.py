import enum

from sqlalchemy import Column, DateTime, Enum, Float, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from modules.database.models.utility_models import TimeStampMixin
from modules.utilities.database import Base


class UserRole(enum.Enum):
    OWNER = "owner"
    MANAGER = "manager"
    WORKER = "worker"
    CONSULTANT = "consultant"


# Pivot table for User-Farm many-to-many relationship
user_farm = Table(
    "user_farm",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("farm_id", Integer, ForeignKey("farms.id"), primary_key=True),
    Column("role", Enum(UserRole), nullable=False),
    Column("created_at", DateTime(timezone=True), server_default=func.now()),
    Column("updated_at", DateTime(timezone=True), onupdate=func.now()),
)


class User(Base, TimeStampMixin):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    farms = relationship("Farm", secondary=user_farm, back_populates="users")


class Farm(Base, TimeStampMixin):
    __tablename__ = "farms"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    location = Column(String)
    size = Column(Float)  # in hectares
    users = relationship("User", secondary=user_farm, back_populates="farms")
    crop_diseases = relationship("CropDisease", back_populates="farm")
    soil_health_records = relationship("SoilHealth", back_populates="farm")
    crop_diagnosis = relationship("CropDiagnosis", back_populates="farm")
    crop = relationship("Crop", back_populates="farm")
