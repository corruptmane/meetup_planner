from typing import NoReturn

import pytz
from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import CallbackQuery, ContentType, Message

from app.keyboards.inline import create_community_kb as kb
from app.keyboards.inline import exit_kb
from app.misc import generate_pages
from app.utils import db_commands as commands


async def cmd_create_community(msg: Message, state: FSMContext, from_tz: bool = False) -> NoReturn:
    if from_tz:
        upd = msg.edit_text
    else:
        upd = msg.answer
    message = await upd("How do you wanna call that new community? (64 max characters)", reply_markup=exit_kb)
    await state.set_state("cmd_create_community")
    await state.update_data(msg_id=message.message_id)


async def back_to_cmd_create_community(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await cmd_create_community(call.message, state, True)


async def create_community_title(msg: Message, state: FSMContext, discard: bool = False) -> NoReturn:
    if not discard:
        title = msg.text
        if len(title) > 64:
            await msg.answer(f"You have reached max characters ({len(title)}/64), re-enter your title")
            return
        upd = msg.answer
        current_page = 1
        await state.update_data(title=title)
    else:
        upd = msg.edit_text
        data = await state.get_data()
        current_page = data.get("current_page")
    timezones = generate_pages(pytz.all_timezones, 20)
    message = await upd("Choose timezone for your community from list below (click on your timezone)",
                        reply_markup=kb.timezones_kb(timezones[current_page - 1], current_page, len(timezones)))
    await state.update_data(timezones=timezones, current_page=current_page, msg_id=message.message_id)
    await state.set_state("choose_tz")


async def prev_next_tz_page(call: CallbackQuery, state: FSMContext) -> NoReturn:
    await call.answer()
    data = await state.get_data()
    current_page = data.get("current_page")
    timezones = data.get("timezones")
    direction = call.data.split(":")[1]
    if direction == "prev":
        if current_page == 1:
            current_page = len(timezones)
        else:
            current_page -= 1
    else:
        if current_page == len(timezones):
            current_page = 1
        else:
            current_page += 1
    await call.message.edit_reply_markup(kb.timezones_kb(timezones[current_page - 1], current_page, len(timezones)))
    await state.update_data(current_page=current_page)


async def create_community_tz(call: CallbackQuery, state: FSMContext) -> NoReturn:
    await call.answer()
    data = await state.get_data()
    tz = call.data.split(":")[1]
    title = data.get("title")
    await call.message.edit_text(f"Confirm creating new community with these options:\n\nTitle: {title}"
                                 f"\nTimeZone: {tz}\n\nAre you confirm these options?",
                                 reply_markup=kb.confirm_create_community_kb)
    await state.set_state("confirm_create_community")
    await state.update_data(tz=tz)


async def confirm_create_community(call: CallbackQuery, state: FSMContext) -> NoReturn:
    await call.answer()
    data = await state.get_data()
    title = data.get("title")
    tz = data.get("tz")
    community = await commands.add_community(title, tz, call.from_user.id)
    await call.message.edit_text("You've successfully created community.\n\nHere is invitation code to add people "
                                 f"to this community:\n\n<code>{community.invite_code}</code>")
    await state.reset_state()


async def back_to_create_community_title(call: CallbackQuery, state: FSMContext) -> NoReturn:
    await call.answer()
    await create_community_title(call.message, state, True)


async def exit_create_community(call: CallbackQuery, state: FSMContext) -> NoReturn:
    await call.answer()
    await call.message.edit_text("You've successfully exited from community-creating menu. "
                                 "Hit / to see available commands")
    await state.reset_state()


def setup(dispatcher: Dispatcher) -> NoReturn:
    dispatcher.register_message_handler(cmd_create_community, Command("create"), content_types=ContentType.TEXT)
    dispatcher.register_callback_query_handler(back_to_cmd_create_community, text="back", state="choose_tz")
    dispatcher.register_message_handler(create_community_title, content_types=ContentType.TEXT,
                                        state="cmd_create_community")
    dispatcher.register_callback_query_handler(prev_next_tz_page, text_startswith="tz_page:", state="choose_tz")
    dispatcher.register_callback_query_handler(create_community_tz, text_startswith="tz:", state="choose_tz")
    dispatcher.register_callback_query_handler(back_to_create_community_title, text="back",
                                               state="confirm_create_community")
    dispatcher.register_callback_query_handler(confirm_create_community, text="confirm_create_community",
                                               state="confirm_create_community")
    dispatcher.register_callback_query_handler(exit_create_community, text="discard_create_community",
                                               state="confirm_create_community")
    dispatcher.register_callback_query_handler(exit_create_community, text="exit",
                                               state=["choose_tz", "cmd_create_community"])


__all__ = ("setup",)
