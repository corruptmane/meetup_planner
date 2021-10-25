from typing import NoReturn

import pytz
from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import ContentType, Message, CallbackQuery

from app.keyboards.inline.create_community_kb import timezones_kb, confirm_create_community_kb
from app.misc import generate_pages
from app.utils import db_commands as commands


async def cmd_create_community(msg: Message, state: FSMContext) -> NoReturn:
    await msg.answer("How do you wanna call that new community? (64 max characters)")
    await state.set_state("cmd_create_community")


async def create_community_title(msg: Message, state: FSMContext) -> NoReturn:  # TODO: end-up handler
    title = msg.text
    if len(title) > 64:
        await msg.answer(f"You have reached max characters ({len(title)}/64), re-enter your title")
        return
    timezones = generate_pages(pytz.all_timezones, 20)
    current_page = 1
    message = await msg.answer("Choose timezone for your community from list below (click on your timezone)",
                               reply_markup=timezones_kb(timezones[current_page - 1], current_page, len(timezones)))
    await state.update_data(title=title, timezones=timezones, current_page=current_page, msg_id=message.message_id)
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
    await call.message.edit_reply_markup(timezones_kb(timezones[current_page - 1], current_page, len(timezones)))
    await state.update_data(current_page=current_page)


async def create_community_tz(call: CallbackQuery, state: FSMContext) -> NoReturn:
    await call.answer()
    data = await state.get_data()
    tz = call.data.split(":")[1]
    title = data.get("title")
    await call.message.edit_text(f"Confirm creating new community with these options:\n\nTitle: {title}"
                                 f"\nTimeZone: {tz}\n\nAre you confirm these options?",
                                 reply_markup=confirm_create_community_kb)
    await state.set_state("confirm_create_community")
    await state.update_data(tz=tz)


async def create_community_confirm(call: CallbackQuery, state: FSMContext) -> NoReturn:
    await call.answer()
    data = await state.get_data()
    title = data.get("title")
    tz = data.get("tz")
    community = await commands.add_community(title, tz, call.from_user.id)
    await call.message.edit_text("You've successfully created community.\nHere is invitation code to add people "
                                 f"to this community:\n\n<code>{community.invite_code}</code>")
    await state.reset_state()


async def create_community_discard(call: CallbackQuery, state: FSMContext) -> NoReturn:  # TODO: end-up this handler
    await call.answer()


def setup(dispatcher: Dispatcher) -> NoReturn:
    dispatcher.register_message_handler(cmd_create_community, Command("create"), content_types=ContentType.TEXT)
    dispatcher.register_message_handler(create_community_title, content_types=ContentType.TEXT,
                                        state="cmd_create_community")
    dispatcher.register_callback_query_handler(prev_next_tz_page, text_endswith="_page", state="choose_tz")
    dispatcher.register_callback_query_handler(create_community_tz, text_startswith="tz:", state="choose_tz")
    dispatcher.register_callback_query_handler(create_community_confirm, text="confirm_create_community",
                                               state="confirm_create_community")
