"""create ProductsImage table

Revision ID: 8a572dec1206
Revises: f4f64cd4124b
Create Date: 2024-04-04 20:52:07.252345

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "8a572dec1206"
down_revision: Union[str, None] = "f4f64cd4124b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "ProductsImage",
        sa.Column("id", sa.Uuid, primary_key=True),
        sa.Column("slug", sa.String(255), nullable=False, unique=True),
        sa.Column("image_url", sa.String(255), nullable=True),
        sa.Column("product_id", sa.Uuid, sa.ForeignKey("Product.id"), nullable=False),
        sa.Column("created_at", sa.DateTime, nullable=False),
        sa.Column("updated_at", sa.DateTime, nullable=True),
        sa.Column("deleted_at", sa.DateTime, nullable=True),
    )
    pass


def downgrade() -> None:
    op.drop_table("ProductsImage")
    pass
