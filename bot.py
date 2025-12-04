import logging
from datetime import datetime, date
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes
)
import config
from database import db
from ielts_topics import get_current_topic, get_current_day_number, format_topic_message

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


def ensure_user_registered(user):
    """Ensure user is registered in database"""
    if user:
        db.add_user(
            user_id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            username=user.username
        )


def get_user_name(user_id: int) -> str:
    """Get user name by ID from database"""
    return db.get_user_name(user_id)


def get_writing_task() -> str:
    """Get today's writing task based on schedule"""
    today = date.today()
    weekday = today.weekday()
    task = config.WRITING_SCHEDULE.get(weekday)

    if task:
        return f"✍️ Writing ({task})"
    return "✍️ Writing (Отдых)"


def create_task_keyboard_dual() -> InlineKeyboardMarkup:
    """Create inline keyboard with two columns - one for each user"""
    keyboard = []
    all_users = db.get_all_users()

    # If less than 2 users, show single column
    if len(all_users) < 2:
        user_id = list(all_users.keys())[0] if all_users else 0
        return create_task_keyboard_single(user_id)

    # Get two users (Shakhnaz and Sultan)
    user_ids = list(all_users.keys())[:2]
    user1_id, user2_id = user_ids[0], user_ids[1]

    user1_status = db.get_today_status(user1_id)
    user2_status = db.get_today_status(user2_id)

    user1_name = get_user_name(user1_id)
    user2_name = get_user_name(user2_id)

    # Get short names (first name only)
    user1_short = user1_name.split()[0]
    user2_short = user2_name.split()[0]

    # All tasks (morning + afternoon)
    all_tasks = list(config.MORNING_TASKS) + list(config.AFTERNOON_TASKS)

    # Create two column layout
    for task_id, task_name in all_tasks:
        # Adjust writing task name
        if task_id == 'writing':
            task_name = get_writing_task()

        # Get status for both users
        status1 = "✅" if user1_status.get(task_id, False) else "☐"
        status2 = "✅" if user2_status.get(task_id, False) else "☐"

        # Create two buttons side by side
        button1 = InlineKeyboardButton(
            f"{status1} {user1_short}",
            callback_data=f"toggle_{user1_id}_{task_id}"
        )
        button2 = InlineKeyboardButton(
            f"{status2} {user2_short}",
            callback_data=f"toggle_{user2_id}_{task_id}"
        )

        # Add task name as label row
        keyboard.append([
            InlineKeyboardButton(task_name, callback_data=f"task_label_{task_id}")
        ])
        # Add user buttons row
        keyboard.append([button1, button2])

    return InlineKeyboardMarkup(keyboard)


def create_task_keyboard_single(user_id: int) -> InlineKeyboardMarkup:
    """Create inline keyboard with all daily tasks for a specific user"""
    keyboard = []
    user_status = db.get_today_status(user_id)

    # Morning tasks
    for task_id, task_name in config.MORNING_TASKS:
        status = "✅" if user_status.get(task_id, False) else "☐"
        button_text = f"{status} {task_name}"
        keyboard.append([InlineKeyboardButton(button_text, callback_data=f"toggle_{user_id}_{task_id}")])

    # Afternoon tasks
    for task_id, task_name in config.AFTERNOON_TASKS:
        if task_id == 'writing':
            task_name = get_writing_task()

        status = "✅" if user_status.get(task_id, False) else "☐"
        button_text = f"{status} {task_name}"
        keyboard.append([InlineKeyboardButton(button_text, callback_data=f"toggle_{user_id}_{task_id}")])

    # Show all users progress button
    keyboard.append([InlineKeyboardButton("👥 Прогресс всех", callback_data="show_all")])

    return InlineKeyboardMarkup(keyboard)


