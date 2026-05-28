from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    Table
)

from app.db.base import Base


user_groups = Table(
    "user_groups",
    Base.metadata,
    Column(
        "user_id",
        Integer,
        ForeignKey("users.id"),
        primary_key=True
    ),
    Column(
        "group_id",
        Integer,
        ForeignKey("groups.id"),
        primary_key=True
    )
)


group_permissions = Table(
    "group_permissions",
    Base.metadata,
    Column(
        "group_id",
        Integer,
        ForeignKey("groups.id"),
        primary_key=True
    ),
    Column(
        "permission_id",
        Integer,
        ForeignKey("permissions.id"),
        primary_key=True
    )
)
