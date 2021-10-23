import sqlalchemy as sa

from app.models.base import TimedBaseModel


class Community(TimedBaseModel):
    __tablename__ = "communities"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    title = sa.Column(sa.String(64), nullable=False)
    creator = sa.Column(sa.BigInteger, sa.ForeignKey('users.user_id'), nullable=False, index=True)
    participants = sa.Column(sa.ARRAY(sa.BigInteger))

    query: sa.sql.Select
