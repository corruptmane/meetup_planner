from datetime import date, datetime
from typing import NoReturn

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, ContentType, Message
from aiogram_broadcaster import TextBroadcaster
from pytz import timezone

from app.keyboards.inline import back_and_exit_kb
from app.keyboards.inline import user_panel_kb as kb
from app.misc import check_date, check_time, delete_last_msg
from app.utils import db_commands as commands


async def community_user_panel(call: CallbackQuery, state: FSMContext, back_to: bool = False) -> NoReturn:
    await call.answer()
    if back_to:
        community_id = (await state.get_data()).get("community_id")
    else:
        community_id = int(call.data.split(":")[-1])
    community = await commands.get_community_by_community_id(community_id)
    utc_offset = datetime.now(timezone(community.timezone)).strftime("%z")
    await call.message.edit_text(f"You've successfully entered <i>{community.title}</i> user-panel. Here you can plan "
                                 f"meeting by tapping on button from listed below.\n(Timezone: {community.timezone} | "
                                 f"UTC{utc_offset}).", reply_markup=kb.user_panel_kb)
    await state.update_data(community_id=community_id)
    await state.set_state("community_user_panel")


async def back_to_community_user_panel(call: CallbackQuery, state: FSMContext) -> NoReturn:
    await community_user_panel(call, state, True)


async def chosen_type_of_meeting(call: CallbackQuery, state: FSMContext) -> NoReturn:
    await call.answer()
    type_of_meeting = "personal" if call.data == "personal_meeting" else "group"
    await state.update_data(type_of_meeting=type_of_meeting)
    await user_panel_enter_date(call, state, True)


async def user_panel_enter_date(call: CallbackQuery, state: FSMContext, from_choose: bool = False) -> NoReturn:
    if not from_choose:
        await call.answer()
    message = await call.message.edit_text("Enter meeting date in that format: <code>dd.mm.yyyy</code>. In example: "
                                           "18.01.2022.", reply_markup=back_and_exit_kb)
    await state.update_data(msg_id=message.message_id)
    await state.set_state("enter_meeting_date")


async def user_panel_enter_time(msg: Message, state: FSMContext, back_to: bool = False) -> NoReturn:
    msg_text = "Now, enter meeting time in that format: <code>hh:mm</code>. In example: 18:30."
    if back_to:
        await msg.edit_text(msg_text, reply_markup=back_and_exit_kb)
        await state.set_state("enter_meeting_time")
        return
    await delete_last_msg(msg, state)
    error = False
    try:
        check_date(msg.text)
    except ValueError as err:
        error = True
        msg_text = (f"Seems like you made a mistake. Here is an error:\n\n{err.args[0]}\n\nEnter meeting date "
                    "in that format: <code>dd.mm.yyyy</code>. In example: 18.01.2022")
    message = await msg.answer(msg_text, reply_markup=back_and_exit_kb)
    await state.update_data(msg_id=message.message_id)
    if not error:
        await state.update_data(user_date=msg.text)
        await state.set_state("enter_meeting_time")


async def back_to_user_panel_enter_time(call: CallbackQuery, state: FSMContext) -> NoReturn:
    await call.answer()
    await user_panel_enter_time(call.message, state, True)


async def user_panel_enter_meeting_note(msg: Message, state: FSMContext, back_to: bool = False) -> NoReturn:
    msg_text = "Now, enter meeting note which community creator would see."
    if back_to:
        await msg.edit_text(msg_text, reply_markup=back_and_exit_kb)
        await state.set_state("enter_meeting_note")
        return
    await delete_last_msg(msg, state)
    data = await state.get_data()
    user_date_str = data.get("user_date")
    day, month, year = list(map(int, user_date_str.split(".")))
    community_id = data.get("community_id")
    community = await commands.get_community_by_community_id(community_id)
    error = False
    try:
        check_time(msg.text, date(year, month, day), timezone(community.timezone))
    except ValueError as err:
        error = True
        msg_text = (f"Seems like you made a mistake. Here is an error:\n\n{err.args[0]}\n\nEnter meeting time "
                    "in that format: <code>hh:mm</code>. In example: 18:30")
    message = await msg.answer(msg_text, reply_markup=back_and_exit_kb)
    await state.update_data(msg_id=message.message_id)
    if not error:
        await state.update_data(user_time=msg.text)
        await state.set_state("enter_meeting_note")


async def back_to_user_panel_enter_meeting_note(call: CallbackQuery, state: FSMContext) -> NoReturn:
    await call.answer()
    await user_panel_enter_meeting_note(call.message, state, True)


