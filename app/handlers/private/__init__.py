from typing import NoReturn

from aiogram import Dispatcher

from app.handlers.private import connect_to_community, create_community, list_communities, start


def setup(dispatcher: Dispatcher) -> NoReturn:
    start.setup(dispatcher)
    create_community.setup(dispatcher)
    connect_to_community.setup(dispatcher)
    list_communities.setup(dispatcher)
