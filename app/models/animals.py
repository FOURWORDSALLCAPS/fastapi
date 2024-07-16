from enum import Enum
from uuid import uuid4

from sqlalchemy import ForeignKey, Integer, String, Date, Float, UniqueConstraint, CheckConstraint, UUID
from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime

from app.models.base import BaseDB


class GenderEnum(str, Enum):
    COW = "cow"
    BULL = "bull"


class AnimalDB(BaseDB):
    __tablename__ = 'animals'  # noqa
    animal_uuid: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    animal_number: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    gender: Mapped[GenderEnum] = mapped_column(SQLAlchemyEnum(GenderEnum), nullable=False)
    birth_date: Mapped[datetime] = mapped_column(Date, nullable=False)

    milk_records = relationship("MilkRecordDB", back_populates="animal")


class MilkRecordDB(BaseDB):
    __tablename__ = 'milk_records'  # noqa
    record_uuid: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    animal_uuid: Mapped[UUID] = mapped_column(UUID, ForeignKey('animals.animal_uuid'), nullable=False)
    milk_amount: Mapped[float] = mapped_column(Float, nullable=False)
    record_date: Mapped[datetime] = mapped_column(Date, nullable=False, default=datetime.utcnow)

    animal = relationship("AnimalDB", back_populates="milk_records")
