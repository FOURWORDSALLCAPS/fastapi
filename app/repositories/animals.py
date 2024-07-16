from typing import List
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert

from app.engines.postgres_storage import PostgresEngine
from app.models.animals import AnimalDB, MilkRecordDB


class AnimalRepository:
    def __init__(self):
        self.db: PostgresEngine = PostgresEngine()

    async def animal_exists(self, animal_number: int) -> bool:
        result = await self.db.execute(
            select(AnimalDB).where(AnimalDB.animal_number == animal_number)
        )
        return result is not None

    async def get_animal_by_uuid(self, animal_uuid: int) -> AnimalDB | None:
        stmt = select(AnimalDB).where(AnimalDB.animal_uuid == animal_uuid)
        return await self.db.select_one(stmt)

    async def get_all_animals(self) -> List[AnimalDB]:
        stmt = select(AnimalDB)
        return await self.db.select_all(stmt)

    async def add_animal(self, animal: AnimalDB) -> AnimalDB:
        stmt = insert(AnimalDB).values(
            animal_uuid=animal.animal_uuid,
            animal_number=animal.animal_number,
            gender=animal.gender,
            birth_date=animal.birth_date
        ).returning(AnimalDB)

        result = await self.db.execute(stmt)
        if result:
            return animal

    async def get_milk_records_by_animal_uuid(self, animal_uuid: int) -> List[MilkRecordDB]:
        stmt = select(MilkRecordDB).where(MilkRecordDB.animal_uuid == animal_uuid)
        return await self.db.select_all(stmt)

    async def add_milk_record(self, milk_record: MilkRecordDB) -> MilkRecordDB:
        stmt = insert(MilkRecordDB).values(
            record_uuid=milk_record.record_uuid,
            animal_uuid=milk_record.animal_uuid,
            milk_amount=milk_record.milk_amount,
            record_date=milk_record.record_date
        ).returning(MilkRecordDB)

        result = await self.db.execute(stmt)
        if result:
            return milk_record

    async def get_milk_record_by_date(self, animal_uuid: int, record_date: datetime) -> MilkRecordDB | None:
        stmt = select(MilkRecordDB).where(
            MilkRecordDB.animal_uuid == animal_uuid,
            MilkRecordDB.record_date == record_date
        )
        return await self.db.select_one(stmt)
