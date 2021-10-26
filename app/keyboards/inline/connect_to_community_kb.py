from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

exit_kb = InlineKeyboardMarkup(row_width=1, inline_keyboard=[[InlineKeyboardButton("Exit", callback_data="exit")]])

__all__ = ("exit_kb",)
