"""add timestamps to furnace charge items

Revision ID: 962dcf9ea6eb
Revises: 63202ce0c0ae
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "962dcf9ea6eb"
down_revision: Union[str, Sequence[str], None] = "63202ce0c0ae"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "furnace_charge_items",
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
    )
    op.add_column(
        "furnace_charge_items",
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
    )


def downgrade() -> None:
    op.drop_column("furnace_charge_items", "updated_at")
    op.drop_column("furnace_charge_items", "created_at")