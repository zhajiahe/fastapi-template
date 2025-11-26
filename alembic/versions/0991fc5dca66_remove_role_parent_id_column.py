"""remove role parent_id column

Revision ID: 0991fc5dca66
Revises: 9aad798d4ed2
Create Date: 2025-11-26 16:44:08.422831

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0991fc5dca66'
down_revision: Union[str, Sequence[str], None] = '9aad798d4ed2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # SQLite 不支持直接删除列，需要使用 batch_alter_table
    with op.batch_alter_table('roles') as batch_op:
        batch_op.drop_column('parent_id')


def downgrade() -> None:
    """Downgrade schema."""
    with op.batch_alter_table('roles') as batch_op:
        batch_op.add_column(sa.Column('parent_id', sa.INTEGER(), nullable=True))
        batch_op.create_foreign_key('fk_roles_parent_id', 'roles', ['parent_id'], ['id'], ondelete='SET NULL')
