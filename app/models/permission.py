from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.db.base import Base
from app.db.mixins import (
    PublicUUIDMixin,
    SoftDeleteMixin,
    TimestampMixin
)

from app.models.associations import group_permissions


class Permission(
    Base,
    TimestampMixin,
    SoftDeleteMixin,
    PublicUUIDMixin
):
    __tablename__ = "permissions"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    code = Column(
        String,
        unique=True,
        nullable=False,
        index=True
    )

    description = Column(
        String,
        nullable=True
    )

    groups = relationship(
        "Group",
        secondary=group_permissions,
        back_populates="permissions"
    )