async def user_panel_confirm_meeting_data(msg: Message, state: FSMContext) -> NoReturn:
    await delete_last_msg(msg, state)
    meeting_note = msg.html_text
    data = await state.get_data()
    user_date, user_time, community_id = data.get("user_date"), data.get("user_time"), int(data.get("community_id"))
    community = await commands.get_community_by_community_id(community_id)
    day, month, year = list(map(int, user_date.split(".")))
    hour, minute = list(map(int, user_time.split(":")))
    user_datetime = datetime(year, month, day, hour, minute, tzinfo=timezone(community.timezone))
    strftime = user_datetime.strftime("%A, %d.%m.%Y %H:%M %Z (%z)")
    message = await msg.answer(f"Confirm meeting data:\n\nDate and time: {strftime}\nNote:\n{meeting_note}",
                               reply_markup=kb.confirm_meeting_kb)
    await state.update_data(meeting_note=meeting_note, msg_id=message.message_id)
    await state.set_state("confirm_meeting_data")


async def user_panel_confirm_meeting(call: CallbackQuery, state: FSMContext) -> NoReturn:
    await call.answer()
    data = await state.get_data()
    user_date, user_time, community_id = data.get("user_date"), data.get("user_time"), int(data.get("community_id"))
    community = await commands.get_community_by_community_id(community_id)
    type_of_meeting, note = data.get("type_of_meeting"), data.get("meeting_note")
    day, month, year = list(map(int, user_date.split(".")))
    hour, minute = list(map(int, user_time.split(":")))
    user_datetime = datetime(year, month, day, hour, minute, tzinfo=timezone(community.timezone))
    strftime = user_datetime.strftime("%A, %d.%m.%Y %H:%M %Z (%z)")
    await commands.add_meeting(community.id, call.from_user.id, user_datetime, note, type_of_meeting)
    meeting_creator = await commands.get_user_by_user_id(call.from_user.id)
    await TextBroadcaster(community.creator_id,
                          "That user ($user_mention) wants $type_of_meeting meeting (Community: <i>$community_title</i>"
                          ". Collected data:\n\nDate and time: $strftime\nNote:\n$note\n\nAre you approve/decline that "
                          "request? You can always return to requests by entering community control-panel",
                          kwargs=dict(user_mention=meeting_creator.mention, type_of_meeting=type_of_meeting,
                                      community_title=community.title, strftime=strftime, note=note)).run()
    await call.message.edit_text("You've successfully created meeting. Enter user-panel or exit by hitting on exact "
                                 "button", reply_markup=kb.last_user_panel_kb)
    await state.set_state("created_meeting")


async def exit_from_user_panel(call: CallbackQuery, state: FSMContext) -> NoReturn:
    await call.answer()
    await call.message.edit_text("You've successfully exited from user-panel menu.\n\nHit / to see available commands")
    await state.reset_state()


def setup(dispatcher: Dispatcher) -> NoReturn:
    dispatcher.register_callback_query_handler(exit_from_user_panel, text="exit", state="community_user_panel")
    dispatcher.register_callback_query_handler(community_user_panel, text_startswith="connected_community:",
                                               state="connected_communities_list")
    dispatcher.register_callback_query_handler(back_to_community_user_panel, text="exit",
                                               state=["enter_meeting_date", "enter_meeting_time",
                                                      "enter_meeting_note", "confirm_meeting_data", "created_meeting"])
    dispatcher.register_callback_query_handler(back_to_community_user_panel, text="enter_user_panel",
                                               state="created_meeting")
    dispatcher.register_callback_query_handler(back_to_community_user_panel, text="back", state="enter_meeting_date")
    dispatcher.register_callback_query_handler(back_to_community_user_panel, text="discard_meeting",
                                               state="confirm_meeting_data")
    dispatcher.register_callback_query_handler(chosen_type_of_meeting, text_endswith="_meeting",
                                               state="community_user_panel")
    dispatcher.register_callback_query_handler(user_panel_enter_date, text="back", state="enter_meeting_time")
    dispatcher.register_message_handler(user_panel_enter_time, regexp=r"^\d\d\.\d\d\.\d\d\d\d$",
                                        state="enter_meeting_date")
    dispatcher.register_callback_query_handler(back_to_user_panel_enter_time, text="back", state="enter_meeting_note")
    dispatcher.register_message_handler(user_panel_enter_meeting_note, regexp=r"^\d\d:\d\d$",
                                        state="enter_meeting_time")
    dispatcher.register_callback_query_handler(back_to_user_panel_enter_meeting_note, text="back",
                                               state="confirm_meeting_data")
    dispatcher.register_message_handler(user_panel_confirm_meeting_data, content_types=ContentType.TEXT,
                                        state="enter_meeting_note")
    dispatcher.register_callback_query_handler(user_panel_confirm_meeting, text="confirm_meeting",
                                               state="confirm_meeting_data")
