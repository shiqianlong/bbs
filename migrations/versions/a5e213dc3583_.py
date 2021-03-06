"""empty message

Revision ID: a5e213dc3583
Revises: 5263a294620c
Create Date: 2022-02-05 12:32:32.133513

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a5e213dc3583'
down_revision = '5263a294620c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('post',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('title', sa.String(length=200), nullable=False, comment='贴子标题'),
    sa.Column('content', sa.Text(), nullable=False, comment='内容'),
    sa.Column('create_time', sa.DateTime(), nullable=True, comment='创建时间'),
    sa.Column('board_id', sa.Integer(), nullable=True, comment='所属板块id'),
    sa.Column('author_id', sa.String(length=100), nullable=True, comment='所属作者id'),
    sa.ForeignKeyConstraint(['author_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['board_id'], ['board.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('post')
    # ### end Alembic commands ###
