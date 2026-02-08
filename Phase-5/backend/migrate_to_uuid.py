"""
Migrate conversations.id from INTEGER to VARCHAR(255) UUID
"""
import asyncio
import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text

# Load environment variables
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

# Convert to async psycopg URL
if DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg://", 1)

async def migrate():
    engine = create_async_engine(DATABASE_URL, echo=True)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with async_session() as session:
        try:
            print("Starting migration: INTEGER id -> VARCHAR(255) UUID")

            # Step 1: Drop foreign key constraints
            print("\n[1/5] Dropping foreign key constraints...")
            await session.execute(text("""
                ALTER TABLE messages
                DROP CONSTRAINT IF EXISTS messages_conversation_id_fkey;
            """))
            await session.commit()

            # Step 2: Drop existing conversations and messages (we'll recreate)
            print("\n[2/5] Dropping existing data...")
            await session.execute(text("DROP TABLE IF EXISTS messages CASCADE;"))
            await session.execute(text("DROP TABLE IF EXISTS conversations CASCADE;"))
            await session.commit()

            # Step 3: Recreate conversations table with VARCHAR id
            print("\n[3/5] Creating conversations table with VARCHAR id...")
            await session.execute(text("""
                CREATE TABLE conversations (
                    id VARCHAR(255) PRIMARY KEY,
                    user_id VARCHAR(255) NOT NULL REFERENCES users(id),
                    title VARCHAR(255),
                    is_active BOOLEAN NOT NULL DEFAULT TRUE,
                    created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL,
                    updated_at TIMESTAMP WITHOUT TIME ZONE NOT NULL
                );
            """))
            await session.execute(text("""
                CREATE INDEX ix_conversations_user_id ON conversations(user_id);
            """))
            await session.execute(text("""
                CREATE INDEX ix_conversations_is_active ON conversations(is_active);
            """))
            await session.execute(text("""
                CREATE INDEX ix_conversations_updated_at ON conversations(updated_at);
            """))
            await session.commit()

            # Step 4: Recreate messages table with VARCHAR conversation_id
            print("\n[4/5] Creating messages table with VARCHAR conversation_id...")
            await session.execute(text("""
                CREATE TABLE messages (
                    id SERIAL PRIMARY KEY,
                    conversation_id VARCHAR(255) NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
                    role VARCHAR(50) NOT NULL,
                    content TEXT NOT NULL,
                    tool_calls JSONB,
                    created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL
                );
            """))
            await session.execute(text("""
                CREATE INDEX ix_messages_conversation_id ON messages(conversation_id);
            """))
            await session.execute(text("""
                CREATE INDEX ix_messages_created_at ON messages(created_at);
            """))
            await session.commit()

            print("\n[5/5] Migration complete!")
            print("✅ Conversations and messages tables now use UUID VARCHAR(255) ids")

        except Exception as e:
            print(f"\n❌ Migration failed: {e}")
            await session.rollback()
            raise
        finally:
            await engine.dispose()

if __name__ == "__main__":
    asyncio.run(migrate())
