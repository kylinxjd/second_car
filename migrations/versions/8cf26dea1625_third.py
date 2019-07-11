"""'third'

Revision ID: 8cf26dea1625
Revises: 04b82a0a652b
Create Date: 2019-07-10 11:52:55.175450

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8cf26dea1625'
down_revision = '04b82a0a652b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('sc_order',
    sa.Column('is_delete', sa.Boolean(), nullable=True),
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.Column('update_time', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('car_id', sa.Integer(), nullable=True),
    sa.Column('order_time', sa.DateTime(), nullable=True),
    sa.Column('car_price', sa.Float(), nullable=True),
    sa.Column('service_charge', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['car_id'], ['sc_cars.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['sc_users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('sc_order')
    # ### end Alembic commands ###