from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

back_btn = InlineKeyboardButton("« Back ", callback_data="back")
exit_btn = InlineKeyboardButton("Exit", callback_data="exit")

exit_kb = InlineKeyboardMarkup(row_width=1, inline_keyboard=[[exit_btn]])

__all__ = ("back_btn", "exit_btn", "exit_kb",)
