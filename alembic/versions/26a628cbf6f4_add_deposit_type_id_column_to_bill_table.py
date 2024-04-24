"""add deposit_type_id column to bill table

Revision ID: 26a628cbf6f4
Revises: 81a1b387e195
Create Date: 2024-04-24 16:10:34.010613

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "26a628cbf6f4"
down_revision: Union[str, None] = "81a1b387e195"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "Bill",
        sa.Column(
            "deposit_type_id",
            sa.Uuid,
            nullable=True,
        ),
    )
    op.create_foreign_key(
        "fk_deposit_type_id_bill",
        "Bill",
        "DepositType",
        ["deposit_type_id"],
        ["id"],
    )


def downgrade() -> None:
    op.drop_constraint("fk_deposit_type_id_bill", "Bill", type_="foreignkey")
    op.drop_column("Bill", "deposit_type_id")
