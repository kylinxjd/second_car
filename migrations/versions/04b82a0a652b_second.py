"""'second'

Revision ID: 04b82a0a652b
Revises: aee1b18670b3
Create Date: 2019-07-10 11:03:34.708109

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '04b82a0a652b'
down_revision = 'aee1b18670b3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('sc_brand',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=20), nullable=True),
    sa.Column('car_style', sa.String(length=50), nullable=True),
    sa.Column('car_style_detail', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('sc_cars',
    sa.Column('is_delete', sa.Boolean(), nullable=True),
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.Column('update_time', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('brand_id', sa.Integer(), nullable=True),
    sa.Column('price', sa.Integer(), nullable=False),
    sa.Column('age', sa.Integer(), nullable=True),
    sa.Column('vehicle_model', sa.String(length=20), nullable=True),
    sa.Column('gear_box', sa.Integer(), nullable=True),
    sa.Column('milage', sa.DECIMAL(), nullable=True),
    sa.Column('displacement', sa.Float(), nullable=True),
    sa.Column('car_register_time', sa.DateTime(), nullable=True),
    sa.Column('car_num', sa.String(length=50), nullable=True),
    sa.Column('color', sa.String(length=10), nullable=True),
    sa.Column('car_oil', sa.String(length=10), nullable=True),
    sa.Column('emission_standard', sa.String(length=10), nullable=True),
    sa.Column('seat_num', sa.Integer(), nullable=True),
    sa.Column('transfer_num', sa.Integer(), nullable=True),
    sa.Column('inspect_annually', sa.String(length=10), nullable=True),
    sa.Column('compulsory_insurance', sa.String(length=10), nullable=True),
    sa.Column('commercial_annually', sa.String(length=10), nullable=True),
    sa.Column('index_image_url', sa.String(length=100), nullable=True),
    sa.ForeignKeyConstraint(['brand_id'], ['sc_brand.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['sc_users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('sc_car_img',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('car_id', sa.Integer(), nullable=True),
    sa.Column('url', sa.String(length=100), nullable=True),
    sa.ForeignKeyConstraint(['car_id'], ['sc_cars.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('sc_car_img')
    op.drop_table('sc_cars')
    op.drop_table('sc_brand')
    # ### end Alembic commands ###
