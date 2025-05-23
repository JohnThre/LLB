"""Add user roles and permissions

Revision ID: 20240320_02_add_roles
Revises: 20240320_initial
Create Date: 2024-03-20 00:02:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '20240320_02_add_roles'
down_revision: str = '20240320_initial'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create roles enum type
    op.execute("CREATE TYPE user_role AS ENUM ('admin', 'moderator', 'user')")
    
    # Add role column to users table
    op.add_column('users',
        sa.Column('role', sa.Enum('admin', 'moderator', 'user', 
                                name='user_role'),
                 nullable=False, server_default='user')
    )
    
    # Create permissions table
    op.create_table(
        'permissions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, 
                 server_default=sa.text('now()')),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )
    
    # Create role_permissions table
    op.create_table(
        'role_permissions',
        sa.Column('role', sa.Enum('admin', 'moderator', 'user', 
                                name='user_role'), nullable=False),
        sa.Column('permission_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, 
                 server_default=sa.text('now()')),
        sa.ForeignKeyConstraint(['permission_id'], ['permissions.id'], ),
        sa.PrimaryKeyConstraint('role', 'permission_id')
    )
    
    # Insert default permissions
    op.bulk_insert(
        sa.table('permissions',
            sa.column('name', sa.String),
            sa.column('description', sa.String)
        ),
        [
            {'name': 'manage_users', 'description': 'Manage user accounts'},
            {'name': 'manage_chats', 'description': 'Manage chat rooms'},
            {'name': 'manage_messages', 'description': 'Manage messages'},
            {'name': 'view_analytics', 'description': 'View analytics'},
            {'name': 'manage_settings', 'description': 'Manage system settings'}
        ]
    )
    
    # Insert default role permissions
    op.bulk_insert(
        sa.table('role_permissions',
            sa.column('role', sa.Enum('admin', 'moderator', 'user', 
                                    name='user_role')),
            sa.column('permission_id', sa.Integer)
        ),
        [
            # Admin permissions
            {'role': 'admin', 'permission_id': 1},
            {'role': 'admin', 'permission_id': 2},
            {'role': 'admin', 'permission_id': 3},
            {'role': 'admin', 'permission_id': 4},
            {'role': 'admin', 'permission_id': 5},
            # Moderator permissions
            {'role': 'moderator', 'permission_id': 2},
            {'role': 'moderator', 'permission_id': 3},
            {'role': 'moderator', 'permission_id': 4},
            # User permissions
            {'role': 'user', 'permission_id': 2},
            {'role': 'user', 'permission_id': 3}
        ]
    )


def downgrade() -> None:
    # Drop role_permissions table
    op.drop_table('role_permissions')
    
    # Drop permissions table
    op.drop_table('permissions')
    
    # Drop role column from users table
    op.drop_column('users', 'role')
    
    # Drop user_role enum type
    op.execute('DROP TYPE user_role') 