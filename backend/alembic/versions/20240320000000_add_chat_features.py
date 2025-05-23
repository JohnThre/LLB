"""Add chat features

Revision ID: 20240320000000
Revises: 20240319000000
Create Date: 2024-03-20 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '20240320000000'
down_revision = '20240319000000'
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Add is_archived and is_pinned columns to chats table
    op.add_column('chats', sa.Column('is_archived', sa.Boolean(), 
                  nullable=False, server_default='false'))
    op.add_column('chats', sa.Column('is_pinned', sa.Boolean(), 
                  nullable=False, server_default='false'))
    
    # Add pinned_at column to chats table
    op.add_column('chats', sa.Column('pinned_at', sa.DateTime(), 
                  nullable=True))
    
    # Add index for pinned chats
    op.create_index('ix_chats_is_pinned', 'chats', ['is_pinned'])
    
    # Add index for archived chats
    op.create_index('ix_chats_is_archived', 'chats', ['is_archived'])

def downgrade() -> None:
    # Drop indexes
    op.drop_index('ix_chats_is_archived')
    op.drop_index('ix_chats_is_pinned')
    
    # Drop columns
    op.drop_column('chats', 'pinned_at')
    op.drop_column('chats', 'is_pinned')
    op.drop_column('chats', 'is_archived') 