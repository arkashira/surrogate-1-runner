"""Add role field to User model with PostgreSQL ENUM support."""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import ENUM

# ----------------------------------------------------------------------
# Revision identifiers, used by Alembic.
# ----------------------------------------------------------------------
revision = "0004_add_role"
down_revision = "0003_add_user_model"
branch_labels = None
depends_on = None


def upgrade() -> None:
    """
    Create the enum type and add the role column with a server‑side default.
    """
    # 1. Create the enum type if it does not already exist.
    user_role_enum = ENUM(
        "user",
        "admin",
        name="user_role_enum",
        create_type=False,  # we will create it explicitly
    )
    user_role_enum.create(op.get_bind(), checkfirst=True)

    # 2. Add the role column with a server‑side default of 'user'.
    op.add_column(
        "users",
        sa.Column(
            "role",
            user_role_enum,
            nullable=False,
            server_default="user",
        ),
    )


def downgrade() -> None:
    """
    Remove the role column and drop the enum type.
    """
    op.drop_column("users", "role")
    op.execute("DROP TYPE IF EXISTS user_role_enum")