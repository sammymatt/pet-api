"""add vaccines appointments tablets tables

Revision ID: b2c3d4e5f6a7
Revises: a1b2c3d4e5f6
Create Date: 2026-01-27 12:30:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b2c3d4e5f6a7'
down_revision: Union[str, Sequence[str], None] = 'a1b2c3d4e5f6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Create vaccines table
    op.create_table(
        'vaccines',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('administered_date', sa.Date(), nullable=False),
        sa.Column('next_due_date', sa.Date(), nullable=True),
        sa.Column('administered_by', sa.String(), nullable=True),
        sa.Column('notes', sa.String(), nullable=True),
        sa.Column('pet_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['pet_id'], ['pets.id']),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_vaccines_id'), 'vaccines', ['id'], unique=False)

    # Create appointments table
    op.create_table(
        'appointments',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('appointment_date', sa.DateTime(), nullable=False),
        sa.Column('reason', sa.String(), nullable=False),
        sa.Column('vet_name', sa.String(), nullable=True),
        sa.Column('location', sa.String(), nullable=True),
        sa.Column('notes', sa.String(), nullable=True),
        sa.Column('status', sa.String(), nullable=True),
        sa.Column('pet_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['pet_id'], ['pets.id']),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_appointments_id'), 'appointments', ['id'], unique=False)

    # Create tablets table
    op.create_table(
        'tablets',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('dosage', sa.String(), nullable=True),
        sa.Column('frequency', sa.String(), nullable=True),
        sa.Column('start_date', sa.Date(), nullable=False),
        sa.Column('end_date', sa.Date(), nullable=True),
        sa.Column('notes', sa.String(), nullable=True),
        sa.Column('pet_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['pet_id'], ['pets.id']),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_tablets_id'), 'tablets', ['id'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_tablets_id'), table_name='tablets')
    op.drop_table('tablets')
    op.drop_index(op.f('ix_appointments_id'), table_name='appointments')
    op.drop_table('appointments')
    op.drop_index(op.f('ix_vaccines_id'), table_name='vaccines')
    op.drop_table('vaccines')
