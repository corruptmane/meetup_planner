from typing import NoReturn

from aiogram import Dispatcher

from app.handlers.private import (connect_to_community, create_community,
                                  first, last, list_communities, user_panel)


def setup(dispatcher: Dispatcher) -> NoReturn:
    first.setup(dispatcher)
    create_community.setup(dispatcher)
    connect_to_community.setup(dispatcher)
    list_communities.setup(dispatcher)
    user_panel.setup(dispatcher)
    last.setup(dispatcher)
