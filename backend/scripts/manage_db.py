#!/usr/bin/env python
import os
import sys
from pathlib import Path

import click
from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Add the parent directory to the Python path
sys.path.append(str(Path(__file__).parent.parent))

from app.core.config import settings
from app.db.base import Base
from app.db.init_db import init_db, seed_db

@click.group()
def cli():
    """Database management commands."""
    pass

@cli.command()
@click.option('--message', '-m', help='Migration message')
def migrate(message):
    """Create a new migration."""
    alembic_cfg = Config("alembic.ini")
    command.revision(alembic_cfg, message=message, autogenerate=True)

@cli.command()
@click.option('--revision', '-r', default='head', help='Revision to upgrade to')
def upgrade(revision):
    """Upgrade database to a later version."""
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, revision)

@cli.command()
@click.option('--revision', '-r', help='Revision to downgrade to')
def downgrade(revision):
    """Revert database to a previous version."""
    alembic_cfg = Config("alembic.ini")
    command.downgrade(alembic_cfg, revision)

@cli.command()
def history():
    """Show migration history."""
    alembic_cfg = Config("alembic.ini")
    command.history(alembic_cfg)

@cli.command()
def current():
    """Show current database version."""
    alembic_cfg = Config("alembic.ini")
    command.current(alembic_cfg)

@cli.command()
@click.option('--seed/--no-seed', default=True, help='Seed the database')
def init(seed):
    """Initialize the database."""
    engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)
    Base.metadata.create_all(bind=engine)
    
    if seed:
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, 
                                  bind=engine)
        db = SessionLocal()
        try:
            init_db(db)
            seed_db(db)
        finally:
            db.close()
        click.echo("Database initialized and seeded successfully.")
    else:
        click.echo("Database initialized successfully.")

@cli.command()
def seed():
    """Seed the database with initial data."""
    engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    try:
        seed_db(db)
        click.echo("Database seeded successfully.")
    finally:
        db.close()

@cli.command()
@click.confirmation_option(prompt='Are you sure you want to drop all tables?')
def drop_all():
    """Drop all tables in the database."""
    engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)
    Base.metadata.drop_all(bind=engine)
    click.echo("All tables dropped successfully.")

if __name__ == '__main__':
    cli() 