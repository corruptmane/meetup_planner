from typing import NoReturn

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import CallbackQuery, ContentType, Message

from app.keyboards.inline import exit_kb
from app.misc import delete_last_msg
from app.utils import db_commands as commands


async def cmd_connect_to_community(msg: Message, state: FSMContext) -> NoReturn:
    args = msg.get_args()
    if not args:
        message = await msg.answer("Send invite code to connect to community, or exit this operation",
                                   reply_markup=exit_kb)
        await state.set_state("enter_invite_code")
        await state.update_data(msg_id=message.message_id)
        return
    invite_code = args[-1]
    invite_code = invite_code.strip("[]")
    community, user = await commands.get_community_by_invite_code(invite_code, msg.from_user.id)
    if not community:
        message = await msg.answer("You've entered non-existing invite code. Send correct code to connect to "
                                   "community, or exit this operation", reply_markup=exit_kb)
        await state.set_state("enter_invite_code")
        await state.update_data(msg_id=message.message_id)
        return
    elif community.id in user.participates_in:
        message = await msg.answer("You already participates in community with that invite code.", reply_markup=exit_kb)
        await state.update_data(msg_id=message.message_id)
        return
    await commands.add_participant_to_community(community.id, msg.from_user.id)
    await commands.add_community_to_participates_in(community.id, msg.from_user.id)
    await msg.answer(f"You've successfully connected to community {community.title}. Hit / to see available commands")
    await state.reset_state()


async def enter_invite_code(msg: Message, state: FSMContext) -> NoReturn:
    await delete_last_msg(msg, state)
    invite_code = msg.text.strip("[]")
    community, user = await commands.get_community_by_invite_code(invite_code, msg.from_user.id)
    if not community:
        message = await msg.answer("You've entered non-existing invite code. Send correct code to connect to "
                                   "community, or exit this operation", reply_markup=exit_kb)
        await state.update_data(msg_id=message.message_id)
        return
    elif community.id in user.participates_in:
        message = await msg.answer("You already participates in community with that invite code.", reply_markup=exit_kb)
        await state.update_data(msg_id=message.message_id)
        return
    await commands.add_participant_to_community(community.id, msg.from_user.id)
    await commands.add_community_to_participates_in(community.id, msg.from_user.id)
    await msg.answer(f"You've successfully connected to community {community.title}. Hit / to see available commands")
    await state.reset_state()


async def exit_from_enter_invite_code(call: CallbackQuery, state: FSMContext) -> NoReturn:
    await call.answer()
    await call.message.edit_text("You've successfully exited from connecting-to-community menu.\n\n"
                                 "Hit / to see available commands")
    await state.reset_state()


def setup(dispatcher: Dispatcher) -> NoReturn:
    dispatcher.register_message_handler(cmd_connect_to_community, Command("connect"), content_types=ContentType.TEXT)
    dispatcher.register_message_handler(enter_invite_code, content_types=ContentType.TEXT, state="enter_invite_code")
    dispatcher.register_callback_query_handler(exit_from_enter_invite_code, text="exit", state="enter_invite_code")


__all__ = ("setup",)
