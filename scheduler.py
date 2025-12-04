import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from telegram.ext import Application
import config
from bot import send_morning_reminder, send_afternoon_reminder, send_daily_topic

logger = logging.getLogger(__name__)


class BotScheduler:
    def __init__(self, application: Application):
        self.application = application
        self.scheduler = AsyncIOScheduler(timezone=config.TIMEZONE)

    def setup_jobs(self):
        """Setup scheduled jobs"""
        # Morning reminder
        morning_hour, morning_minute = config.MORNING_REMINDER.hour, config.MORNING_REMINDER.minute
        self.scheduler.add_job(
            self._morning_job,
            CronTrigger(hour=morning_hour, minute=morning_minute, timezone=config.TIMEZONE),
            id='morning_reminder',
            name='Morning Reminder'
        )
        logger.info(f"Scheduled morning reminder at {morning_hour:02d}:{morning_minute:02d}")

        # Afternoon reminder
        afternoon_hour, afternoon_minute = config.AFTERNOON_REMINDER.hour, config.AFTERNOON_REMINDER.minute
        self.scheduler.add_job(
            self._afternoon_job,
            CronTrigger(hour=afternoon_hour, minute=afternoon_minute, timezone=config.TIMEZONE),
            id='afternoon_reminder',
            name='Afternoon Reminder'
        )
        logger.info(f"Scheduled afternoon reminder at {afternoon_hour:02d}:{afternoon_minute:02d}")

        # Daily topic reminder
        topic_hour, topic_minute = config.TOPIC_REMINDER.hour, config.TOPIC_REMINDER.minute
        self.scheduler.add_job(
            self._topic_job,
            CronTrigger(hour=topic_hour, minute=topic_minute, timezone=config.TIMEZONE),
            id='daily_topic',
            name='Daily IELTS Topic'
        )
        logger.info(f"Scheduled daily topic at {topic_hour:02d}:{topic_minute:02d}")

    async def _morning_job(self):
        """Morning reminder job"""
        await send_morning_reminder(self.application)

    async def _afternoon_job(self):
        """Afternoon reminder job"""
        await send_afternoon_reminder(self.application)

    async def _topic_job(self):
        """Daily topic job"""
        await send_daily_topic(self.application)

    def start(self):
        """Start the scheduler"""
        self.scheduler.start()
        logger.info("Scheduler started")

    def shutdown(self):
        """Shutdown the scheduler"""
        try:
            if self.scheduler.running:
                self.scheduler.shutdown(wait=False)
                logger.info("Scheduler stopped")
        except RuntimeError as e:
            # Event loop might be closed already, which is fine during shutdown
            logger.debug(f"Scheduler shutdown: {e}")
