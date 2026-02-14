"""Email coloumn now is unique

Revision ID: f4bed2584b0e
Revises: e0ad035d0b58
Create Date: 2026-02-14 10:03:01.508473

"""

from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "f4bed2584b0e"
down_revision: Union[str, Sequence[str], None] = "e0ad035d0b58"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_unique_constraint(None, "users", ["email"])


def downgrade() -> None:
    op.drop_constraint(None, "users", type_="unique")
