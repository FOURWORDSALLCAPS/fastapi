from typing import NoReturn
from uuid import UUID

from sqlalchemy import func, select, update
from sqlalchemy.dialects.postgresql import insert

from app.engines.postgres_storage import PostgresEngine
from app.models.users import UserDB


class UserRepository:
    def __init__(self):
        self.db: PostgresEngine = PostgresEngine()

    async def get_user_by_uuid(self, user_uuid: UUID) -> UserDB | None:
        stmt = select(UserDB).where(UserDB.user_uuid == user_uuid)
        return await self.db.select_one(stmt)

    async def get_user_by_username(self, username: str) -> UserDB | None:
        stmt = select(UserDB).where(UserDB.username == username)
        return await self.db.select_one(stmt)

    # async def create_or_update_user(self, user_data: dict) -> UserDB:
    #     stmt = (
    #         insert(UserDB)
    #         .values(**user_data)
    #         .on_conflict_do_update(
    #             index_elements=UserDB.__table__.primary_key.columns,
    #             set_={**user_data, UserDB.update_date: func.now()},
    #         )
    #         .returning(UserDB)
    #     )
    #     return await self.db.execute(stmt)

    async def update_user(self, user_uuid: UUID, user_data: dict) -> NoReturn:
        stmp = update(UserDB).where(UserDB.user_uuid == user_uuid).values(**user_data)
        await self.db.execute(stmp, no_return=True)
