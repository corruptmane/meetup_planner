from typing import NoReturn

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import Message, ContentType

from app.keyboards.inline.list_communities_kb import created_communities_kb
from app.utils import db_commands as commands


async def cmd_list_created_communities(msg: Message, state: FSMContext) -> NoReturn:
    communities = await commands.get_communities_by_creator_id(msg.from_user.id)
    if not communities:
        await msg.answer("You didn't created any community yet. Create community by typing /create, "
                         "or hit / to see available commands")
        return
    community_titles = [tuple(community.id, community.title) for community in communities]
    await msg.answer("Here you can see all communities created by you. You can enter community control-panel by "
                     "hitting on one of community titles", reply_markup=created_communities_kb(community_titles))
    await state.set_state("created_communities_list")


async def cmd_list_communities_participates_in(msg: Message, state: FSMContext) -> NoReturn:  # TODO: end-up that handler
    communities = await commands.get_communities_participates_in()
    if not communities:
        await msg.answer("You didn't connected to any community. If you have invite code, "
                         "type /connect <code>invite_code</code>")
        return


def setup(dispatcher: Dispatcher) -> NoReturn:
    dispatcher.register_message_handler(cmd_list_created_communities, Command("created"),
                                        content_types=ContentType.TEXT)
