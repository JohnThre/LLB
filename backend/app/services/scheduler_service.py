"""
Scheduler Service for automated knowledge updates
"""

import asyncio
from datetime import datetime, timedelta
from typing import Dict, Any
from app.core.logging import get_logger
from app.services.knowledge_service import KnowledgeService

logger = get_logger(__name__)


class SchedulerService:
    """Service for scheduling automated knowledge updates."""

    def __init__(self):
        self.knowledge_service = KnowledgeService()
        self.is_running = False
        self.update_interval = timedelta(hours=24)  # Daily updates
        self.last_update = None

    async def start_scheduler(self):
        """Start the automated scheduler."""
        if self.is_running:
            logger.warning("Scheduler already running")
            return

        self.is_running = True
        logger.info("Starting knowledge update scheduler")
        
        # Run initial update
        await self._run_scheduled_update()
        
        # Schedule regular updates
        while self.is_running:
            try:
                await asyncio.sleep(3600)  # Check every hour
                
                if self._should_update():
                    await self._run_scheduled_update()
                    
            except Exception as e:
                logger.error(f"Scheduler error: {e}")
                await asyncio.sleep(300)  # Wait 5 minutes on error

    async def stop_scheduler(self):
        """Stop the automated scheduler."""
        self.is_running = False
        logger.info("Knowledge update scheduler stopped")

    def _should_update(self) -> bool:
        """Check if an update should be performed."""
        if not self.last_update:
            return True
            
        return datetime.utcnow() - self.last_update >= self.update_interval

    async def _run_scheduled_update(self):
        """Run a scheduled knowledge update."""
        try:
            logger.info("Running scheduled knowledge update")
            result = await self.knowledge_service.search_and_update_knowledge()
            self.last_update = datetime.utcnow()
            logger.info(f"Scheduled update completed: {result}")
            
        except Exception as e:
            logger.error(f"Scheduled update failed: {e}")

    async def trigger_manual_update(self, query: str = None) -> Dict[str, Any]:
        """Trigger a manual knowledge update."""
        try:
            logger.info(f"Triggering manual update with query: {query}")
            result = await self.knowledge_service.search_and_update_knowledge(query)
            return result
            
        except Exception as e:
            logger.error(f"Manual update failed: {e}")
            raise

    def get_status(self) -> Dict[str, Any]:
        """Get scheduler status."""
        return {
            'is_running': self.is_running,
            'last_update': self.last_update.isoformat() if self.last_update else None,
            'next_update': (self.last_update + self.update_interval).isoformat() if self.last_update else None,
            'update_interval_hours': self.update_interval.total_seconds() / 3600
        }