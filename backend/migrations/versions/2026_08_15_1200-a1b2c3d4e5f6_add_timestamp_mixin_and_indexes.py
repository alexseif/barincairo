"""add timestamp mixin and foreign key indexes

Revision ID: a1b2c3d4e5f6
Revises: 04f8795f4bfc
Create Date: 2026-08-15 12:00:00.000000

"""
from collections.abc import Sequence
from typing import Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'a1b2c3d4e5f6'
down_revision: Union[str, None] = '04f8795f4bfc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # categories
    op.add_column('categories', sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False))
    op.add_column('categories', sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False))

    # vibe_tags
    op.add_column('vibe_tags', sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False))
    op.add_column('vibe_tags', sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False))

    # venues
    op.add_column('venues', sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False))
    op.create_index(op.f('ix_venues_category_id'), 'venues', ['category_id'], unique=False)

    # venue_photos
    op.add_column('venue_photos', sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False))
    op.add_column('venue_photos', sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False))
    op.create_index(op.f('ix_venue_photos_venue_id'), 'venue_photos', ['venue_id'], unique=False)

    # subscribers
    op.add_column('subscribers', sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False))

    # users
    op.add_column('users', sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False))


def downgrade() -> None:
    op.drop_column('users', 'updated_at')
    op.drop_column('subscribers', 'updated_at')
    op.drop_index(op.f('ix_venue_photos_venue_id'), table_name='venue_photos')
    op.drop_column('venue_photos', 'updated_at')
    op.drop_column('venue_photos', 'created_at')
    op.drop_index(op.f('ix_venues_category_id'), table_name='venues')
    op.drop_column('venues', 'updated_at')
    op.drop_column('vibe_tags', 'updated_at')
    op.drop_column('vibe_tags', 'created_at')
    op.drop_column('categories', 'updated_at')
    op.drop_column('categories', 'created_at')
