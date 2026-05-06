"""add audit columns

Revision ID: a1b2c3d4e5f6
Revises: 4d41c850d44c
Create Date: 2026-05-05 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'a1b2c3d4e5f6'
down_revision: Union[str, Sequence[str], None] = '4d41c850d44c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('created_at', sa.DateTime(), nullable=False,
        server_default=sa.text('CURRENT_TIMESTAMP')))
    op.add_column('users', sa.Column('updated_at', sa.DateTime(), nullable=False,
        server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP')))
    op.add_column('user_scores', sa.Column('created_at', sa.DateTime(), nullable=False,
        server_default=sa.text('CURRENT_TIMESTAMP')))
    op.add_column('user_scores', sa.Column('updated_at', sa.DateTime(), nullable=False,
        server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP')))


def downgrade() -> None:
    op.drop_column('user_scores', 'updated_at')
    op.drop_column('user_scores', 'created_at')
    op.drop_column('users', 'updated_at')
    op.drop_column('users', 'created_at')
