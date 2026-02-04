"""Add conversations and messages tables

Revision ID: 002
Revises: 001
Create Date: 2026-01-15

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB


# revision identifiers, used by Alembic.
revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create conversations table
    op.create_table(
        'conversations',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.String(length=255), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    )
    op.create_index('idx_conversations_user_id', 'conversations', ['user_id'])
    op.create_index('idx_conversations_updated_at', 'conversations', ['updated_at'])
    op.create_index('idx_conversations_is_active', 'conversations', ['is_active'])

    # Create messages table
    op.create_table(
        'messages',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('conversation_id', sa.Integer(), nullable=False),
        sa.Column('role', sa.String(length=50), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('tool_calls', JSONB, nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['conversation_id'], ['conversations.id'], ondelete='CASCADE'),
    )
    op.create_index('idx_messages_conversation_id', 'messages', ['conversation_id'])
    op.create_index('idx_messages_created_at', 'messages', ['created_at'])

    # Create tool_executions table
    op.create_table(
        'tool_executions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('message_id', sa.Integer(), nullable=False),
        sa.Column('conversation_id', sa.Integer(), nullable=False),
        sa.Column('tool_name', sa.String(length=100), nullable=False),
        sa.Column('parameters', JSONB, nullable=False),
        sa.Column('result', JSONB, nullable=True),
        sa.Column('status', sa.String(length=50), nullable=False, server_default='pending'),
        sa.Column('error_message', sa.String(length=1000), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('completed_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['message_id'], ['messages.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['conversation_id'], ['conversations.id'], ondelete='CASCADE'),
    )
    op.create_index('idx_tool_executions_message_id', 'tool_executions', ['message_id'])
    op.create_index('idx_tool_executions_conversation_id', 'tool_executions', ['conversation_id'])
    op.create_index('idx_tool_executions_status', 'tool_executions', ['status'])


def downgrade() -> None:
    op.drop_table('tool_executions')
    op.drop_table('messages')
    op.drop_table('conversations')
