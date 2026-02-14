"""fix pass coloumn in users

Revision ID: e0ad035d0b58
Revises: e3bfbc2127a8
Create Date: 2026-02-14 09:54:49.736771

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "e0ad035d0b58"
down_revision: Union[str, Sequence[str], None] = "e3bfbc2127a8"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "users", sa.Column("hashed_password", sa.String(length=200), nullable=False)
    )
    op.drop_column("users", "hashed_assword")


def downgrade() -> None:
    op.add_column(
        "users",
        sa.Column(
            "hashed_assword",
            sa.VARCHAR(length=200),
            autoincrement=False,
            nullable=False,
        ),
    )
    op.drop_column("users", "hashed_password")
