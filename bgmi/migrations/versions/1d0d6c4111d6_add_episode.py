"""add episode

Revision ID: 1d0d6c4111d6
Revises: c6a7c781b99b
Create Date: 2020-02-25 22:06:20.588339

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "1d0d6c4111d6"
down_revision = "c6a7c781b99b"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "episode",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("source", sa.String(length=40), nullable=False),
        sa.Column("series", sa.String(length=255), nullable=True),
        sa.Column("url", sa.String(length=255), nullable=True),
        sa.Column("date", sa.Date(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_episode_series"), "episode", ["series"], unique=False)
    op.create_index(op.f("ix_episode_source"), "episode", ["source"], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_episode_source"), table_name="episode")
    op.drop_index(op.f("ix_episode_series"), table_name="episode")
    op.drop_table("episode")
    # ### end Alembic commands ###