"""update_action_table

Revision ID: 681938fc2ac1
Revises: 5dda03b65708
Create Date: 2020-11-30 20:39:10.561442

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '681938fc2ac1'
down_revision = '5dda03b65708'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('action', sa.Column('description', sa.String(length=81), nullable=False, comment='动作描述'))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('action', 'description')
    # ### end Alembic commands ###