def format_dual_progress_message() -> str:
    """Format progress message for both users"""
    today = date.today()
    all_users = db.get_all_users()

    # Check if Saturday or Sunday
    is_saturday = today.weekday() == 5
    is_sunday = today.weekday() == 6

    special_day = ""
    if is_saturday:
        special_day = "\n🎯 **MOCK TEST DAY!**"
    elif is_sunday:
        special_day = "\n😌 **ЛЁГКИЙ РЕЖИМ**"

    if len(all_users) < 2:
        # Single user mode
        if all_users:
            user_id = list(all_users.keys())[0]
            return format_user_progress_message(user_id)
        return "📅 Начните использовать бота!"

    # Get two users
    user_ids = list(all_users.keys())[:2]
    user1_id, user2_id = user_ids[0], user_ids[1]

    user1_name = get_user_name(user1_id)
    user2_name = get_user_name(user2_id)

    user1_status = db.get_today_status(user1_id)
    user2_status = db.get_today_status(user2_id)

    all_tasks = config.MORNING_TASKS + config.AFTERNOON_TASKS
    total = len(all_tasks)

    completed1 = sum(1 for task_id, _ in all_tasks if user1_status.get(task_id, False))
    completed2 = sum(1 for task_id, _ in all_tasks if user2_status.get(task_id, False))

    streak1, best1 = db.get_streak(user1_id)
    streak2, best2 = db.get_streak(user2_id)

    message = f"""
📅 **{today.strftime('%d.%m.%Y')}**{special_day}
─────────────────

**{user1_name}**: {completed1}/{total} задач | 🔥 {streak1} дней
**{user2_name}**: {completed2}/{total} задач | 🔥 {streak2} дней

Нажимайте на кнопки, чтобы отметить задачи:
"""

    return message


def format_user_progress_message(user_id: int) -> str:
    """Format progress message for a single user"""
    today = date.today()
    user_status = db.get_today_status(user_id)
    user_name = get_user_name(user_id)

    all_tasks = config.MORNING_TASKS + config.AFTERNOON_TASKS
    completed = sum(1 for task_id, _ in all_tasks if user_status.get(task_id, False))
    total = len(all_tasks)

    current_streak, best_streak = db.get_streak(user_id)

    # Check if Saturday or Sunday
    is_saturday = today.weekday() == 5
    is_sunday = today.weekday() == 6

    special_day = ""
    if is_saturday:
        special_day = "\n🎯 **MOCK TEST DAY!**"
    elif is_sunday:
        special_day = "\n😌 **ЛЁГКИЙ РЕЖИМ**"

    message = f"""
📅 **{today.strftime('%d.%m.%Y')} - {user_name}**{special_day}
─────────────────
Выполнено: {completed}/{total} задач
🔥 Streak: {current_streak} дней (Лучший: {best_streak})

Нажимайте на кнопки ниже, чтобы отметить задачи:
"""

    return message


def format_all_users_summary() -> str:
    """Format summary of all users' progress"""
    today = date.today()
    all_users = db.get_all_users()

    if not all_users:
        return "📊 Пока никто не начал работу с ботом"

    summary = f"📊 **Общий прогресс - {today.strftime('%d.%m.%Y')}**\n\n"

    all_tasks = config.MORNING_TASKS + config.AFTERNOON_TASKS
    total_tasks = len(all_tasks)

    for user_id, user_name in all_users.items():
        user_status = db.get_today_status(user_id)
        completed = sum(1 for task_id, _ in all_tasks if user_status.get(task_id, False))
        current_streak, _ = db.get_streak(user_id)

        # Progress bar
        progress = "█" * completed + "░" * (total_tasks - completed)

        summary += f"**{user_name}**\n"
        summary += f"├ {progress} {completed}/{total_tasks}\n"
        summary += f"└ 🔥 {current_streak} дней\n\n"

    return summary


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    user = update.effective_user
    ensure_user_registered(user)

    welcome_text = f"""
👋 Привет, {user.first_name}!

Я буду помогать отслеживать ваш прогресс в подготовке к IELTS.

📅 **Расписание напоминаний:**
• {config.MORNING_TIME} - Утренний чек-лист (Reading + Listening)
• {config.TOPIC_TIME} - Топик дня (IELTS Vocabulary)
• {config.AFTERNOON_TIME} - Дневной чек-лист (Writing + Speaking + Review)

**Расписание Writing:**
• Пн, Ср, Пт - Task 2
• Вт, Чт, Сб - Task 1
• Вс - отдых

📚 **30-Day Vocabulary Plan:**
Каждый день бот присылает новый топик с vocabulary для IELTS!

🔥 **Команды:**
/today - Текущий прогресс
/topic - Топик дня
/stats - Статистика и streak
/all - Прогресс всех участников
/help - Помощь

{"**💡 Добавьте меня в групповой чат** с вашими study buddies!" if not config.GROUP_CHAT_ID else ""}

Удачи! 🎯
"""

    await update.message.reply_text(welcome_text, parse_mode='Markdown')


