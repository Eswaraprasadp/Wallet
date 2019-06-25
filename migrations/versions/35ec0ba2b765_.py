"""empty message

Revision ID: 35ec0ba2b765
Revises: 1c8a4413e52e
Create Date: 2019-06-25 15:44:36.673181

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '35ec0ba2b765'
down_revision = '1c8a4413e52e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('expenses', sa.Column('modified_time', sa.DateTime(), nullable=True))
    op.create_index(op.f('ix_expenses_modified_time'), 'expenses', ['modified_time'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_expenses_modified_time'), table_name='expenses')
    op.drop_column('expenses', 'modified_time')
    # ### end Alembic commands ###
