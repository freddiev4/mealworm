"""Add user analytics table

Revision ID: abc123456789
Revises: dd9e8cb112a6
Create Date: 2026-02-01 14:41:23.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "abc123456789"
down_revision: Union[str, None] = "dd9e8cb112a6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create user_analytics table
    op.create_table(
        "user_analytics",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("meal_plan_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("last_meal_plan_generated", sa.DateTime(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_user_analytics_user_id"),
        "user_analytics",
        ["user_id"],
        unique=True,
    )

    # Populate analytics table with existing data
    # This SQL counts meal plans per user and populates the analytics table
    op.execute("""
        INSERT INTO user_analytics (user_id, meal_plan_count, last_meal_plan_generated, created_at, updated_at)
        SELECT
            u.id as user_id,
            COALESCE(COUNT(gmp.id), 0) as meal_plan_count,
            MAX(gmp.created_at) as last_meal_plan_generated,
            CURRENT_TIMESTAMP as created_at,
            CURRENT_TIMESTAMP as updated_at
        FROM users u
        LEFT JOIN generated_meal_plans gmp ON u.id = gmp.user_id
        GROUP BY u.id
    """)


def downgrade() -> None:
    op.drop_index(op.f("ix_user_analytics_user_id"), table_name="user_analytics")
    op.drop_table("user_analytics")
