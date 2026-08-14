"""refactor_single_language_and_working_hours

Revision ID: 04f8795f4bfc
Revises: 0003_venue_staging
Create Date: 2026-08-15 00:46:47.468265

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '04f8795f4bfc'
down_revision: Union[str, None] = '0003_venue_staging'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Categories
    op.add_column('categories', sa.Column('name', sa.String(length=100), nullable=True))
    op.execute("UPDATE categories SET name = name_en")
    op.alter_column('categories', 'name', nullable=False)
    op.drop_column('categories', 'name_en')
    op.drop_column('categories', 'name_ar')

    # Venue Staging
    op.add_column('venue_staging', sa.Column('working_hours', sa.String(length=100), nullable=True))

    # Venues
    op.add_column('venues', sa.Column('name', sa.String(length=150), nullable=True))
    op.add_column('venues', sa.Column('description', sa.Text(), nullable=True))
    op.add_column('venues', sa.Column('address', sa.String(length=255), nullable=True))
    op.add_column('venues', sa.Column('working_hours', sa.String(length=100), nullable=True))
    op.execute("UPDATE venues SET name = name_en, address = address_en, description = description_en")
    op.alter_column('venues', 'name', nullable=False)
    op.alter_column('venues', 'address', nullable=False)
    op.drop_column('venues', 'name_en')
    op.drop_column('venues', 'address_en')
    op.drop_column('venues', 'name_ar')
    op.drop_column('venues', 'description_en')
    op.drop_column('venues', 'description_ar')
    op.drop_column('venues', 'address_ar')

    # Vibe Tags
    op.add_column('vibe_tags', sa.Column('name', sa.String(length=100), nullable=True))
    op.execute("UPDATE vibe_tags SET name = name_en")
    op.alter_column('vibe_tags', 'name', nullable=False)
    op.drop_column('vibe_tags', 'name_en')
    op.drop_column('vibe_tags', 'name_ar')


def downgrade() -> None:
    # Vibe Tags
    op.add_column('vibe_tags', sa.Column('name_en', sa.String(length=100), nullable=True))
    op.add_column('vibe_tags', sa.Column('name_ar', sa.String(length=100), nullable=True))
    op.execute("UPDATE vibe_tags SET name_en = name, name_ar = name")
    op.alter_column('vibe_tags', 'name_en', nullable=False)
    op.alter_column('vibe_tags', 'name_ar', nullable=False)
    op.drop_column('vibe_tags', 'name')

    # Venues
    op.add_column('venues', sa.Column('name_en', sa.String(length=150), nullable=True))
    op.add_column('venues', sa.Column('name_ar', sa.String(length=150), nullable=True))
    op.add_column('venues', sa.Column('address_en', sa.String(length=255), nullable=True))
    op.add_column('venues', sa.Column('address_ar', sa.String(length=255), nullable=True))
    op.add_column('venues', sa.Column('description_en', sa.Text(), nullable=True))
    op.add_column('venues', sa.Column('description_ar', sa.Text(), nullable=True))
    op.execute("UPDATE venues SET name_en = name, name_ar = name, address_en = address, address_ar = address, description_en = description, description_ar = description")
    op.alter_column('venues', 'name_en', nullable=False)
    op.alter_column('venues', 'name_ar', nullable=False)
    op.alter_column('venues', 'address_en', nullable=False)
    op.alter_column('venues', 'address_ar', nullable=False)
    op.drop_column('venues', 'working_hours')
    op.drop_column('venues', 'address')
    op.drop_column('venues', 'description')
    op.drop_column('venues', 'name')

    # Venue Staging
    op.drop_column('venue_staging', 'working_hours')

    # Categories
    op.add_column('categories', sa.Column('name_en', sa.String(length=100), nullable=True))
    op.add_column('categories', sa.Column('name_ar', sa.String(length=100), nullable=True))
    op.execute("UPDATE categories SET name_en = name, name_ar = name")
    op.alter_column('categories', 'name_en', nullable=False)
    op.alter_column('categories', 'name_ar', nullable=False)
    op.drop_column('categories', 'name')
