"""empty message

Revision ID: 1b347b521d8f
Revises: 46a402810309
Create Date: 2019-07-10 00:11:11.018874

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1b347b521d8f'
down_revision = '46a402810309'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('post', sa.Column('image_src', sa.String(length=200), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('post', 'image_src')
    # ### end Alembic commands ###
