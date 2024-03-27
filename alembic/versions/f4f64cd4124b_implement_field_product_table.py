"""implement field product table

Revision ID: f4f64cd4124b
Revises:
Create Date: 2024-03-26 03:05:39.640371

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "f4f64cd4124b"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("Product", sa.Column("variant", sa.Text()))
    op.add_column("Product", sa.Column("preorder_start_date", sa.DateTime))
    op.add_column("Product", sa.Column("preorder_end_date", sa.DateTime))
    op.alter_column(
        "Product",
        "image",
        existing_type=sa.String(255),
        new_column_name="thumbnail",
        server_default=None,
    )
    #
    op.add_column("Series", sa.Column("deleted_at", sa.DateTime))
    op.add_column("Tag", sa.Column("deleted_at", sa.DateTime))
    op.add_column("Category", sa.Column("deleted_at", sa.DateTime))
    pass


def downgrade() -> None:
    op.drop_column("Product", "variant")
    op.drop_column("Product", "preorder_start_date")
    op.drop_column("Product", "preorder_end_date")
    op.alter_column(
        "Product",
        "thumbnail",
        existing_type=sa.String(255),
        new_column_name="image",
        server_default=None,
    )
    #
    op.drop_column("Series", "deleted_at")
    op.drop_column("Tag", "deleted_at")
    op.drop_column("Category", "deleted_at")
    pass
