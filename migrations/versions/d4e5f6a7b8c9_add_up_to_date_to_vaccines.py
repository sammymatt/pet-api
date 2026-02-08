"""add up_to_date to vaccines

Revision ID: d4e5f6a7b8c9
Revises: c3d4e5f6a7b8
Create Date: 2026-02-06 10:30:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd4e5f6a7b8c9'
down_revision: Union[str, Sequence[str], None] = 'c3d4e5f6a7b8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add up_to_date column to vaccines table."""
    op.add_column('vaccines', sa.Column('up_to_date', sa.Boolean(), nullable=True))


def downgrade() -> None:
    """Remove up_to_date column from vaccines table."""
    op.drop_column('vaccines', 'up_to_date')
