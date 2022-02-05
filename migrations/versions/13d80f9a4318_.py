"""empty message

Revision ID: 13d80f9a4318
Revises: a5e213dc3583
Create Date: 2022-02-05 12:40:39.689142

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '13d80f9a4318'
down_revision = 'a5e213dc3583'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('banner',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=200), nullable=False, comment='轮播图名称'),
    sa.Column('image_url', sa.String(length=250), nullable=False, comment='图片链接'),
    sa.Column('link_url', sa.String(length=250), nullable=False, comment='跳转链接'),
    sa.Column('priority', sa.Integer(), nullable=True, comment='优先级'),
    sa.Column('create_time', sa.DateTime(), nullable=True, comment='创建时间'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('comment',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('content', sa.Text(), nullable=False, comment='评论内容'),
    sa.Column('create_time', sa.DateTime(), nullable=True, comment='创建时间'),
    sa.Column('post_id', sa.Integer(), nullable=True, comment='所属贴子id'),
    sa.Column('author_id', sa.String(length=100), nullable=False, comment='所属作者id'),
    sa.ForeignKeyConstraint(['author_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['post_id'], ['post.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('comment')
    op.drop_table('banner')
    # ### end Alembic commands ###