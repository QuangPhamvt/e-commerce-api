"""create additional fee table

Revision ID: 81a1b387e195
Revises: 12b492a610c5
Create Date: 2024-04-23 10:57:04.912552

"""

from datetime import datetime
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "81a1b387e195"
down_revision: Union[str, None] = "12b492a610c5"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "AdditionalFee",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("description", sa.String(255), nullable=False),
        sa.Column("value", sa.Float, nullable=False),
        sa.Column("bill_id", sa.Uuid(), sa.ForeignKey("Bill.id"), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False, default=datetime.now()),
        sa.Column("updated_at", sa.DateTime(), nullable=False, default=datetime.now()),
    )


def downgrade() -> None:
    op.drop_table("AdditionalFee")
