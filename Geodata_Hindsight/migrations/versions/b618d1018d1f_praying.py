"""Praying

Revision ID: b618d1018d1f
Revises: 
Create Date: 2019-12-02 16:53:35.019615

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b618d1018d1f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('company',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('company_name', sa.String(length=64), nullable=True),
    sa.Column('company_email', sa.String(length=120), nullable=True),
    sa.Column('company_address', sa.String(length=200), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_company_company_address'), 'company', ['company_address'], unique=True)
    op.create_index(op.f('ix_company_company_email'), 'company', ['company_email'], unique=True)
    op.create_index(op.f('ix_company_company_name'), 'company', ['company_name'], unique=True)
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('company_id', sa.Integer(), nullable=True),
    sa.Column('manager', sa.Boolean(), nullable=True),
    sa.Column('admin', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['company_id'], ['company.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    op.drop_index(op.f('ix_company_company_name'), table_name='company')
    op.drop_index(op.f('ix_company_company_email'), table_name='company')
    op.drop_index(op.f('ix_company_company_address'), table_name='company')
    op.drop_table('company')
    # ### end Alembic commands ###
