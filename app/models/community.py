import sqlalchemy as sa

from app.models.base import TimedBaseModel


class Community(TimedBaseModel):
    __tablename__ = "communities"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    invite_code = sa.Column(sa.String, nullable=False)
    title = sa.Column(sa.String(64), nullable=False)
    creator_id = sa.Column(sa.BigInteger, sa.ForeignKey("users.user_id"), nullable=False, index=True)
    participants_ids = sa.Column(sa.ARRAY(sa.BigInteger))
    timezone = sa.Column(sa.String(100), nullable=False)

    query: sa.sql.Select
