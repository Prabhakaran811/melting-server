"""add confirmed_at to furnace charge mixes

Revision ID: GENERATED_REVISION_ID
Revises: 70fe7b1177e8
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "49f7006d0a7b"
down_revision: Union[str, Sequence[str], None] = "70fe7b1177e8"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "furnace_charge_mixes",
        sa.Column("confirmed_at", sa.DateTime(timezone=True), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("furnace_charge_mixes", "confirmed_at")