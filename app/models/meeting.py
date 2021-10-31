import enum

import sqlalchemy as sa

from app.models.base import TimedBaseModel


class MeetingTypeEnum(enum.Enum):
    personal = "PERSONAL"
    group = "GROUP"


class MeetingStatusEnum(enum.Enum):
    created = "CREATED"
    approved = "ACCEPTED"
    rejected = "REJECTED"
    under_consideration = "UNDER_CONSIDERATION"


class Meeting(TimedBaseModel):
    __tablename__ = "meetings"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    creator_id = sa.Column(sa.BigInteger, sa.ForeignKey("users.user_id"), nullable=False, index=True)
    community_id = sa.Column(sa.Integer, sa.ForeignKey("communities.id"), nullable=False, index=True)

    type_of_meeting = sa.Column(sa.Enum(MeetingTypeEnum), nullable=False, index=True)
    status = sa.Column(sa.Enum(MeetingStatusEnum), nullable=False, index=True)
    planned_to = sa.Column(sa.DateTime(True), nullable=False)
    note = sa.Column(sa.String, nullable=False)

    query: sa.sql.Select
