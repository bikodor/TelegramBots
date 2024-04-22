from aiogram import types
from aiogram.filters import Filter


class IsDice(Filter):
    async def check(self, message: types.Message) -> bool:
        return message.dice is not None