"""Add params field to chat table

Revision ID: add_chat_params_field
Revises: 1af9b942657b
Create Date: 2024-01-01 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'add_chat_params_field'
down_revision = '1af9b942657b'
branch_labels = None
depends_on = None


def upgrade():
    # Добавляем поле params в таблицу chat
    op.add_column('chat', sa.Column('params', sa.JSON(), server_default='{}', nullable=True))


def downgrade():
    # Удаляем поле params из таблицы chat
    op.drop_column('chat', 'params')
