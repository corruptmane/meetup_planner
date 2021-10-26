from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def created_communities_kb(communities: list[tuple]) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=1)
    for community_id, title in communities:
        keyboard.insert(InlineKeyboardButton(title, callback_data=f"created_comm:{community_id}"))
    return keyboard


__all__ = ("created_communities_kb",)
