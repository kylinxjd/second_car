"""'first'

Revision ID: aee1b18670b3
Revises: 
Create Date: 2019-07-09 16:40:08.187605

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'aee1b18670b3'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('sc_users',
    sa.Column('is_delete', sa.Boolean(), nullable=True),
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.Column('update_time', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=20), nullable=True),
    sa.Column('password', sa.String(length=100), nullable=True),
    sa.Column('phone', sa.String(length=11), nullable=False),
    sa.Column('id_card', sa.String(length=18), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('sc_users')
    # ### end Alembic commands ###
