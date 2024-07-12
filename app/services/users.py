from http import HTTPStatus
from uuid import UUID

from fastapi import HTTPException

from app.repositories.user import UserRepository
from app.schemes.users import User, UserChangePassword, UserCreate
from app.services.auth import AuthService


class UserService:
    def __init__(self):
        self.user_repository: UserRepository = UserRepository()

    # async def create_or_update_user(self, user_data: UserCreate) -> User:
    #     if user_data.password:
    #         user_data.password = AuthService.hash_password(user_data.password)
    #
    #     user_dict = user_data.model_dump(exclude_none=True)
    #     user_data = await self.user_repository.create_or_update_user(user_dict)
    #     return User(**user_data.__dict__)

    async def change_password(self, user_uuid: UUID, user_password_data: UserChangePassword) -> bool:
        user_dict: User = await self.user_repository.get_user_by_uuid(user_uuid)

        current_password_hash = AuthService.hash_password(user_password_data.password)
        if user_dict.password != current_password_hash:
            raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail='Passwords do not match')

        await self.user_repository.update_user(
            user_uuid, {'password': AuthService.hash_password(user_password_data.password_new)}
        )

        return True
