from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.db.base import Base
from app.db.mixins import (
    PublicUUIDMixin,
    SoftDeleteMixin,
    TimestampMixin
)

from app.models.associations import (
    group_permissions,
    user_groups
)


class Group(
    Base,
    TimestampMixin,
    SoftDeleteMixin,
    PublicUUIDMixin
):
    __tablename__ = "groups"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String,
        unique=True,
        nullable=False,
        index=True
    )

    description = Column(
        String,
        nullable=True
    )

    users = relationship(
        "User",
        secondary=user_groups,
        back_populates="groups"
    )

    permissions = relationship(
        "Permission",
        secondary=group_permissions,
        back_populates="groups"
    )