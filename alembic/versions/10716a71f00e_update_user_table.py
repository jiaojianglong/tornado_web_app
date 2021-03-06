"""update user table

Revision ID: 10716a71f00e
Revises: 77d08c67ef64
Create Date: 2020-07-21 11:04:08.169066

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '10716a71f00e'
down_revision = '77d08c67ef64'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('email', sa.String(length=64), nullable=True, comment='邮箱'))
    op.add_column('user', sa.Column('password_code', sa.String(length=128), nullable=True, comment='密码'))
    op.alter_column('user', 'username',
               existing_type=mysql.VARCHAR(length=30),
               comment='用户名',
               existing_nullable=True)
    op.drop_column('user', 'password')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('password', mysql.VARCHAR(length=128), nullable=True))
    op.alter_column('user', 'username',
               existing_type=mysql.VARCHAR(length=30),
               comment=None,
               existing_comment='用户名',
               existing_nullable=True)
    op.drop_column('user', 'password_code')
    op.drop_column('user', 'email')
    # ### end Alembic commands ###
