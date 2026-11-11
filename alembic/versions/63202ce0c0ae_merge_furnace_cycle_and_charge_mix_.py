"""merge furnace cycle and charge mix migrations

Revision ID: 63202ce0c0ae
Revises: 6f70b0de3ad2, 49f7006d0a7b
Create Date: 2026-11-11 19:37:55.480051

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '63202ce0c0ae'
down_revision: Union[str, Sequence[str], None] = ('6f70b0de3ad2', '49f7006d0a7b')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
