import os
from dotenv import load_dotenv
from datetime import time
import pytz

load_dotenv()

# Bot configuration
BOT_TOKEN = os.getenv('BOT_TOKEN')

# Group chat mode
GROUP_CHAT_ID = int(os.getenv('GROUP_CHAT_ID', 0))

# Study buddies - add their IDs and names here
# You can get user IDs by having them send /start to the bot in private
# Or just let them use the bot and their IDs will be added automatically
STUDY_BUDDIES = {}

# Parse user list from env (format: "id1:name1,id2:name2")
users_str = os.getenv('STUDY_BUDDIES', '')
if users_str:
    for user in users_str.split(','):
        if ':' in user:
            user_id, name = user.split(':', 1)
            try:
                STUDY_BUDDIES[int(user_id.strip())] = name.strip()
            except ValueError:
                pass

# Timezone
TIMEZONE = pytz.timezone(os.getenv('TIMEZONE', 'Asia/Almaty'))

# Reminder times
MORNING_TIME = os.getenv('MORNING_REMINDER_TIME', '09:00')
AFTERNOON_TIME = os.getenv('AFTERNOON_REMINDER_TIME', '14:30')
TOPIC_TIME = os.getenv('TOPIC_REMINDER_TIME', '10:00')

# Parse time strings
def parse_time(time_str):
    hour, minute = map(int, time_str.split(':'))
    return time(hour, minute)

MORNING_REMINDER = parse_time(MORNING_TIME)
AFTERNOON_REMINDER = parse_time(AFTERNOON_TIME)
TOPIC_REMINDER = parse_time(TOPIC_TIME)

# Database
DB_PATH = os.getenv('DB_PATH', 'bot_data.db')

# Task configuration by day of week (0=Monday, 6=Sunday)
WRITING_SCHEDULE = {
    0: 'Task 2',  # Monday
    1: 'Task 1',  # Tuesday
    2: 'Task 2',  # Wednesday
    3: 'Task 1',  # Thursday
    4: 'Task 2',  # Friday
    5: 'Task 1',  # Saturday (+ Mock Test)
    6: None       # Sunday - rest day
}

# Daily tasks structure
MORNING_TASKS = [
    ('reading', '📖 Reading (60-90 мин)'),
    ('listening', '🎧 Listening (30-45 мин)')
]

AFTERNOON_TASKS = [
    ('writing', '✍️ Writing'),  # Will be dynamic based on day
    ('speaking', '🗣 Speaking (30 мин)'),
    ('error_review', '📝 Error Notebook Review'),
    ('vocabulary', '📚 Vocabulary (10-15 мин)'),
    ('articles', '📝 Articles (10 мин)')
]

# IELTS Topics - 30 Day Plan
# Set your start date for the 30-day plan (format: YYYY-MM-DD)
# If None, the plan will cycle through topics based on day of year
from datetime import datetime as dt
TOPICS_START_DATE_STR = os.getenv('TOPICS_START_DATE', None)
TOPICS_START_DATE = dt.strptime(TOPICS_START_DATE_STR, '%Y-%m-%d').date() if TOPICS_START_DATE_STR else None
