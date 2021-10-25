from typing import NoReturn

from aiogram import Dispatcher

from app.handlers.private import create_community, start


def setup(dispatcher: Dispatcher) -> NoReturn:
    start.setup(dispatcher)
    create_community.setup(dispatcher)
