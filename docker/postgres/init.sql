-- LLB Database Initialization Script
-- This script sets up the initial database schema and data

-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- Create database user if not exists (for development)
DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'llb_user') THEN
        CREATE ROLE llb_user WITH LOGIN PASSWORD 'llb_password';
    END IF;
END
$$;

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE llb_db TO llb_user;
GRANT ALL PRIVILEGES ON DATABASE llb_db_dev TO llb_user;

-- Create schemas
CREATE SCHEMA IF NOT EXISTS llb_app;
CREATE SCHEMA IF NOT EXISTS llb_ai;

-- Grant schema privileges
GRANT ALL ON SCHEMA llb_app TO llb_user;
GRANT ALL ON SCHEMA llb_ai TO llb_user;

-- Set default privileges for future tables
ALTER DEFAULT PRIVILEGES IN SCHEMA llb_app GRANT ALL ON TABLES TO llb_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA llb_ai GRANT ALL ON TABLES TO llb_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA llb_app GRANT ALL ON SEQUENCES TO llb_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA llb_ai GRANT ALL ON SEQUENCES TO llb_user;

-- Create initial tables (these will be managed by Alembic migrations)
-- This is just for reference and initial setup

-- Users table
CREATE TABLE IF NOT EXISTS llb_app.users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    is_superuser BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Chat sessions table
CREATE TABLE IF NOT EXISTS llb_app.chat_sessions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES llb_app.users(id) ON DELETE CASCADE,
    title VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Chat messages table
CREATE TABLE IF NOT EXISTS llb_app.chat_messages (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    session_id UUID REFERENCES llb_app.chat_sessions(id) ON DELETE CASCADE,
    role VARCHAR(20) NOT NULL CHECK (role IN ('user', 'assistant', 'system')),
    content TEXT NOT NULL,
    metadata JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- AI models table
CREATE TABLE IF NOT EXISTS llb_ai.models (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) NOT NULL,
    version VARCHAR(50) NOT NULL,
    model_type VARCHAR(50) NOT NULL,
    file_path VARCHAR(500),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(name, version)
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_users_email ON llb_app.users(email);
CREATE INDEX IF NOT EXISTS idx_users_username ON llb_app.users(username);
CREATE INDEX IF NOT EXISTS idx_chat_sessions_user_id ON llb_app.chat_sessions(user_id);
CREATE INDEX IF NOT EXISTS idx_chat_messages_session_id ON llb_app.chat_messages(session_id);
CREATE INDEX IF NOT EXISTS idx_chat_messages_created_at ON llb_app.chat_messages(created_at);
CREATE INDEX IF NOT EXISTS idx_models_name_version ON llb_ai.models(name, version);

-- Insert initial AI models data
INSERT INTO llb_ai.models (name, version, model_type, file_path, is_active) 
VALUES 
    ('gemma-3-1b', '1.0', 'text_generation', '/app/models/gemma-3-1b', TRUE),
    ('whisper-base', '1.0', 'speech_recognition', '/app/models/whisper', TRUE)
ON CONFLICT (name, version) DO NOTHING;

-- Create a function to update the updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create triggers for updated_at
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON llb_app.users 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_chat_sessions_updated_at BEFORE UPDATE ON llb_app.chat_sessions 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Create a demo user for testing (password: demo123)
INSERT INTO llb_app.users (username, email, hashed_password, is_active) 
VALUES (
    'demo', 
    'demo@llb.local', 
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj3QJflLxQxe', 
    TRUE
) ON CONFLICT (email) DO NOTHING; 