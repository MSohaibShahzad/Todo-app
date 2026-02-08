"""Placeholder migration - user_id already string

Revision ID: 001
Revises: 000
Create Date: 2026-01-12

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '001'
down_revision: Union[str, None] = '000'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """No-op: user_id is already created as string in initial migration."""
    pass


def downgrade() -> None:
    """No-op: nothing to revert."""
    pass
