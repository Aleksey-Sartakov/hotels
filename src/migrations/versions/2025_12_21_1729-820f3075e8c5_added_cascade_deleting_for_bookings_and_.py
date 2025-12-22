"""Added cascade deleting for bookings and facilities

Revision ID: 820f3075e8c5
Revises: a3839ad1be22
Create Date: 2025-12-21 17:29:41.504402

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "820f3075e8c5"
down_revision: Union[str, Sequence[str], None] = "a3839ad1be22"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.drop_constraint(op.f("bookings_user_id_fkey"), "bookings", type_="foreignkey")
    op.drop_constraint(op.f("bookings_room_id_fkey"), "bookings", type_="foreignkey")
    op.create_foreign_key("bookings_user_id_fkey", "bookings", "users", ["user_id"], ["id"], ondelete="CASCADE")
    op.create_foreign_key("bookings_room_id_fkey", "bookings", "rooms", ["room_id"], ["id"], ondelete="CASCADE")
    op.drop_constraint(op.f("rooms_to_facilities_facility_id_fkey"), "rooms_to_facilities", type_="foreignkey")
    op.drop_constraint(op.f("rooms_to_facilities_room_id_fkey"), "rooms_to_facilities", type_="foreignkey")
    op.create_foreign_key("rooms_to_facilities_facility_id_fkey", "rooms_to_facilities", "facilities", ["facility_id"], ["id"], ondelete="CASCADE")
    op.create_foreign_key("rooms_to_facilities_room_id_fkey", "rooms_to_facilities", "rooms", ["room_id"], ["id"], ondelete="CASCADE")


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_constraint("rooms_to_facilities_facility_id_fkey", "rooms_to_facilities", type_="foreignkey")
    op.drop_constraint("rooms_to_facilities_room_id_fkey", "rooms_to_facilities", type_="foreignkey")
    op.create_foreign_key(op.f("rooms_to_facilities_room_id_fkey"), "rooms_to_facilities", "rooms", ["room_id"], ["id"])
    op.create_foreign_key(
        op.f("rooms_to_facilities_facility_id_fkey"), "rooms_to_facilities", "facilities", ["facility_id"], ["id"]
    )
    op.drop_constraint("bookings_user_id_fkey", "bookings", type_="foreignkey")
    op.drop_constraint("bookings_room_id_fkey", "bookings", type_="foreignkey")
    op.create_foreign_key(op.f("bookings_room_id_fkey"), "bookings", "rooms", ["room_id"], ["id"])
    op.create_foreign_key(op.f("bookings_user_id_fkey"), "bookings", "users", ["user_id"], ["id"])
