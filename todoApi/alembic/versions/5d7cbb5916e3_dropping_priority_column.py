"""dropping priority column

Revision ID: 5d7cbb5916e3
Revises: 
Create Date: 2024-09-25 19:50:22.828467

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5d7cbb5916e3'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_column('todos', 'priority')


def downgrade() -> None:
    pass
