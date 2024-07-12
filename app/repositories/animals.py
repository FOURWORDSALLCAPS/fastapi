from typing import List
from datetime import datetime

from sqlalchemy import select

from app.engines.postgres_storage import PostgresEngine
from app.models.animals import AnimalDB, MilkRecordDB


class AnimalRepository:
    def __init__(self):
        self.db: PostgresEngine = PostgresEngine()

    async def get_animal_by_uuid(self, animal_uuid: int) -> AnimalDB | None:
        stmt = select(AnimalDB).where(AnimalDB.animal_uuid == animal_uuid)
        return await self.db.select_one(stmt)

    async def get_all_animals(self) -> List[AnimalDB]:
        stmt = select(AnimalDB)
        return await self.db.select_all(stmt)

    async def add_animal(self, animal: AnimalDB) -> AnimalDB:
        async with self.db.session() as session:
            async with session.begin():
                session.add(animal)
                await session.commit()
                await session.refresh(animal)
        return animal

    async def get_milk_records_by_animal_uuid(self, animal_uuid: int) -> List[MilkRecordDB]:
        stmt = select(MilkRecordDB).where(MilkRecordDB.animal_uuid == animal_uuid)
        return await self.db.select_all(stmt)

    async def add_milk_record(self, milk_record: MilkRecordDB) -> MilkRecordDB:
        async with self.db.session() as session:
            async with session.begin():
                session.add(milk_record)
                await session.commit()
                await session.refresh(milk_record)
        return milk_record

    async def get_milk_record_by_date(self, animal_uuid: int, record_date: datetime) -> MilkRecordDB | None:
        stmt = select(MilkRecordDB).where(
            MilkRecordDB.animal_uuid == animal_uuid,
            MilkRecordDB.record_date == record_date
        )
        return await self.db.select_one(stmt)
