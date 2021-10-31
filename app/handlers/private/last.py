from typing import NoReturn

from aiogram import Dispatcher
from aiogram.types import Message, CallbackQuery, ContentType


async def non_tracking_message(msg: Message) -> NoReturn:
    await msg.answer("Non tracking message or you do something wrong")


async def non_tracking_callback_query(call: CallbackQuery) -> NoReturn:
    await call.answer("Non tracking callback")


def setup(dispatcher: Dispatcher) -> NoReturn:
    dispatcher.register_message_handler(non_tracking_message, content_types=ContentType.ANY, state="*")
    dispatcher.register_callback_query_handler(non_tracking_callback_query, state="*")
