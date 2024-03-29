"""'five'

Revision ID: 604afba8f835
Revises: d15b0abcb101
Create Date: 2019-07-12 13:57:38.538782

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '604afba8f835'
down_revision = 'd15b0abcb101'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('s_c',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('car_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['car_id'], ['sc_cars.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['sc_users.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'car_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('s_c')
    # ### end Alembic commands ###
