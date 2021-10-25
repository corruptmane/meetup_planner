from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from app.misc import generate_pages

back_btn = InlineKeyboardButton("« Back ", callback_data="back")
exit_btn = InlineKeyboardButton("Exit", callback_data="exit")


def timezones_kb(timezones: list, current_page: int, quantity_of_pages: int) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=3)
    timezones = generate_pages(timezones, 2)
    for double_timezone in timezones:
        keyboard.row(InlineKeyboardButton(double_timezone[0], callback_data=f"tz:{double_timezone[0]}"))
        if len(double_timezone) == 1:
            break
        keyboard.insert(InlineKeyboardButton(double_timezone[1], callback_data=f"tz:{double_timezone[1]}"))
    if current_page == 1:
        prev_page_int = quantity_of_pages
        next_page_int = 2
    elif current_page == quantity_of_pages:
        prev_page_int = current_page - 1
        next_page_int = 1
    else:
        prev_page_int = current_page - 1
        next_page_int = current_page + 1
    keyboard.row(InlineKeyboardButton(f"({prev_page_int} / {quantity_of_pages})",
                                      callback_data="tz_page:prev"),
                 back_btn,
                 InlineKeyboardButton(f"({next_page_int} / {quantity_of_pages})",
                                      callback_data="tz_page:next"))
    keyboard.row(exit_btn)
    return keyboard


confirm_create_community_kb = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton("Confirm", callback_data="confirm_create_community"),
        InlineKeyboardButton("Discard", callback_data="discard_create_community")
    ],
    [
        back_btn
    ]
])

exit_kb = InlineKeyboardMarkup(row_width=1, inline_keyboard=[[exit_btn]])

__all__ = ("timezones_kb", "confirm_create_community_kb", "exit_kb")
