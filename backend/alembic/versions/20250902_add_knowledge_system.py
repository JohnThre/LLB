"""Add knowledge system

Revision ID: 20250902_add_knowledge_system
Revises: 20240320_04_add_security
Create Date: 2025-09-02 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '20250902_add_knowledge_system'
down_revision: Union[str, None] = '20240320_04_add_security'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create knowledge_entries table
    op.create_table(
        'knowledge_entries',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(500), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('summary', sa.Text(), nullable=True),
        sa.Column('category', sa.String(100), nullable=False),
        sa.Column('language', sa.String(10), nullable=False, default='en'),
        sa.Column('source_url', sa.String(1000), nullable=True),
        sa.Column('source_type', sa.String(50), nullable=False, default='ai_generated'),
        sa.Column('keywords', postgresql.ARRAY(sa.String()), nullable=True),
        sa.Column('quality_score', sa.Float(), nullable=False, default=0.0),
        sa.Column('is_verified', sa.Boolean(), nullable=False, default=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, default=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, 
                 server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, 
                 server_default=sa.text('now()')),
        sa.PrimaryKeyConstraint('id')
    )

    # Create knowledge_updates table for tracking update history
    op.create_table(
        'knowledge_updates',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('update_type', sa.String(50), nullable=False),
        sa.Column('entries_added', sa.Integer(), nullable=False, default=0),
        sa.Column('entries_updated', sa.Integer(), nullable=False, default=0),
        sa.Column('search_query', sa.String(500), nullable=True),
        sa.Column('status', sa.String(20), nullable=False, default='pending'),
        sa.Column('error_message', sa.Text(), nullable=True),
        sa.Column('started_at', sa.DateTime(), nullable=False, 
                 server_default=sa.text('now()')),
        sa.Column('completed_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    # Create indexes
    op.create_index('ix_knowledge_entries_category', 'knowledge_entries', ['category'])
    op.create_index('ix_knowledge_entries_language', 'knowledge_entries', ['language'])
    op.create_index('ix_knowledge_entries_is_active', 'knowledge_entries', ['is_active'])
    op.create_index('ix_knowledge_updates_status', 'knowledge_updates', ['status'])


def downgrade() -> None:
    # Drop indexes
    op.drop_index('ix_knowledge_updates_status')
    op.drop_index('ix_knowledge_entries_is_active')
    op.drop_index('ix_knowledge_entries_language')
    op.drop_index('ix_knowledge_entries_category')
    
    # Drop tables
    op.drop_table('knowledge_updates')
    op.drop_table('knowledge_entries')