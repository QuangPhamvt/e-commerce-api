"""create series table

Revision ID: acbd098a84cd
Revises: 6ecae55e5283
Create Date: 2024-03-15 14:28:08.617193

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = "acbd098a84cd"
down_revision: Union[str, None] = "6ecae55e5283"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "Series",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("name", sa.String(length=50), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("image", sa.String(length=255), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.alter_column(
        "Product", "original_price", existing_type=mysql.FLOAT(), nullable=True
    )
    op.alter_column("Product", "sell_price", existing_type=mysql.FLOAT(), nullable=True)
    op.alter_column(
        "Product",
        "quantity",
        existing_type=mysql.INTEGER(display_width=11),
        nullable=True,
    )
    op.alter_column(
        "Product", "image", existing_type=mysql.VARCHAR(length=255), nullable=True
    )
    op.alter_column(
        "Product", "country", existing_type=mysql.VARCHAR(length=50), nullable=True
    )
    op.alter_column(
        "Product", "factory", existing_type=mysql.VARCHAR(length=50), nullable=True
    )
    op.alter_column(
        "Product", "status", existing_type=mysql.VARCHAR(length=12), nullable=True
    )
    op.alter_column(
        "Product", "category_id", existing_type=mysql.CHAR(length=32), nullable=True
    )
    op.create_foreign_key(None, "Product", "Series", ["series_id"], ["id"])
    op.alter_column(
        "UserNotification",
        "content",
        existing_type=mysql.TINYTEXT(),
        type_=sa.Text(length=255),
        existing_nullable=False,
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "UserNotification",
        "content",
        existing_type=sa.Text(length=255),
        type_=mysql.TINYTEXT(),
        existing_nullable=False,
    )
    op.drop_constraint(None, "Product", type_="foreignkey")
    op.alter_column(
        "Product", "category_id", existing_type=mysql.CHAR(length=32), nullable=False
    )
    op.alter_column(
        "Product", "status", existing_type=mysql.VARCHAR(length=12), nullable=False
    )
    op.alter_column(
        "Product", "factory", existing_type=mysql.VARCHAR(length=50), nullable=False
    )
    op.alter_column(
        "Product", "country", existing_type=mysql.VARCHAR(length=50), nullable=False
    )
    op.alter_column(
        "Product", "image", existing_type=mysql.VARCHAR(length=255), nullable=False
    )
    op.alter_column(
        "Product",
        "quantity",
        existing_type=mysql.INTEGER(display_width=11),
        nullable=False,
    )
    op.alter_column(
        "Product", "sell_price", existing_type=mysql.FLOAT(), nullable=False
    )
    op.alter_column(
        "Product", "original_price", existing_type=mysql.FLOAT(), nullable=False
    )
    op.drop_table("Series")
    # ### end Alembic commands ###
