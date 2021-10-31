from typing import NoReturn

from aiogram import Dispatcher

from app.handlers.private import (first, create_community, connect_to_community, list_communities, user_panel, last)


def setup(dispatcher: Dispatcher) -> NoReturn:
    first.setup(dispatcher)
    create_community.setup(dispatcher)
    connect_to_community.setup(dispatcher)
    list_communities.setup(dispatcher)
    user_panel.setup(dispatcher)
    last.setup(dispatcher)
