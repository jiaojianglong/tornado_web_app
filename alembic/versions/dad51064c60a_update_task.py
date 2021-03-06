"""update_task

Revision ID: dad51064c60a
Revises: 0eefe0e4de5f
Create Date: 2021-03-07 16:36:40.571879

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'dad51064c60a'
down_revision = '0eefe0e4de5f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('task_log', sa.Column('log_str', sa.Text(), nullable=False))
    op.drop_index('ix_task_log_task_id', table_name='task_log')
    op.drop_column('task_log', 'log')
    op.drop_column('task_log', 'task_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('task_log', sa.Column('task_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.add_column('task_log', sa.Column('log', mysql.TEXT(), nullable=False))
    op.create_index('ix_task_log_task_id', 'task_log', ['task_id'], unique=False)
    op.drop_column('task_log', 'log_str')
    # ### end Alembic commands ###
