"""add frequency to vaccines

Revision ID: c3d4e5f6a7b8
Revises: b2c3d4e5f6a7
Create Date: 2026-02-06 10:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c3d4e5f6a7b8'
down_revision: Union[str, Sequence[str], None] = 'b2c3d4e5f6a7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add frequency column to vaccines table."""
    op.add_column('vaccines', sa.Column('frequency', sa.String(), nullable=True))


def downgrade() -> None:
    """Remove frequency column from vaccines table."""
    op.drop_column('vaccines', 'frequency')
