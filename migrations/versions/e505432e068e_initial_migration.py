"""Initial migration

Revision ID: e505432e068e
Revises: 
Create Date: 2024-11-16 22:26:30.944456

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e505432e068e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('survey_response',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('q1_time', sa.Integer(), nullable=True),
    sa.Column('q1_closeness', sa.Integer(), nullable=True),
    sa.Column('q1_data', sa.JSON(), nullable=True),
    sa.Column('q2_time', sa.Integer(), nullable=True),
    sa.Column('q2_closeness', sa.Integer(), nullable=True),
    sa.Column('q2_data', sa.JSON(), nullable=True),
    sa.Column('q3_time', sa.Integer(), nullable=True),
    sa.Column('q3_closeness', sa.Integer(), nullable=True),
    sa.Column('q3_data', sa.JSON(), nullable=True),
    sa.Column('q4_time', sa.Integer(), nullable=True),
    sa.Column('q4_closeness', sa.Integer(), nullable=True),
    sa.Column('q4_data', sa.JSON(), nullable=True),
    sa.Column('q5_time', sa.Integer(), nullable=True),
    sa.Column('q5_closeness', sa.Integer(), nullable=True),
    sa.Column('q5_data', sa.JSON(), nullable=True),
    sa.Column('q6_time', sa.Integer(), nullable=True),
    sa.Column('q6_closeness', sa.Integer(), nullable=True),
    sa.Column('q6_data', sa.JSON(), nullable=True),
    sa.Column('q7_time', sa.Integer(), nullable=True),
    sa.Column('q7_closeness', sa.Integer(), nullable=True),
    sa.Column('q7_data', sa.JSON(), nullable=True),
    sa.Column('q8_time', sa.Integer(), nullable=True),
    sa.Column('q8_closeness', sa.Integer(), nullable=True),
    sa.Column('q8_data', sa.JSON(), nullable=True),
    sa.Column('q9_time', sa.Integer(), nullable=True),
    sa.Column('q9_closeness', sa.Integer(), nullable=True),
    sa.Column('q9_data', sa.JSON(), nullable=True),
    sa.Column('q10_time', sa.Integer(), nullable=True),
    sa.Column('q10_closeness', sa.Integer(), nullable=True),
    sa.Column('q10_data', sa.JSON(), nullable=True),
    sa.Column('q11_time', sa.Integer(), nullable=True),
    sa.Column('q11_closeness', sa.Integer(), nullable=True),
    sa.Column('q11_data', sa.JSON(), nullable=True),
    sa.Column('q12_time', sa.Integer(), nullable=True),
    sa.Column('q12_closeness', sa.Integer(), nullable=True),
    sa.Column('q12_data', sa.JSON(), nullable=True),
    sa.Column('q13_time', sa.Integer(), nullable=True),
    sa.Column('q13_closeness', sa.Integer(), nullable=True),
    sa.Column('q13_data', sa.JSON(), nullable=True),
    sa.Column('q14_time', sa.Integer(), nullable=True),
    sa.Column('q14_closeness', sa.Integer(), nullable=True),
    sa.Column('q14_data', sa.JSON(), nullable=True),
    sa.Column('q15_time', sa.Integer(), nullable=True),
    sa.Column('q15_closeness', sa.Integer(), nullable=True),
    sa.Column('q15_data', sa.JSON(), nullable=True),
    sa.Column('q16_time', sa.Integer(), nullable=True),
    sa.Column('q16_closeness', sa.Integer(), nullable=True),
    sa.Column('q16_data', sa.JSON(), nullable=True),
    sa.Column('q17_time', sa.Integer(), nullable=True),
    sa.Column('q17_closeness', sa.Integer(), nullable=True),
    sa.Column('q17_data', sa.JSON(), nullable=True),
    sa.Column('q18_time', sa.Integer(), nullable=True),
    sa.Column('q18_closeness', sa.Integer(), nullable=True),
    sa.Column('q18_data', sa.JSON(), nullable=True),
    sa.Column('q19_time', sa.Integer(), nullable=True),
    sa.Column('q19_closeness', sa.Integer(), nullable=True),
    sa.Column('q19_data', sa.JSON(), nullable=True),
    sa.Column('q20_time', sa.Integer(), nullable=True),
    sa.Column('q20_closeness', sa.Integer(), nullable=True),
    sa.Column('q20_data', sa.JSON(), nullable=True),
    sa.Column('timestamp2', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('survey_response')
    # ### end Alembic commands ###
