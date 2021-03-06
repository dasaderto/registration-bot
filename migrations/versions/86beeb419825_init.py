"""init

Revision ID: 86beeb419825
Revises: 
Create Date: 2022-02-20 23:06:16.545498

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '86beeb419825'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('tg_first_name', sa.String(length=255), nullable=True),
    sa.Column('tg_last_name', sa.String(length=255), nullable=True),
    sa.Column('tg_username', sa.String(length=255), nullable=True),
    sa.Column('tg_raw_user', postgresql.JSON(astext_type=sa.Text()), nullable=True),
    sa.Column('phone', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_table('users')
    # ### end Alembic commands ###
