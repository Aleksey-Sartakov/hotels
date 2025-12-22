"""Added cascade deleting for rooms

Revision ID: a3839ad1be22
Revises: feb5dd36d31b
Create Date: 2025-12-21 14:42:27.613013

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "a3839ad1be22"
down_revision: Union[str, Sequence[str], None] = "feb5dd36d31b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.drop_constraint(op.f("rooms_hotel_id_fkey"), "rooms", type_="foreignkey")
    op.create_foreign_key("rooms_hotel_id_fkey", "rooms", "hotels", ["hotel_id"], ["id"], ondelete="CASCADE")


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_constraint("rooms_hotel_id_fkey", "rooms", type_="foreignkey")
    op.create_foreign_key(op.f("rooms_hotel_id_fkey"), "rooms", "hotels", ["hotel_id"], ["id"])
