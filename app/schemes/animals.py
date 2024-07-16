from typing import Optional, List
from datetime import datetime
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, validator


class MilkRecord(BaseModel):
    animal_uuid: UUID
    milk_amount: float
    record_date: datetime

    class Config:
        orm_mode = True


class Animal(BaseModel):
    animal_uuid: UUID
    animal_number: str
    gender: str
    birth_date: datetime

    @validator('gender')
    def validate_gender(cls, value):
        if value not in {'cow', 'bull'}:
            raise ValueError('gender must be either `cow` or `bull`')
        return value

    class Config:
        orm_mode = True


class AnimalCreate(BaseModel):
    animal_number: str
    gender: str
    birth_date: datetime

    @validator('gender')
    def validate_gender(cls, value):
        if value not in {'cow', 'bull'}:
            raise ValueError('gender must be either `cow` or `bull`')
        return value

    class Config:
        orm_mode = True


class MilkRecordCreate(BaseModel):
    animal_uuid: UUID
    milk_amount: float
    record_date: datetime

    class Config:
        orm_mode = True


class AnimalFilter(BaseModel):
    gender: Optional[str] = None
    min_age: Optional[int] = None
    max_age: Optional[int] = None
