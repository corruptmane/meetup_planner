from contextlib import suppress
from datetime import date, datetime, time
from typing import List, NoReturn

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message
from aiogram.utils.exceptions import MessageError
from pytz import timezone


def generate_pages(array: List, articles_on_page: int) -> List[List]:
    length = len(array)
    number_of_pages = (length // articles_on_page)
    if length % articles_on_page != 0:
        number_of_pages += 1
    results = [array[page * articles_on_page : (page + 1) * articles_on_page] for page in range(number_of_pages)]
    return results


async def delete_last_msg(msg: Message, state: FSMContext) -> NoReturn:
    data = await state.get_data()
    msg_id = data.get("msg_id")
    dp = Dispatcher.get_current()
    with suppress(MessageError):
        await dp.bot.delete_message(msg.from_user.id, msg_id)


def check_date(string: str) -> NoReturn:
    day, month, year = list(map(int, string.split(".")))
    today = date.today()
    try:
        user_date = date(year, month, day)
    except ValueError as err:
        if err.args[0] == "month must be in 1..12":
            raise ValueError("Month must be between 1 and 12")
        elif err.args[0] == "day is out of range for month":
            raise ValueError("Day is out of range for that month")
        else:
            raise err
    else:
        if user_date < today:
            raise ValueError("You can't plan meeting to past")


def check_time(string: str, user_date: date, tz: timezone) -> NoReturn:
    hour, minute = list(map(int, string.split(":")))
    try:
        time(hour, minute)
    except ValueError as err:
        if err.args[0] == "hour must be in 0..23":
            raise ValueError("Hour must be between 0 and 23")
        elif err.args[0] == "minute must be in 0..59":
            raise ValueError("Minute must be between 0 and 59")
        else:
            raise err
    else:
        user_datetime = datetime(user_date.year, user_date.month, user_date.day, hour, minute, tzinfo=tz)
        if user_datetime <= datetime.now(tz):
            raise ValueError("You can't plan meeting to past")


__all__ = ("generate_pages", "delete_last_msg", "check_date", "check_time")
