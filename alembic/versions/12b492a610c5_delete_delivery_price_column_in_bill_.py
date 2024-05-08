"""delete delivery_price column in bill table

Revision ID: 12b492a610c5
Revises: f73fa9c02108
Create Date: 2024-04-23 08:39:18.394286

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "12b492a610c5"
down_revision: Union[str, None] = "2b463a5d02b8"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_column("Bill", "delivery_price")


def downgrade() -> None:
    op.add_column(
        "Bill",
        sa.Column("delivery_price", sa.Float(), nullable=True),
    )
