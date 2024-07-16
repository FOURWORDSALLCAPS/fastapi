from typing import List

from fastapi import APIRouter, Depends

from app.schemes.animals import AnimalCreate, MilkRecordCreate, AnimalFilter, MilkRecord, Animal
from app.services.animals import AnimalService

router = APIRouter(prefix='/animals', tags=['Animals'])


@router.post('/create/', response_model=Animal)
async def create_animal(
    animal_data: AnimalCreate,
    animal_service: AnimalService = Depends()
):
    return await animal_service.create_or_update_animal(animal_data)


@router.post('/milk_record/create/', response_model=MilkRecord)
async def create_milk_record(
    milk_record_data: MilkRecordCreate,
    animal_service: AnimalService = Depends()
):
    return await animal_service.add_milk_record(milk_record_data)


@router.get('/all/', response_model=List[Animal])
async def get_animals(
    animal_filter: AnimalFilter = Depends(),
    animal_service: AnimalService = Depends()
):
    return await animal_service.get_all_animals(animal_filter)
