"""Create ImageTask table

Revision ID: 8666a3fd51cc
Revises: 239ced00d0e1
Create Date: 2024-10-26 23:14:53.369162

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8666a3fd51cc'
down_revision: Union[str, None] = '239ced00d0e1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('image_tasks',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('task_id', sa.String(), nullable=True),
    sa.Column('img_link', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_image_tasks_id'), 'image_tasks', ['id'], unique=False)
    op.create_index(op.f('ix_image_tasks_img_link'), 'image_tasks', ['img_link'], unique=True)
    op.create_index(op.f('ix_image_tasks_task_id'), 'image_tasks', ['task_id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_image_tasks_task_id'), table_name='image_tasks')
    op.drop_index(op.f('ix_image_tasks_img_link'), table_name='image_tasks')
    op.drop_index(op.f('ix_image_tasks_id'), table_name='image_tasks')
    op.drop_table('image_tasks')
    # ### end Alembic commands ###
