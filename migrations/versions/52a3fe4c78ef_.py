"""empty message

Revision ID: 52a3fe4c78ef
Revises: e699c2d67205
Create Date: 2019-12-15 19:38:43.222258

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '52a3fe4c78ef'
down_revision = 'e699c2d67205'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('goods', 'state')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('goods', sa.Column('state', mysql.TINYINT(display_width=4), autoincrement=False, nullable=True, comment='审核状态, 0待审核, 1审核通过, 2不通过'))
    # ### end Alembic commands ###