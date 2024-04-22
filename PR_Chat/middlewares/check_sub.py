from aiogram import BaseMiddleware
from typing import Callable, Awaitable, Dict, Any

from aiogram.enums import ParseMode
from aiogram.types import Message
from keyboards.inline import sub_channel

import re

def contains_url(text):
    url_pattern1 = r'(https?://)?([-\w]+\.)+[\w-]+(/[-\w./?%&=]*)?'
    url_pattern2 = r'(http?://)?([-\w]+\.)+[\w-]+(/[-\w./?%&=]*)?'
    match1 = re.search(url_pattern1, text)
    match2 = re.search(url_pattern2, text)

    # Проверяем, есть ли совпадение и не содержит ли оно 't.me'
    return (bool(match1) or bool(match2)) and ('t.me' not in match1.group(0) or 't.me' not in match1.group(0))


class CheckSubscription(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        bot = data.get('bot')
        chat_member = await event.bot.get_chat_member('@Nastya_for_every_day', event.from_user.id)

        if chat_member.status == 'left':
            await bot.delete_message(chat_id=-1002055009883, message_id=event.message_id)
            user_mention = f"[{event.from_user.first_name}](tg://user?id={event.from_user.id})"
            text = f"<a href='tg://user?id={event.from_user.id}'>{event.from_user.first_name}</a>, подпишись на канал @Nastya_for_every_day, чтобы я пропускал ваши сообщения в чат!"

            # Отправляем сообщение с parse_mode=Markdown, чтобы ссылка работала
            await event.answer(text, reply_markup=sub_channel, parse_mode=ParseMode.HTML)

        else:
            return await handler(event, data)

class CheckWrongHref(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        bot = data.get('bot')

        if contains_url(event.text):
            await bot.delete_message(chat_id=-1002055009883, message_id=event.message_id)
            text = f"<a href='tg://user?id={event.from_user.id}'>{event.from_user.first_name}</a>, в вашем сообщении были замечены подозрительные ссылки, поэтому сообщение было удалено.\nПожалуйста, используйте ссылки, которые ведут на телеграмм канал."

            # Отправляем сообщение с parse_mode=Markdown, чтобы ссылка работала
            await event.answer(text, reply_markup=sub_channel, parse_mode=ParseMode.HTML)

        else:
            return await handler(event, data)