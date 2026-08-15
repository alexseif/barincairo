"""add name and email to subscribers and make whatsapp_number nullable

Revision ID: b2c3d4e5f6a7
Revises: a1b2c3d4e5f6
Create Date: 2026-08-16 00:00:00.000000

"""
from collections.abc import Sequence
from typing import Union

import sqlalchemy as sa
from alembic import op

revision: str = 'b2c3d4e5f6a7'
down_revision: Union[str, None] = 'a1b2c3d4e5f6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("ALTER TABLE subscribers ADD COLUMN IF NOT EXISTS name VARCHAR(100)")
    op.execute("ALTER TABLE subscribers ADD COLUMN IF NOT EXISTS email VARCHAR(255)")
    op.execute("ALTER TABLE subscribers ALTER COLUMN whatsapp_number DROP NOT NULL")
    op.execute("CREATE UNIQUE INDEX IF NOT EXISTS ix_subscribers_email ON subscribers (email)")


def downgrade() -> None:
    op.drop_index(op.f('ix_subscribers_email'), table_name='subscribers')
    op.alter_column('subscribers', 'whatsapp_number', existing_type=sa.String(length=30), nullable=False)
    op.drop_column('subscribers', 'email')
    op.drop_column('subscribers', 'name')
