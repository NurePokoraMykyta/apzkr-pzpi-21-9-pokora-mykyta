"""Додані колонки created_at та updated_at у aquariums

Revision ID: 6147866fcfb2
Revises: 48858562b5bf
Create Date: 2024-07-21 19:27:33.193834

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6147866fcfb2'
down_revision: Union[str, None] = '48858562b5bf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('aquariums', sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True))
    op.add_column('aquariums', sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('aquariums', 'updated_at')
    op.drop_column('aquariums', 'created_at')
    # ### end Alembic commands ###
