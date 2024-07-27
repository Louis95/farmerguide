from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float, Text, Enum, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from modules.utilities.database import Base
from modules.database.models.utility_models import TimeStampMixin


class UserRole(enum.Enum):
    OWNER = "owner"
    MANAGER = "manager"
    WORKER = "worker"
    CONSULTANT = "consultant"


# Pivot table for User-Farm many-to-many relationship
user_farm = Table('user_farm', Base,
                  Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
                  Column('farm_id', Integer, ForeignKey('farms.id'), primary_key=True),
                  Column('role', Enum(UserRole), nullable=False),
                  Column('created_at', DateTime(timezone=True), server_default=func.now()),
                  Column('updated_at', DateTime(timezone=True), onupdate=func.now()))


class User(Base, TimeStampMixin):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    farms = relationship("Farm", secondary=user_farm, back_populates="users")
