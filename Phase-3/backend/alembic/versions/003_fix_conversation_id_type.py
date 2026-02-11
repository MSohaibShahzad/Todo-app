"""Fix conversation id type from integer to string

Revision ID: 003
Revises: 002
Create Date: 2026-02-11

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '003'
down_revision = '002'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Drop foreign key constraints that reference conversations.id
    op.drop_constraint('messages_conversation_id_fkey', 'messages', type_='foreignkey')
    op.drop_constraint('tool_executions_conversation_id_fkey', 'tool_executions', type_='foreignkey')
    op.drop_constraint('tool_executions_message_id_fkey', 'tool_executions', type_='foreignkey')

    # Drop primary key constraint on conversations
    op.drop_constraint('conversations_pkey', 'conversations', type_='primary')

    # Change conversations.id from INTEGER to VARCHAR(255)
    op.alter_column('conversations', 'id',
                    existing_type=sa.INTEGER(),
                    type_=sa.String(length=255),
                    existing_nullable=False,
                    postgresql_using='id::text')

    # Change messages.conversation_id from INTEGER to VARCHAR(255)
    op.alter_column('messages', 'conversation_id',
                    existing_type=sa.INTEGER(),
                    type_=sa.String(length=255),
                    existing_nullable=False,
                    postgresql_using='conversation_id::text')

    # Change tool_executions.conversation_id from INTEGER to VARCHAR(255)
    op.alter_column('tool_executions', 'conversation_id',
                    existing_type=sa.INTEGER(),
                    type_=sa.String(length=255),
                    existing_nullable=False,
                    postgresql_using='conversation_id::text')

    # Re-add primary key constraint
    op.create_primary_key('conversations_pkey', 'conversations', ['id'])

    # Re-add foreign key constraints
    op.create_foreign_key('messages_conversation_id_fkey', 'messages', 'conversations', ['conversation_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key('tool_executions_conversation_id_fkey', 'tool_executions', 'conversations', ['conversation_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key('tool_executions_message_id_fkey', 'tool_executions', 'messages', ['message_id'], ['id'], ondelete='CASCADE')


def downgrade() -> None:
    # Drop foreign key constraints
    op.drop_constraint('messages_conversation_id_fkey', 'messages', type_='foreignkey')
    op.drop_constraint('tool_executions_conversation_id_fkey', 'tool_executions', type_='foreignkey')
    op.drop_constraint('tool_executions_message_id_fkey', 'tool_executions', type_='foreignkey')

    # Drop primary key
    op.drop_constraint('conversations_pkey', 'conversations', type_='primary')

    # Change back to INTEGER
    op.alter_column('conversations', 'id',
                    existing_type=sa.String(length=255),
                    type_=sa.INTEGER(),
                    existing_nullable=False,
                    postgresql_using='id::integer')

    op.alter_column('messages', 'conversation_id',
                    existing_type=sa.String(length=255),
                    type_=sa.INTEGER(),
                    existing_nullable=False,
                    postgresql_using='conversation_id::integer')

    op.alter_column('tool_executions', 'conversation_id',
                    existing_type=sa.String(length=255),
                    type_=sa.INTEGER(),
                    existing_nullable=False,
                    postgresql_using='conversation_id::integer')

    # Re-add constraints
    op.create_primary_key('conversations_pkey', 'conversations', ['id'])
    op.create_foreign_key('messages_conversation_id_fkey', 'messages', 'conversations', ['conversation_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key('tool_executions_conversation_id_fkey', 'tool_executions', 'conversations', ['conversation_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key('tool_executions_message_id_fkey', 'tool_executions', 'messages', ['message_id'], ['id'], ondelete='CASCADE')
