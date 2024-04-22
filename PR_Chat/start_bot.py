import asyncio
from aiogram import Bot, Dispatcher
from config_reader import config
from middlewares.check_sub import CheckSubscription, CheckWrongHref
from handlers import bot_messages



async def main():
    bot = Bot(config.bot_token.get_secret_value(), parse_mode='HTML')
    dp = Dispatcher()

    dp.message.middleware(CheckSubscription())
    dp.message.middleware(CheckWrongHref())

    dp.include_routers(
        bot_messages.router,
    )

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())