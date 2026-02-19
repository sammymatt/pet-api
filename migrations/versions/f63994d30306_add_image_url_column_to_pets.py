"""add image_url column to pets

Revision ID: f63994d30306
Revises: 4f42a09cc186
Create Date: 2026-02-18 23:35:45.412752

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f63994d30306'
down_revision: Union[str, Sequence[str], None] = '4f42a09cc186'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('pets', sa.Column('image_url', sa.String(), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('pets', 'image_url')
