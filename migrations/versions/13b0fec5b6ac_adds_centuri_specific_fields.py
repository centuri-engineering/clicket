"""adds centuri specific fields

Revision ID: 13b0fec5b6ac
Revises:
Create Date: 2020-02-05 10:37:49.288262

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "13b0fec5b6ac"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "flicket_topic", sa.Column("requester", sa.String(length=128), nullable=True)
    )
    op.add_column(
        "flicket_topic", sa.Column("requester_role", sa.Integer(), nullable=True)
    )
    op.add_column(
        "flicket_topic", sa.Column("requester_role_id", sa.Integer(), nullable=True)
    )


def downgrade():
    pass
