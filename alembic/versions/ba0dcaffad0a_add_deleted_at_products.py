"""add_deleted_at_products

Revision ID: ba0dcaffad0a
Revises:
Create Date: 2024-03-20 21:42:20.433771

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "ba0dcaffad0a"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("Product", sa.Column("deleted_at", sa.DateTime(), nullable=True))
    pass


def downgrade() -> None:
    op.drop_column("Product", "deleted_at")
    pass