async def today_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show today's progress"""
    user = update.effective_user
    ensure_user_registered(user)

    # Use dual column keyboard for both users
    message_text = format_dual_progress_message()
    keyboard = create_task_keyboard_dual()

    await update.message.reply_text(
        text=message_text,
        reply_markup=keyboard,
        parse_mode='Markdown'
    )


async def all_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show all users' progress"""
    summary = format_all_users_summary()
    await update.message.reply_text(summary, parse_mode='Markdown')


async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show user statistics"""
    user = update.effective_user
    ensure_user_registered(user)
    user_id = user.id

    current_streak, best_streak = db.get_streak(user_id)
    week_stats = db.get_week_stats(user_id)
    today_status = db.get_today_status(user_id)

    # Count completed tasks today
    all_tasks = config.MORNING_TASKS + config.AFTERNOON_TASKS
    completed_today = sum(1 for completed in today_status.values() if completed)
    total_tasks = len(all_tasks)

    stats_text = f"""
📊 **Статистика - {user.first_name}**

🔥 Текущий streak: **{current_streak} дней**
🏆 Лучший streak: **{best_streak} дней**

📅 **Сегодня:** {completed_today}/{total_tasks} задач выполнено

📈 **За неделю:**
"""

    for task_name, count in week_stats.items():
        task_emoji = {
            'reading': '📖',
            'listening': '🎧',
            'writing': '✍️',
            'speaking': '🗣',
            'error_review': '📝',
            'vocabulary': '📚',
            'articles': '📝'
        }.get(task_name, '•')
        stats_text += f"{task_emoji} {task_name.title()}: {count}/7\n"

    await update.message.reply_text(stats_text, parse_mode='Markdown')


async def topic_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show today's IELTS vocabulary topic"""
    user = update.effective_user
    ensure_user_registered(user)

    try:
        # Get today's topic
        day_number = get_current_day_number(config.TOPICS_START_DATE)
        topic = get_current_topic(config.TOPICS_START_DATE)
        message = format_topic_message(topic, day_number)

        await update.message.reply_text(message, parse_mode='Markdown')
    except Exception as e:
        logger.error(f"Error showing topic: {e}")
        await update.message.reply_text("Ошибка при получении топика. Попробуйте позже.")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show help message"""
    help_text = """
📖 **Помощь**

**Команды:**
/start - Начать работу с ботом
/today - Показать сегодняшний чек-лист
/topic - Показать топик дня (30-day vocabulary plan)
/stats - Показать статистику и streak
/all - Показать прогресс всех участников
/help - Эта справка

**Как пользоваться:**
1. Бот присылает напоминания утром и днем (в группу или личные сообщения)
2. Используйте /today чтобы увидеть свой чек-лист
3. Нажимайте на кнопки, чтобы отметить выполненные задачи
4. Используйте /all чтобы увидеть прогресс всех
5. Используйте /topic чтобы увидеть топик дня для изучения vocabulary
6. Поддерживайте streak! 🔥

**Расписание Writing:**
• Пн, Ср, Пт - Task 2
• Вт, Чт, Сб - Task 1
• Вс - отдых

