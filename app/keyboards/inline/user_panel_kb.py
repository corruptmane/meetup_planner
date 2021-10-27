from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from app.keyboards.inline import back_btn, exit_btn

user_panel_kb = InlineKeyboardMarkup(row_width=1, inline_keyboard=[
    [
        InlineKeyboardButton("Plan meeting", callback_data="plan_meeting")
    ],
    [
        InlineKeyboardButton(back_btn)
    ],
    [
        InlineKeyboardButton(exit_btn)
    ]
])

__all__ = ("user_panel_kb",)
