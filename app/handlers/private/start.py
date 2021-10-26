from typing import NoReturn

from aiogram import Dispatcher
from aiogram.dispatcher.filters import Command
from aiogram.types import ContentType, Message
from asyncpg import UniqueViolationError

from app.utils import db_commands as commands


async def start_bot(msg: Message) -> NoReturn:
    await msg.answer(f"Hello, {msg.from_user.full_name}!")
    try:
        await commands.add_user(msg.from_user.id, msg.from_user.full_name, msg.from_user.get_mention())
    except UniqueViolationError:
        await commands.update_user_naming(msg.from_user.id, msg.from_user.full_name, msg.from_user.get_mention())


def setup(dispatcher: Dispatcher) -> NoReturn:
    dispatcher.register_message_handler(
        start_bot, Command("start"), content_types=ContentType.TEXT, state="*"
    )


__all__ = ["setup"]
