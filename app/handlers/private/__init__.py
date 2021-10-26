from typing import NoReturn

from aiogram import Dispatcher

from app.handlers.private import connect_to_community, create_community, start


def setup(dispatcher: Dispatcher) -> NoReturn:
    start.setup(dispatcher)
    create_community.setup(dispatcher)
    connect_to_community.setup(dispatcher)
