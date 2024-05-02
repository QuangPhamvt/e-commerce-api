"""add payos_id column to bill table

Revision ID: 2b463a5d02b8
Revises: 45aac420852a
Create Date: 2024-04-20 22:43:29.310668

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "2b463a5d02b8"
down_revision: Union[str, None] = "45aac420852a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "Bill",
        sa.Column(
            "payos_id",
            sa.Integer(),
            unique=True,
        ),
    )


def downgrade() -> None:
    op.drop_column("Bill", "payos_id")
