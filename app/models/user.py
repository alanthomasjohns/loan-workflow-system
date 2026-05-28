from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from app.db.base import Base
from app.db.mixins import (
    PublicUUIDMixin,
    SoftDeleteMixin,
    TimestampMixin
)

from app.models.associations import user_groups


class User(
    Base,
    TimestampMixin,
    SoftDeleteMixin,
    PublicUUIDMixin
):
    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    first_name = Column(
        String,
        nullable=False
    )

    last_name = Column(
        String,
        nullable=False
    )

    email = Column(
        String,
        unique=True,
        nullable=False,
        index=True
    )

    hashed_password = Column(
        String,
        nullable=False
    )

    is_active = Column(
        Boolean,
        default=True,
        nullable=False
    )

    groups = relationship(
        "Group",
        secondary=user_groups,
        back_populates="users"
    )

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"