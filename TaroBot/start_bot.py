import asyncio
from aiogram import Bot, Dispatcher
from config_reader import config
from middlewares.antiflood import AntiFloodMiddleware
import user_commands

async def main():
    bot = Bot(config.bot_token.get_secret_value(), parse_mode='HTML')
    dp = Dispatcher()

    dp.message.middleware(AntiFloodMiddleware())

    dp.include_routers(
        user_commands.router,
    )

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())