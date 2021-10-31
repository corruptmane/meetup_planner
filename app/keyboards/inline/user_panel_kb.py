from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from app.keyboards.inline import back_btn, exit_btn

user_panel_kb = InlineKeyboardMarkup(row_width=1, inline_keyboard=[
    [
        InlineKeyboardButton("Plan personal meeting", callback_data="personal_meeting")
    ],
    [
        InlineKeyboardButton("Offer group meeting", callback_data="group_meeting")
    ],
    [
        back_btn
    ],
    [
        exit_btn
    ]
])

confirm_meeting_kb = InlineKeyboardMarkup(row_width=2, inline_keyboard=[
    [
        InlineKeyboardButton("Confirm", callback_data="confirm_meeting"),
        InlineKeyboardButton("Discard", callback_data="discard_meeting")
    ],
    [
        back_btn
    ],
    [
        exit_btn
    ]
])

last_user_panel_kb = InlineKeyboardMarkup(row_width=1, inline_keyboard=[
    [
        InlineKeyboardButton("User panel", callback_data="enter_user_panel")
    ],
    [
        exit_btn
    ]
])

__all__ = ("user_panel_kb", "confirm_meeting_kb", "last_user_panel_kb")
