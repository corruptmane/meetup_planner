from typing import NoReturn

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import CallbackQuery, ContentType, Message

from app.keyboards.inline import list_communities_kb as kb
from app.utils import db_commands as commands


async def cmd_list_created_communities(msg: Message, state: FSMContext) -> NoReturn:
    communities = await commands.get_communities_by_creator_id(msg.from_user.id)
    if not communities:
        await msg.answer("You didn't created any community yet. Create community by typing /create, "
                         "or hit / to see available commands")
        return
    communities = [tuple([community.id, community.title]) for community in communities]
    await msg.answer("Here you can see all communities created by you. You can enter community control-panel by "
                     "hitting on one of community titles", reply_markup=kb.created_communities_kb(communities))
    await state.set_state("created_communities_list")


async def cmd_list_communities_participates_in(msg: Message, state: FSMContext) -> NoReturn:
    communities = await commands.get_communities_participates_in(msg.from_user.id)
    if not communities:
        await msg.answer("You didn't connected to any community. If you have invite code, "
                         "type /connect <code>invite_code</code>")
        return
    communities = [tuple([community.id, community.title]) for community in communities]
    await msg.answer("Here you can see all communities you participates in. You can enter community user-panel by "
                     "hitting on one of community titles", reply_markup=kb.connected_communities_kb(communities))
    await state.set_state("connected_communities_list")


async def exit_from_list_communities(call: CallbackQuery, state: FSMContext) -> NoReturn:
    await call.answer()
    await call.message.edit_text("You've successfully exited from list of communities."
                                 "\n\nHit / to see available commands")
    await state.reset_state()


def setup(dispatcher: Dispatcher) -> NoReturn:
    dispatcher.register_message_handler(cmd_list_created_communities, Command("created"),
                                        content_types=ContentType.TEXT)
    dispatcher.register_message_handler(cmd_list_communities_participates_in, Command("connected"),
                                        content_types=ContentType.TEXT)
    dispatcher.register_callback_query_handler(exit_from_list_communities, text="exit",
                                               state=["created_communities_list", "connected_communities_list"])