Удачи в подготовке к IELTS! 🎯
"""

    await update.message.reply_text(help_text, parse_mode='Markdown')


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle inline button presses"""
    query = update.callback_query
    user = query.from_user
    ensure_user_registered(user)

    await query.answer()

    data = query.data

    if data.startswith("toggle_"):
        # Parse callback data: toggle_{user_id}_{task_id}
        parts = data.split("_", 2)
        if len(parts) >= 3:
            target_user_id = int(parts[1])
            task_id = parts[2]
        else:
            # Old format fallback
            logger.warning(f"Old callback format detected: {data}")
            return

        # Toggle task completion for target user
        current_status = db.get_today_status(target_user_id)
        new_status = not current_status.get(task_id, False)

        db.mark_task(target_user_id, task_id, new_status)

        # Update the message with new keyboard (dual column)
        message_text = format_dual_progress_message()
        keyboard = create_task_keyboard_dual()

        try:
            await query.edit_message_text(
                text=message_text,
                reply_markup=keyboard,
                parse_mode='Markdown'
            )
        except Exception as e:
            logger.error(f"Error editing message: {e}")

    elif data.startswith("task_label_"):
        # Just a label, do nothing
        await query.answer("Нажмите на имя чтобы отметить задачу", show_alert=False)

    elif data == "show_all":
        # Show all users' progress
        summary = format_all_users_summary()
        await query.answer(summary, show_alert=True)


async def send_group_checklist(context: ContextTypes.DEFAULT_TYPE, checklist_type: str = "morning"):
    """Send daily checklist to group chat"""
    if not config.GROUP_CHAT_ID:
        logger.warning("GROUP_CHAT_ID not configured, skipping group message")
        return

    today = date.today()
    is_saturday = today.weekday() == 5
    is_sunday = today.weekday() == 6

    if checklist_type == "morning":
        special = "🎯 **MOCK TEST DAY!**" if is_saturday else ""
        message = f"""
🌅 **УТРЕННЕЕ НАПОМИНАНИЕ** - {today.strftime('%d.%m.%Y')}
{special}
─────────────────
⏰ Дедлайн: до 14:30

**Задачи:**
📖 Reading (60-90 мин)
🎧 Listening (30-45 мин)

Используйте /today чтобы отметить задачи!
Смотрите прогресс друг друга: /all
"""
    else:  # afternoon
        special = "😌 **ЛЁГКИЙ РЕЖИМ**" if is_sunday else ""
        writing_task = get_writing_task()
        message = f"""
🌤️ **ДНЕВНОЕ НАПОМИНАНИЕ** - {today.strftime('%d.%m.%Y')}
{special}
─────────────────
⏰ Дедлайн: до вечера

**Задачи:**
{writing_task}
🗣 Speaking (30 мин)
📝 Error Notebook Review
📚 Vocabulary (10-15 мін)
📝 Articles (10 мін)

Используйте /today чтобы отметить задачи!
Смотрите прогресс друг друга: /all
"""

    try:
        await context.bot.send_message(
            chat_id=config.GROUP_CHAT_ID,
            text=message,
            parse_mode='Markdown'
        )
    except Exception as e:
        logger.error(f"Error sending group message: {e}")


async def send_morning_reminder(context: ContextTypes.DEFAULT_TYPE):
    """Send morning reminder"""
    logger.info("Sending morning reminders")
    await send_group_checklist(context, "morning")


async def send_afternoon_reminder(context: ContextTypes.DEFAULT_TYPE):
    """Send afternoon reminder"""
    logger.info("Sending afternoon reminders")
    await send_group_checklist(context, "afternoon")


async def send_daily_topic(context: ContextTypes.DEFAULT_TYPE):
    """Send daily IELTS vocabulary topic"""
    logger.info("Sending daily IELTS topic")

    if not config.GROUP_CHAT_ID:
        logger.warning("GROUP_CHAT_ID not configured, skipping topic message")
        return

    try:
        # Get today's topic
        day_number = get_current_day_number(config.TOPICS_START_DATE)
        topic = get_current_topic(config.TOPICS_START_DATE)
        message = format_topic_message(topic, day_number)

        # Send to group
        await context.bot.send_message(
            chat_id=config.GROUP_CHAT_ID,
            text=message,
            parse_mode='Markdown'
        )
        logger.info(f"Sent topic for Day {day_number}: {topic['name']}")

    except Exception as e:
        logger.error(f"Error sending daily topic: {e}")


def main():
    """Main function to run the bot"""
    if not config.BOT_TOKEN:
        logger.error("BOT_TOKEN not set in environment variables!")
        return

    # Create application
    application = Application.builder().token(config.BOT_TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("today", today_command))
    application.add_handler(CommandHandler("all", all_command))
    application.add_handler(CommandHandler("stats", stats_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CallbackQueryHandler(button_handler))

    # Start the bot
    logger.info("Bot started")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
