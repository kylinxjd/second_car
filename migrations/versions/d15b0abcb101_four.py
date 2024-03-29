"""'four'

Revision ID: d15b0abcb101
Revises: 8cf26dea1625
Create Date: 2019-07-12 09:50:19.713048

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd15b0abcb101'
down_revision = '8cf26dea1625'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('name', table_name='sc_brand')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index('name', 'sc_brand', ['name'], unique=True)
    # ### end Alembic commands ###
