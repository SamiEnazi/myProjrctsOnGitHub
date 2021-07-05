"""empty message

Revision ID: bc3621bef007
Revises: 3f52f85de4e6
Create Date: 2021-06-20 06:54:22.514043

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bc3621bef007'
down_revision = '3f52f85de4e6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('shows', sa.Column('venue_id', sa.Integer(), nullable=True))
    op.add_column('shows', sa.Column('start_date', sa.DateTime(), nullable=True))
    op.create_foreign_key(None, 'shows', 'venue', ['venue_id'], ['id'])
    op.drop_column('shows', 'id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('shows', sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False))
    op.drop_constraint(None, 'shows', type_='foreignkey')
    op.drop_column('shows', 'start_date')
    op.drop_column('shows', 'venue_id')
    # ### end Alembic commands ###
