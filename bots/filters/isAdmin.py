from aiogram import types
from aiogram.utils.i18n import I18n
from aiogram.filters import BaseFilter
from config import OWNER_ID

class IsAdmin(BaseFilter):
    async def __call__(self, message: types.Message) -> bool:
        if message.from_user and message.from_user.id == OWNER_ID:
            return True
        await message.answer(
            "️You do not have access to this bot."
        )
        return False