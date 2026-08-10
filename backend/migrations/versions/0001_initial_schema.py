"""initial schema and seed data

Revision ID: 0001_initial_schema
Revises: 
Create Date: 2026-08-10 12:35:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
import geoalchemy2

revision: str = '0001_initial_schema'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Ensure PostGIS extension exists
    op.execute("CREATE EXTENSION IF NOT EXISTS postgis;")

    # Create Categories
    op.create_table(
        'categories',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('slug', sa.String(length=50), nullable=False),
        sa.Column('name_en', sa.String(length=100), nullable=False),
        sa.Column('name_ar', sa.String(length=100), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('slug')
    )
    op.create_index(op.f('ix_categories_id'), 'categories', ['id'], unique=False)
    op.create_index(op.f('ix_categories_slug'), 'categories', ['slug'], unique=True)

    # Create Vibe Tags
    op.create_table(
        'vibe_tags',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('slug', sa.String(length=50), nullable=False),
        sa.Column('name_en', sa.String(length=100), nullable=False),
        sa.Column('name_ar', sa.String(length=100), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('slug')
    )
    op.create_index(op.f('ix_vibe_tags_id'), 'vibe_tags', ['id'], unique=False)
    op.create_index(op.f('ix_vibe_tags_slug'), 'vibe_tags', ['slug'], unique=True)

    # Create Venues
    op.create_table(
        'venues',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('category_id', sa.Integer(), nullable=False),
        sa.Column('slug', sa.String(length=100), nullable=False),
        sa.Column('name_en', sa.String(length=150), nullable=False),
        sa.Column('name_ar', sa.String(length=150), nullable=False),
        sa.Column('description_en', sa.Text(), nullable=True),
        sa.Column('description_ar', sa.Text(), nullable=True),
        sa.Column('address_en', sa.String(length=255), nullable=False),
        sa.Column('address_ar', sa.String(length=255), nullable=False),
        sa.Column('location', geoalchemy2.types.Geometry(geometry_type='POINT', srid=4326, from_text='ST_GeomFromEWKT', name='geometry'), nullable=False),
        sa.Column('price_range', sa.String(length=10), server_default='$$', nullable=False),
        sa.Column('vibe_description', sa.String(length=255), nullable=True),
        sa.Column('photo_url', sa.String(length=500), nullable=True),
        sa.Column('is_active', sa.Boolean(), server_default='true', nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['category_id'], ['categories.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('slug')
    )
    op.create_index(op.f('ix_venues_id'), 'venues', ['id'], unique=False)
    op.create_index(op.f('ix_venues_slug'), 'venues', ['slug'], unique=True)

    # Create Venue Vibes Junction Table
    op.create_table(
        'venue_vibes',
        sa.Column('venue_id', sa.Integer(), nullable=False),
        sa.Column('vibe_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['venue_id'], ['venues.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['vibe_id'], ['vibe_tags.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('venue_id', 'vibe_id')
    )

    # Create Venue Photos
    op.create_table(
        'venue_photos',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('venue_id', sa.Integer(), nullable=False),
        sa.Column('photo_url', sa.String(length=500), nullable=False),
        sa.Column('caption', sa.String(length=255), nullable=True),
        sa.ForeignKeyConstraint(['venue_id'], ['venues.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

    # Create Subscribers
    op.create_table(
        'subscribers',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('whatsapp_number', sa.String(length=30), nullable=False),
        sa.Column('source', sa.String(length=50), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('whatsapp_number')
    )
    op.create_index(op.f('ix_subscribers_id'), 'subscribers', ['id'], unique=False)
    op.create_index(op.f('ix_subscribers_whatsapp_number'), 'subscribers', ['whatsapp_number'], unique=True)

    # Seed Initial Categories
    op.execute("""
        INSERT INTO categories (id, slug, name_en, name_ar) VALUES
        (1, 'live-music', 'Live music', 'موسيقى حية'),
        (2, 'cocktail-bar', 'Cocktail bar', 'بار كوكتيل'),
        (3, 'rooftop', 'Rooftop', 'روفتوب'),
        (4, 'cafe-bar', 'Cafe bar', 'كافيه بار');
    """)

    # Seed Expanded Cairo Vibe Tags
    op.execute("""
        INSERT INTO vibe_tags (id, slug, name_en, name_ar) VALUES
        (1, 'fancy', 'Fancy', 'فاخر'),
        (2, 'ambient-music', 'Ambient music', 'موسيقى هادئة'),
        (3, 'live-performance', 'Live performance', 'عروض حية'),
        (4, 'oud-player', 'Oud player', 'عازف عود'),
        (5, 'old-times', 'Old times', 'زمن جميل'),
        (6, 'dancy', 'Dancy', 'راقص'),
        (7, 'flirty', 'Flirty', 'مرح'),
        (8, 'intimate', 'Intimate', 'حميمي'),
        (9, 'golden-hour', 'Golden hour', 'الساعة الذهبية'),
        (10, 'late-night', 'Late-night', 'سهرة متأخرة');
    """)

    # Seed Initial Prototype Venues
    op.execute("""
        INSERT INTO venues (id, category_id, slug, name_en, name_ar, description_en, address_en, address_ar, location, price_range, vibe_description, photo_url, is_active) VALUES
        (1, 1, 'cairo-jazz-610', 'Cairo Jazz Club 610', 'كايرو جاز كلوب', 'A beloved institution for live sets, smoky corners, and the city’s most reliable midnight energy.', '610, First New Cairo', '٦١٠ التجمع الأول', ST_SetSRID(ST_MakePoint(31.4289, 30.0384), 4326), '$$$', 'Late-night / electric', 'https://images.unsplash.com/photo-1514525253161-7a46d19cd819?auto=format&fit=crop&w=900&q=80', true),
        (2, 2, 'vent-downtown', 'Vent', 'فِنت', 'A small, low-lit room for beautifully balanced drinks and long conversations.', '12 El-Horeya, Downtown', '١٢ شارع الحرية، وسط البلد', ST_SetSRID(ST_MakePoint(31.2389, 30.0444), 4326), '$$', 'Intimate / considered', 'https://images.unsplash.com/photo-1515003197210-e0cd71810b5f?auto=format&fit=crop&w=900&q=80', true),
        (3, 3, 'horus-rooftop', 'Horus Rooftop', 'حورس', 'Watch the downtown rooftops turn copper over a cold Sakara and a plate of mezze.', 'Talaat Harb Square', 'ميدان طلعت حرب', ST_SetSRID(ST_MakePoint(31.2398, 30.0468), 4326), '$$', 'Golden hour / open-air', 'https://images.unsplash.com/photo-1572116469696-31de0f17cc34?auto=format&fit=crop&w=900&q=80', true),
        (4, 4, 'soma-caffe', 'Soma Caffe', 'سوما كافيه', 'A daytime cafe that quietly becomes one of Downtown’s favorite after-dark hideouts.', '26 Sherif Street', '٢٦ شارع شريف', ST_SetSRID(ST_MakePoint(31.2415, 30.0452), 4326), '$', 'Quiet / all-day', 'https://images.unsplash.com/photo-1514933651103-005eec06c04b?auto=format&fit=crop&w=900&q=80', true);
    """)

    # Connect Seed Venues with Vibe Tags
    op.execute("""
        INSERT INTO venue_vibes (venue_id, vibe_id) VALUES
        (1, 3), (1, 6), (1, 10), -- Cairo Jazz: Live performance, Dancy, Late-night
        (2, 2), (2, 8), (2, 5),  -- Vent: Ambient music, Intimate, Old times
        (3, 1), (3, 4), (3, 9),  -- Horus: Fancy, Oud player, Golden hour
        (4, 2), (4, 5), (4, 7);  -- Soma: Ambient music, Old times, Flirty
    """)


def downgrade() -> None:
    op.drop_table('subscribers')
    op.drop_table('venue_photos')
    op.drop_table('venue_vibes')
    op.drop_table('venues')
    op.drop_table('vibe_tags')
    op.drop_table('categories')
