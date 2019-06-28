"""empty message

Revision ID: 1fc3e870b516
Revises: 9dc2af2810b8
Create Date: 2019-06-27 21:25:40.338350

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1fc3e870b516'
down_revision = '9dc2af2810b8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('expenses', 'recieved')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('expenses', sa.Column('recieved', sa.BOOLEAN(), nullable=True))
    # ### end Alembic commands ###
