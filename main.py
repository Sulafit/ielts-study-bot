#!/usr/bin/env python3
"""
IELTS Study Buddy Bot - Main Entry Point
"""

import logging
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters
)
import config
from database import db
from scheduler import BotScheduler
from bot import (
    start_command,
    today_command,
    topic_command,
    all_command,
    stats_command,
    help_command,
    button_handler
)

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


async def log_chat_id(update: Update, context):
    """Log chat ID to help users configure GROUP_CHAT_ID"""
    if update.effective_chat:
        chat = update.effective_chat
        logger.info(f"Message received from chat_id={chat.id}, type={chat.type}, title={chat.title or 'N/A'}")


def main():
    """Main function to run the bot with scheduler"""
    if not config.BOT_TOKEN:
        logger.error("BOT_TOKEN not set in environment variables!")
        logger.error("Please copy .env.example to .env and configure it")
        return

    logger.info("Starting IELTS Study Buddy Bot...")
    logger.info(f"Bot username: @checklist_IELTS_account_bot")
    logger.info(f"Morning reminder: {config.MORNING_TIME}")
    logger.info(f"Afternoon reminder: {config.AFTERNOON_TIME}")
    logger.info(f"Daily topic: {config.TOPIC_TIME}")

    if config.GROUP_CHAT_ID:
        logger.info(f"Group chat configured: {config.GROUP_CHAT_ID}")
    else:
        logger.info("No group chat configured - reminders disabled")
        logger.info("To enable group reminders:")
        logger.info("1. Add bot to your group")
        logger.info("2. Send /start in the group")
        logger.info("3. Check logs for 'chat_id=' and copy the ID to .env")

    # Create application
    application = Application.builder().token(config.BOT_TOKEN).build()

    # Add command handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("today", today_command))
    application.add_handler(CommandHandler("topic", topic_command))
    application.add_handler(CommandHandler("all", all_command))
    application.add_handler(CommandHandler("stats", stats_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CallbackQueryHandler(button_handler))

    # Add message handler to log chat IDs (helpful for setup)
    application.add_handler(MessageHandler(filters.ALL, log_chat_id), group=1)

    # Setup and start scheduler
    scheduler = BotScheduler(application)
    scheduler.setup_jobs()
    scheduler.start()

    # Start the bot
    logger.info("Bot is running. Press Ctrl+C to stop.")

    try:
        application.run_polling(allowed_updates=Update.ALL_TYPES)
    except KeyboardInterrupt:
        logger.info("Stopping bot...")
    finally:
        scheduler.shutdown()
        logger.info("Bot stopped")


if __name__ == '__main__':
    main()
