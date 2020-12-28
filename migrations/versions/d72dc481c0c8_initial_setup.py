"""initial_setup

Revision ID: d72dc481c0c8
Revises: 
Create Date: 2020-12-28 01:05:28.705670

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd72dc481c0c8'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('stand',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('external_id', sa.String(length=36), nullable=True),
    sa.Column('registration_id', sa.String(length=10), nullable=True),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('status', sa.String(length=64), nullable=True),
    sa.Column('status_date', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('registration_id')
    )
    op.create_index(op.f('ix_stand_external_id'), 'stand', ['external_id'], unique=True)
    op.create_table('status_history',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('stand_id', sa.Integer(), nullable=True),
    sa.Column('status', sa.String(length=64), nullable=True),
    sa.Column('status_date', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['stand_id'], ['stand.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('status_history')
    op.drop_index(op.f('ix_stand_external_id'), table_name='stand')
    op.drop_table('stand')
    # ### end Alembic commands ###