"""Change user_id to string in tasks table

Revision ID: 001
Revises:
Create Date: 2026-01-12

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Change tasks.user_id from integer to varchar."""
    # SQLAlchemy with postgres will handle the type cast
    op.alter_column(
        'tasks',
        'user_id',
        type_=sa.String(length=255),
        existing_type=sa.Integer(),
        existing_nullable=False
    )


def downgrade() -> None:
    """Revert tasks.user_id from varchar to integer."""
    op.alter_column(
        'tasks',
        'user_id',
        type_=sa.Integer(),
        existing_type=sa.String(length=255),
        existing_nullable=False
    )
