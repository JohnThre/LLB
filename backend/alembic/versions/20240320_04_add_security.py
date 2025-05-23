"""Add security features and validation

Revision ID: 20240320_04_add_security
Revises: 20240320_03_add_analytics
Create Date: 2024-03-20 00:04:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '20240320_04_add_security'
down_revision: str = '20240320_03_add_analytics'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add security-related columns to users table
    op.add_column('users',
        sa.Column('failed_login_attempts', sa.Integer(), nullable=False, 
                 server_default='0')
    )
    op.add_column('users',
        sa.Column('last_failed_login', sa.DateTime(), nullable=True)
    )
    op.add_column('users',
        sa.Column('password_changed_at', sa.DateTime(), nullable=True)
    )
    op.add_column('users',
        sa.Column('email_verified', sa.Boolean(), nullable=False, 
                 server_default='false')
    )
    op.add_column('users',
        sa.Column('email_verification_token', sa.String(), nullable=True)
    )
    op.add_column('users',
        sa.Column('email_verification_sent_at', sa.DateTime(), nullable=True)
    )
    op.add_column('users',
        sa.Column('password_reset_token', sa.String(), nullable=True)
    )
    op.add_column('users',
        sa.Column('password_reset_sent_at', sa.DateTime(), nullable=True)
    )
    op.add_column('users',
        sa.Column('two_factor_enabled', sa.Boolean(), nullable=False, 
                 server_default='false')
    )
    op.add_column('users',
        sa.Column('two_factor_secret', sa.String(), nullable=True)
    )
    
    # Create login_history table
    op.create_table(
        'login_history',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('ip_address', sa.String(), nullable=False),
        sa.Column('user_agent', sa.String(), nullable=True),
        sa.Column('login_at', sa.DateTime(), nullable=False, 
                 server_default=sa.text('now()')),
        sa.Column('success', sa.Boolean(), nullable=False),
        sa.Column('failure_reason', sa.String(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create security_logs table
    op.create_table(
        'security_logs',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('action', sa.String(), nullable=False),
        sa.Column('ip_address', sa.String(), nullable=False),
        sa.Column('user_agent', sa.String(), nullable=True),
        sa.Column('details', postgresql.JSONB(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, 
                 server_default=sa.text('now()')),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create indexes
    op.create_index(op.f('ix_login_history_user_id'), 'login_history', 
                   ['user_id'], unique=False)
    op.create_index(op.f('ix_login_history_login_at'), 'login_history', 
                   ['login_at'], unique=False)
    op.create_index(op.f('ix_security_logs_user_id'), 'security_logs', 
                   ['user_id'], unique=False)
    op.create_index(op.f('ix_security_logs_action'), 'security_logs', 
                   ['action'], unique=False)
    
    # Add constraints
    op.create_check_constraint(
        'failed_login_attempts_non_negative',
        'users',
        'failed_login_attempts >= 0'
    )
    
    # Add triggers for security logging
    op.execute("""
        CREATE OR REPLACE FUNCTION log_login_attempt()
        RETURNS TRIGGER AS $$
        BEGIN
            INSERT INTO login_history (
                user_id, ip_address, user_agent, success, failure_reason
            ) VALUES (
                NEW.id, 
                current_setting('request.headers')::json->>'x-forwarded-for',
                current_setting('request.headers')::json->>'user-agent',
                NEW.failed_login_attempts = 0,
                CASE 
                    WHEN NEW.failed_login_attempts > 0 
                    THEN 'Invalid credentials' 
                    ELSE NULL 
                END
            );
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
    """)
    
    op.execute("""
        CREATE TRIGGER log_login_attempt_trigger
        AFTER UPDATE OF failed_login_attempts ON users
        FOR EACH ROW
        EXECUTE FUNCTION log_login_attempt();
    """)
    
    # Add password policy check
    op.execute("""
        CREATE OR REPLACE FUNCTION check_password_policy()
        RETURNS TRIGGER AS $$
        BEGIN
            IF NEW.hashed_password IS NOT NULL AND (
                LENGTH(NEW.hashed_password) < 8 OR
                NEW.hashed_password !~ '[A-Z]' OR
                NEW.hashed_password !~ '[a-z]' OR
                NEW.hashed_password !~ '[0-9]' OR
                NEW.hashed_password !~ '[^A-Za-z0-9]'
            ) THEN
                RAISE EXCEPTION 'Password does not meet security requirements';
            END IF;
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
    """)
    
    op.execute("""
        CREATE TRIGGER check_password_policy_trigger
        BEFORE INSERT OR UPDATE OF hashed_password ON users
        FOR EACH ROW
        EXECUTE FUNCTION check_password_policy();
    """)


def downgrade() -> None:
    # Drop triggers
    op.execute("DROP TRIGGER IF EXISTS check_password_policy_trigger ON users")
    op.execute("DROP FUNCTION IF EXISTS check_password_policy()")
    op.execute("DROP TRIGGER IF EXISTS log_login_attempt_trigger ON users")
    op.execute("DROP FUNCTION IF EXISTS log_login_attempt()")
    
    # Drop constraints
    op.drop_constraint('failed_login_attempts_non_negative', 'users', 
                      type_='check')
    
    # Drop indexes
    op.drop_index(op.f('ix_security_logs_action'), table_name='security_logs')
    op.drop_index(op.f('ix_security_logs_user_id'), table_name='security_logs')
    op.drop_index(op.f('ix_login_history_login_at'), table_name='login_history')
    op.drop_index(op.f('ix_login_history_user_id'), table_name='login_history')
    
    # Drop tables
    op.drop_table('security_logs')
    op.drop_table('login_history')
    
    # Drop columns from users table
    op.drop_column('users', 'two_factor_secret')
    op.drop_column('users', 'two_factor_enabled')
    op.drop_column('users', 'password_reset_sent_at')
    op.drop_column('users', 'password_reset_token')
    op.drop_column('users', 'email_verification_sent_at')
    op.drop_column('users', 'email_verification_token')
    op.drop_column('users', 'email_verified')
    op.drop_column('users', 'password_changed_at')
    op.drop_column('users', 'last_failed_login')
    op.drop_column('users', 'failed_login_attempts') 