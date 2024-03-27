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
    op.add_column("product", sa.Column("variant", sa.Text()))
    op.add_column("product", sa.Column("preorder_start_date", sa.DateTime))
    op.add_column("product", sa.Column("preorder_end_date", sa.DateTime))
    op.add_column("product", sa.Column("deleted_at", sa.DateTime))
    op.alter_column(
        "product", "image", existing_type=sa.String(255), new_column_name="thumbnail"
    )

    op.add_column("series", sa.Column("deleted_at", sa.DateTime))
    op.add_column("tag", sa.Column("deleted_at", sa.DateTime))
    op.add_column("category", sa.Column("deleted_at", sa.DateTime))
    pass


def downgrade() -> None:
    op.drop_column("product", "variant")
    op.drop_column("product", "preorder_start_date")
    op.drop_column("product", "preorder_end_date")
    op.drop_column("product", "deleted_at")
    op.alter_column(
        "product", "thumbnail", existing_type=sa.String(255), new_column_name="image"
    )

    op.drop_column("series", "deleted_at")
    op.drop_column("tag", "deleted_at")
    op.drop_column("category", "deleted_at")
    pass
