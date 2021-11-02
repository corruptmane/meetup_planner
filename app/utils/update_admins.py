from typing import List, NoReturn

from app.utils import db_commands as commands


async def update_admins(admins_ids: List[int]) -> NoReturn:
    to_check = await commands.get_users_to_startup_update(admins_ids)
    for user in to_check:
        if user.user_id in admins_ids and user.is_admin:
            continue
        elif user.user_id not in admins_ids:
            await commands.update_user_role(user.user_id, "regular")
        elif user.user_id in admins_ids and (not user.is_admin or user.is_banned):
            await commands.update_user_role(user.user_id, "admin")
