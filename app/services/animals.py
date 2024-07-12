from http import HTTPStatus
from datetime import datetime, timedelta
from typing import List

from fastapi import HTTPException

from app.repositories.animals import AnimalRepository
from app.schemes.animals import AnimalCreate, MilkRecordCreate, AnimalFilter
from app.models.animals import AnimalDB, MilkRecordDB


class AnimalService:
    def __init__(self):
        self.animal_repository: AnimalRepository = AnimalRepository()

    async def create_or_update_animal(self, animal_data: AnimalCreate) -> AnimalDB:
        animal_dict = animal_data.dict(exclude_none=True)
        animal = AnimalDB(**animal_dict)
        return await self.animal_repository.add_animal(animal)

    async def add_milk_record(self, milk_record_data: MilkRecordCreate) -> MilkRecordDB:
        animal = await self.animal_repository.get_animal_by_uuid(milk_record_data.animal_uuid)
        if not animal or animal.gender == 'bull':
            raise HTTPException(
                status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
                detail="Cannot add milk record for a bull or non-existent animal"
            )

        existing_record = await self.animal_repository.get_milk_record_by_date(
            milk_record_data.animal_uuid,
            milk_record_data.record_date
        )
        if existing_record:
            raise HTTPException(
                status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
                detail="Milk record for this animal already exists for the given date"
            )

        milk_record_dict = milk_record_data.dict(exclude_none=True)
        milk_record = MilkRecordDB(**milk_record_dict)
        return await self.animal_repository.add_milk_record(milk_record)

    async def get_all_animals(self, animal_filter: AnimalFilter) -> List[AnimalDB]:
        animals = await self.animal_repository.get_all_animals()
        filtered_animals = []

        for animal in animals:
            if animal_filter.gender and animal.gender != animal_filter.gender:
                continue
            if animal_filter.min_age is not None:
                min_birth_date = datetime.now().date() - timedelta(days=animal_filter.min_age * 365)
                if animal.birth_date > min_birth_date:
                    continue
            if animal_filter.max_age is not None:
                max_birth_date = datetime.now().date() - timedelta(days=animal_filter.max_age * 365)
                if animal.birth_date < max_birth_date:
                    continue
            filtered_animals.append(animal)

        return filtered_animals
