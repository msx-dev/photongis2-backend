"""add mppt to electrical_string

Revision ID: 80ff03ef359e
Revises: 0741f51c7397
Create Date: 2026-06-26 14:38:39.983699

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '80ff03ef359e'
down_revision: Union[str, Sequence[str], None] = '0741f51c7397'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
