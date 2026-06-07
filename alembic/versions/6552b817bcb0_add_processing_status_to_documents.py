"""add processing status to documents

Revision ID: 6552b817bcb0
Revises: b48843226de6
Create Date: 2026-06-07 22:39:06.810344

"""
from typing import Sequence, Union
from sqlalchemy.dialects import postgresql

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6552b817bcb0'
down_revision: Union[str, Sequence[str], None] = 'b48843226de6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():

    processing_status_enum = postgresql.ENUM(
        "PENDING",
        "QUEUED",
        "PROCESSING",
        "COMPLETED",
        "FAILED",
        name="processingstatus",
    )

    processing_status_enum.create(op.get_bind())

    op.add_column(
        "loan_documents",
        sa.Column(
            "processing_status",
            processing_status_enum,
            nullable=False,
            server_default="PENDING",
        ),
    )


def downgrade():

    op.drop_column("loan_documents", "processing_status")

    processing_status_enum = postgresql.ENUM(
        "PENDING",
        "QUEUED",
        "PROCESSING",
        "COMPLETED",
        "FAILED",
        name="processingstatus",
    )

    processing_status_enum.drop(op.get_bind())
