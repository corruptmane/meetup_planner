from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

back_btn = InlineKeyboardButton("« Back", callback_data="back")
exit_btn = InlineKeyboardButton("Exit", callback_data="exit")


def timezones_kb(timezones: list, current_page: int, quantity_of_pages: int) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=2)
    for timezone in timezones:
        keyboard.insert(InlineKeyboardButton(text=timezone, callback_data=f"tz:{timezone}"))
    if current_page == 1:
        prev_page_int = quantity_of_pages
        next_page_int = 2
    elif current_page == quantity_of_pages:
        prev_page_int = current_page - 1
        next_page_int = 1
    else:
        prev_page_int = current_page - 1
        next_page_int = current_page + 1
    keyboard.insert(InlineKeyboardButton(f"Previous page ({prev_page_int}/{quantity_of_pages})",
                                         callback_data="tz_page:prev"))
    keyboard.insert(InlineKeyboardButton(f"Next page ({next_page_int}/{quantity_of_pages})",
                                         callback_data="tz_page:next"))
    keyboard.row(back_btn)
    keyboard.row(exit_btn)
    return keyboard


confirm_create_community_kb = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton("Confirm", callback_data="confirm_create_community")
    ],
    [
        InlineKeyboardButton("Discard", callback_data="discard_create_community")
    ],
    [
        back_btn
    ]
])

__all__ = ("timezones_kb", "confirm_create_community_kb")
