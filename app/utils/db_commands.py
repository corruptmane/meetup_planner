import uuid
from typing import List, NoReturn, Optional

from sqlalchemy.sql.elements import False_, True_, and_, or_

from app.models import *


async def add_user(user_id: int, full_name: str, mention: str) -> User:
    return await User(user_id=user_id, full_name=full_name, mention=mention).create()


async def add_community(title: str, tz: str, creator_id: int) -> Community:
    invite_code = str(uuid.uuid4())
    return await Community(title=title, invite_code=invite_code, creator_id=creator_id,
                           timezone=tz, participants_ids=[creator_id]).create()


async def add_participant_to_community(community_id: int, participant_id: int) -> NoReturn:
    community_ = await get_community_by_community_id(community_id)
    participants: list = [*community_.participants_ids, participant_id]
    await community_.update(participants_ids=participants).apply()


async def add_community_to_participates_in(community_id: int, user_id: int) -> NoReturn:
    user_ = await get_user_by_user_id(user_id)
    participates_in: list = [*user_.participates_in, community_id]
    await user_.update(participates_in=participates_in)


async def get_user_by_user_id(user_id: int) -> Optional[User]:
    return await User.get(user_id)


async def get_all_users() -> List[User]:
    return await User.query.gino.all()


async def get_admins() -> Optional[List[User]]:
    return await User.query.where(and_(User.is_admin == True_(), User.is_banned == False_())).gino.all()


async def get_community_by_invite_code(invite_code: str) -> Optional[Community]:
    return await Community.query.where(Community.invite_code == invite_code).gino.first()


async def get_community_by_community_id(community_id: int) -> Optional[Community]:
    return await Community.get(community_id)


async def get_communities_by_creator_id(creator_id: int) -> Optional[List[Community]]:
    return await Community.query.where(Community.creator_id == creator_id).gino.all()


async def get_communities_participates_in(user_id: int) -> Optional[List[Community]]:
    user_ = await get_user_by_user_id(user_id)
    if not user_.participates_in:
        return None
    community_clauses = [Community.id == community_id for community_id in user_.participates_in]
    return await Community.query.where(or_(*community_clauses)).gino.all()


async def update_user_mailing_status(user_id: int) -> NoReturn:
    user_ = await get_user_by_user_id(user_id)
    mailing = not user_.mailing
    await user_.update(mailing=mailing).apply()


async def update_user_role(user_id: int, role: str) -> NoReturn:
    user_ = await get_user_by_user_id(user_id)
    if role == "admin":
        kwargs = dict(is_admin=True, is_banned=False)
    elif role == "banned":
        kwargs = dict(is_admin=False, is_banned=True)
    else:
        kwargs = dict(is_admin=False, is_banned=False)
    await user_.update(**kwargs).apply()


async def update_user_naming(user_id: int, full_name: str, mention: str) -> NoReturn:
    user_ = await get_user_by_user_id(user_id)
    await user_.update(full_name=full_name, mention=mention).apply()
