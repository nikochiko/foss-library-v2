"""Add members table

Revision ID: 620a384a09fd
Revises: 14203f9e0fc7
Create Date: 2021-09-22 12:27:49.167354

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "620a384a09fd"
down_revision = "14203f9e0fc7"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "member",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("first_name", sa.String(), nullable=True),
        sa.Column("last_name", sa.String(), nullable=True),
        sa.Column("email", sa.String(), nullable=True),
        sa.Column("gravatar_url", sa.String(), nullable=True),
        sa.Column("dues_paid", sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("member")
    # ### end Alembic commands ###