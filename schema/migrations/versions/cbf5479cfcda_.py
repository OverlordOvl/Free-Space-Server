"""empty message

Revision ID: cbf5479cfcda
Revises: None
Create Date: 2021-12-12 00:38:56.652120

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cbf5479cfcda'
down_revision = None


def upgrade():
    op.create_table('user',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('username', sa.VARCHAR(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('user')
