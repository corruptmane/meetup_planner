from typing import List, Tuple, Union

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from app.keyboards.inline import exit_btn


def created_communities_kb(communities: List[Tuple[Union[str, int]]]) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=1)
    for community_id, title in communities:
        keyboard.insert(InlineKeyboardButton(title, callback_data=f"created_community:{community_id}"))
    keyboard.insert(exit_btn)
    return keyboard


def connected_communities_kb(communities: List[Tuple[Union[str, int]]]) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=1)
    for community_id, title in communities:
        keyboard.insert(InlineKeyboardButton(title, callback_data=f"connected_community:{community_id}"))
    keyboard.insert(exit_btn)
    return keyboard


__all__ = ("created_communities_kb", "connected_communities_kb",)
