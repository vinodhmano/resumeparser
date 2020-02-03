"""candidate table

Revision ID: 2009be8dafb9
Revises: 
Create Date: 2019-11-25 14:29:07.671991

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2009be8dafb9'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('candidate',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('firstname', sa.String(length=128), nullable=True),
    sa.Column('middlename', sa.String(length=64), nullable=True),
    sa.Column('lastname', sa.String(length=128), nullable=True),
    sa.Column('email_id', sa.String(length=160), nullable=True),
    sa.Column('contact_number', sa.String(length=20), nullable=True),
    sa.Column('date_added', sa.Date(), nullable=True),
    sa.Column('last_modified', sa.Date(), nullable=True),
    sa.Column('skills', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_candidate_email_id'), 'candidate', ['email_id'], unique=False)
    op.create_index(op.f('ix_candidate_firstname'), 'candidate', ['firstname'], unique=False)
    op.create_index(op.f('ix_candidate_lastname'), 'candidate', ['lastname'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_candidate_lastname'), table_name='candidate')
    op.drop_index(op.f('ix_candidate_firstname'), table_name='candidate')
    op.drop_index(op.f('ix_candidate_email_id'), table_name='candidate')
    op.drop_table('candidate')
    # ### end Alembic commands ###
