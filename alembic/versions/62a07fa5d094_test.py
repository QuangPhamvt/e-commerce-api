"""test

Revision ID: 62a07fa5d094
Revises: ec6b1d3445ab
Create Date: 2024-02-25 14:36:23.834543

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "62a07fa5d094"
down_revision: Union[str, None] = "ec6b1d3445ab"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("users", sa.Column("name", sa.String(50)))
    pass


def downgrade() -> None:
    op.drop_column("users", "name")
    pass
