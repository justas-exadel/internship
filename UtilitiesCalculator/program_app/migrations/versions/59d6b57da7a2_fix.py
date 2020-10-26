"""fix

Revision ID: 59d6b57da7a2
Revises: 
Create Date: 2020-10-26 22:18:09.611518

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '59d6b57da7a2'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'APARTMENT', type_='foreignkey')
    op.drop_column('APARTMENT', 'renter_ID')
    op.add_column('RENTER', sa.Column('apartment_ID', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'RENTER', 'APARTMENT', ['apartment_ID'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'RENTER', type_='foreignkey')
    op.drop_column('RENTER', 'apartment_ID')
    op.add_column('APARTMENT', sa.Column('renter_ID', sa.INTEGER(), nullable=True))
    op.create_foreign_key(None, 'APARTMENT', 'RENTER', ['renter_ID'], ['id'])
    # ### end Alembic commands ###