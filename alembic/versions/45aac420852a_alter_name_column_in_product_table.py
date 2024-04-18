"""alter name column in product table

Revision ID: 45aac420852a
Revises: 8a572dec1206
Create Date: 2024-04-19 01:26:40.674486

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "45aac420852a"
down_revision: Union[str, None] = "8a572dec1206"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        "Product",
        "name",
        type_=sa.String(255),
        nullable=False,
    )


def downgrade() -> None:
    op.alter_column(
        "Product",
        "name",
        type_=sa.String(50),
        nullable=False,
    )
