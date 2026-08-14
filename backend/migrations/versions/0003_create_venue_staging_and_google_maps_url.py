"""create venue_staging table and add google_maps_url to venues

Revision ID: 0003_venue_staging
Revises: 557ea531c5de
Create Date: 2026-08-14 16:30:00.000000

"""
from collections.abc import Sequence

import geoalchemy2
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '0003_venue_staging'
down_revision: str | None = '557ea531c5de'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # Add google_maps_url column to venues table
    op.add_column('venues', sa.Column('google_maps_url', sa.Text(), nullable=True))

    # Create venue_staging table
    op.create_table(
        'venue_staging',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('place_id', sa.String(length=255), nullable=False),
        sa.Column('google_maps_url', sa.Text(), nullable=False),
        sa.Column('name_raw', sa.String(length=255), nullable=False),
        sa.Column('address_raw', sa.Text(), nullable=False),
        sa.Column(
            'location',
            geoalchemy2.types.Geometry(geometry_type='POINT', srid=4326, from_text='ST_GeomFromEWKT', name='geometry'),
            nullable=False,
        ),
        sa.Column('raw_payload', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('enriched_payload', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('status', sa.String(length=50), nullable=False, server_default='PENDING_CURATION'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('place_id')
    )
    op.create_index(op.f('ix_venue_staging_place_id'), 'venue_staging', ['place_id'], unique=True)
    op.create_index(op.f('ix_venue_staging_status'), 'venue_staging', ['status'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_venue_staging_status'), table_name='venue_staging')
    op.drop_index(op.f('ix_venue_staging_place_id'), table_name='venue_staging')
    op.drop_table('venue_staging')
    op.drop_column('venues', 'google_maps_url')
