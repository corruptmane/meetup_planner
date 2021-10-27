from contextlib import suppress
from datetime import datetime
from typing import NoReturn

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.utils.exceptions import MessageError
from pytz import timezone

from app.keyboards.inline import back_and_exit_kb
from app.keyboards.inline import user_panel_kb as kb
from app.misc.useful_funcs import check_date
from app.utils import db_commands as commands


async def community_user_panel(call: CallbackQuery, state: FSMContext) -> NoReturn:
    await call.answer()
    community_id = int(call.data.split(":")[-1])
    community = await commands.get_community_by_community_id(community_id)
    utc_offset = datetime.now(timezone(community.timezone)).strftime("%z")
    await call.message.edit_text(f"You've successfully entered <i>{community.title}</i> user-panel. Here you can plan "
                                 f"meeting by tapping on exact button.\n(Timezone: {community.timezone}/"
                                 f"UTC{utc_offset})", reply_markup=kb.user_panel_kb)
    await state.update_data(community_id=community_id)
    await state.set_state("community_user_panel")


async def user_panel_enter_date(call: CallbackQuery, state: FSMContext) -> NoReturn:
    await call.answer()
    message = await call.message.edit_text("Enter meeting date in that format: dd.mm.yyyy. In example: 18.01.2022",
                                           reply_markup=back_and_exit_kb)
    await state.update_data(msg_id=message.message_id)
    await state.set_state("enter_meeting_date")


async def user_panel_enter_time(msg: Message, state: FSMContext) -> NoReturn:
    data = await state.get_data()
    msg_id = data.get("msg_id")
    dp = Dispatcher.get_current()
    with suppress(MessageError):
        await dp.bot.delete_message(msg.from_user.id, msg_id)
    try:
        check_date(msg.text)
    except Exception:
        pass
    message = await msg.answer("Now, enter meeting time in that format: hh:mm. In example: 18:30",
                               reply_markup=back_and_exit_kb)
    await state.update_data(msg_id=message.message_id)
    await state.set_state("enter_meeting_time")


def setup(dispatcher: Dispatcher) -> NoReturn:
    dispatcher.register_callback_query_handler(community_user_panel, text_startswith="connected_community:",
                                               state="connected_communities_list")
    dispatcher.register_callback_query_handler(user_panel_enter_date, text="plan_meeting", state="community_user_panel")
    dispatcher.register_message_handler(user_panel_enter_time, regexp=r"^\d\d\.\d\d\.\d\d\d\d$",
                                        state="enter_meeting_date")
