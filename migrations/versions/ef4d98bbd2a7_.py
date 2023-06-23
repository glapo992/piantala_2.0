"""empty message

Revision ID: ef4d98bbd2a7
Revises: 
Create Date: 2023-06-23 15:56:38.221221

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ef4d98bbd2a7'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('identification',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('img_1', sa.String(length=100), nullable=False),
    sa.Column('img_2', sa.String(length=100), nullable=True),
    sa.Column('img_3', sa.String(length=100), nullable=True),
    sa.Column('img_4', sa.String(length=100), nullable=True),
    sa.Column('img_5', sa.String(length=100), nullable=True),
    sa.Column('organ_1', sa.String(length=30), nullable=False),
    sa.Column('organ_2', sa.String(length=30), nullable=True),
    sa.Column('organ_3', sa.String(length=30), nullable=True),
    sa.Column('organ_4', sa.String(length=30), nullable=True),
    sa.Column('organ_5', sa.String(length=30), nullable=True),
    sa.Column('reliability', sa.Float(), nullable=True),
    sa.Column('specie', sa.String(length=50), nullable=True),
    sa.Column('genus', sa.String(length=50), nullable=True),
    sa.Column('family', sa.String(length=50), nullable=True),
    sa.Column('commonName', sa.String(length=50), nullable=True),
    sa.Column('lat', sa.String(length=30), nullable=True),
    sa.Column('long', sa.String(length=30), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('identification', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_identification_timestamp'), ['timestamp'], unique=False)

    op.create_table('identification_mini',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('img_1', sa.String(length=100), nullable=False),
    sa.Column('organ_1', sa.String(length=30), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('identification_mini', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_identification_mini_timestamp'), ['timestamp'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('identification_mini', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_identification_mini_timestamp'))

    op.drop_table('identification_mini')
    with op.batch_alter_table('identification', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_identification_timestamp'))

    op.drop_table('identification')
    # ### end Alembic commands ###
