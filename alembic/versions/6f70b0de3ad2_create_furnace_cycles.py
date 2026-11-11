
"""create furnace cycles

Revision ID: 6f70b0de3ad2
Revises: 70fe7b1177e8
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "6f70b0de3ad2"
down_revision: Union[str, Sequence[str], None] = "70fe7b1177e8"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Preserve existing Charge Mix and Furnace Cycle Stage tables.
    # Preserve the existing furnace_cycles.shift column.

    op.drop_index(
        "uq_one_running_cycle_per_furnace",
        table_name="furnace_cycles",
    )

    op.create_index(
        "ix_furnace_cycles_status",
        "furnace_cycles",
        ["status"],
        unique=False,
    )

    op.create_index(
        "uq_furnace_cycles_one_running_per_furnace",
        "furnace_cycles",
        ["furnace_id"],
        unique=True,
        postgresql_where=sa.text("status = 'Running'"),
    )


def downgrade() -> None:
    op.drop_index(
        "uq_furnace_cycles_one_running_per_furnace",
        table_name="furnace_cycles",
        postgresql_where=sa.text("status = 'Running'"),
    )

    op.drop_index(
        "ix_furnace_cycles_status",
        table_name="furnace_cycles",
    )

    op.create_index(
        "uq_one_running_cycle_per_furnace",
        "furnace_cycles",
        ["furnace_id"],
        unique=True,
        postgresql_where=sa.text(
            "((status)::text = 'Running'::text)"
        ),
    )
