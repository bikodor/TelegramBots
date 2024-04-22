import asyncio
from aiogram import Bot, Dispatcher
from callbacks import profile, game_dice, game_casino, game_roulette, game_blackjack
from config_reader import config
from middlewares.antiflood import AntiFloodMiddleware
from handlers import user_commands

async def main():
    bot = Bot(config.bot_token.get_secret_value(), parse_mode='HTML')
    dp = Dispatcher()

    dp.message.middleware(AntiFloodMiddleware())

    dp.include_routers(
        user_commands.router,
        profile.router,
        game_dice.router,
        game_casino.router,
        game_roulette.router,
        game_blackjack.router
    )

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())