"""
Database initialization script.
"""

import logging
from sqlalchemy.orm import Session
from app.core.config import settings
from app.db.base import Base
from app.db.session import engine
from app.models.user import User
from app.core.security import get_password_hash

logger = logging.getLogger(__name__)


def init_db(db: Session) -> None:
    """Initialize the database with initial data."""
    try:
        # Create tables
        Base.metadata.create_all(bind=engine)
        
        # Create initial admin user if not exists
        admin = db.query(User).filter(User.email == "admin@llb.local").first()
        if not admin:
            admin_user = User(
                email="admin@llb.local",
                name="Admin User",
                hashed_password=get_password_hash("admin123"),  # Change in production
                role="admin",
                is_active=True
            )
            db.add(admin_user)
            db.commit()
            logger.info("Created initial admin user")
        
        logger.info("Database initialization completed successfully")
        
    except Exception as e:
        logger.error(f"Error initializing database: {str(e)}")
        raise


def reset_db(db: Session) -> None:
    """Reset the database (drop and recreate all tables)."""
    try:
        # Drop all tables
        Base.metadata.drop_all(bind=engine)
        
        # Recreate tables
        Base.metadata.create_all(bind=engine)
        
        # Initialize with initial data
        init_db(db)
        
        logger.info("Database reset completed successfully")
        
    except Exception as e:
        logger.error(f"Error resetting database: {str(e)}")
        raise 