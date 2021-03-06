from typing import NoReturn

from aiogram import Dispatcher
from aiogram.types import BotCommand


async def setup_default_commands(dispatcher: Dispatcher) -> NoReturn:
    await dispatcher.bot.set_my_commands(
        [
            BotCommand("start", "Start bot"),
            BotCommand("help", "Help menu"),
            BotCommand("create", "Create a new community"),
            BotCommand("connect", "Connect to community (Instantly if invite code provided). "
                                  "Syntax: /connect [invite code]"),
            BotCommand("created", "List created communities to manage them"),
            BotCommand("connected", "List connected communities to enter user-panel")
        ]
    )
