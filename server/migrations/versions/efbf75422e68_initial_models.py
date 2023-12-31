"""Initial models

Revision ID: efbf75422e68
Revises: 
Create Date: 2023-10-08 18:14:05.251315

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'efbf75422e68'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('issue',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('owner',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(), nullable=True),
    sa.Column('last_name', sa.String(), nullable=True),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('_password_hash', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tenant',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(), nullable=True),
    sa.Column('last_name', sa.String(), nullable=True),
    sa.Column('email', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('property',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('location', sa.String(), nullable=True),
    sa.Column('owner_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['owner_id'], ['owner.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('house',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('unit', sa.String(), nullable=True),
    sa.Column('tenant_id', sa.Integer(), nullable=True),
    sa.Column('property_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['property_id'], ['property.id'], ),
    sa.ForeignKeyConstraint(['tenant_id'], ['tenant.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('house_issue',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('house_id', sa.Integer(), nullable=True),
    sa.Column('issue_id', sa.Integer(), nullable=True),
    sa.Column('detail', sa.String(), nullable=True),
    sa.Column('status', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['house_id'], ['house.id'], ),
    sa.ForeignKeyConstraint(['issue_id'], ['issue.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('house_issue')
    op.drop_table('house')
    op.drop_table('property')
    op.drop_table('tenant')
    op.drop_table('owner')
    op.drop_table('issue')
    # ### end Alembic commands ###
