import sqlite3
from datetime import datetime, date
from typing import Optional, Dict, List, Tuple
import config

class Database:
    def __init__(self, db_path: str = config.DB_PATH):
        self.db_path = db_path
        self.init_db()

    def get_connection(self):
        return sqlite3.connect(self.db_path)

    def init_db(self):
        """Initialize database tables"""
        conn = self.get_connection()
        cursor = conn.cursor()

        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Daily checklist completions
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS completions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                date DATE NOT NULL,
                task_name TEXT NOT NULL,
                completed BOOLEAN DEFAULT 0,
                completed_at TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id),
                UNIQUE(user_id, date, task_name)
            )
        ''')

        # Streak tracking
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS streaks (
                user_id INTEGER PRIMARY KEY,
                current_streak INTEGER DEFAULT 0,
                best_streak INTEGER DEFAULT 0,
                last_completion_date DATE,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        ''')

        conn.commit()
        conn.close()

    def add_user(self, user_id: int, name: str = None, first_name: str = None,
                 last_name: str = None, username: str = None):
        """Add or update user"""
        conn = self.get_connection()
        cursor = conn.cursor()

        # Use first_name as default name if name not provided
        if not name:
            name = first_name or f"User {user_id}"

        cursor.execute('''
            INSERT OR REPLACE INTO users (user_id, name)
            VALUES (?, ?)
        ''', (user_id, name))

        # Initialize streak if not exists
        cursor.execute('''
            INSERT OR IGNORE INTO streaks (user_id, current_streak, best_streak)
            VALUES (?, 0, 0)
        ''', (user_id,))

        conn.commit()
        conn.close()

    def get_user_name(self, user_id: int) -> str:
        """Get user's name from database"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('SELECT name FROM users WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()
        conn.close()

        if result:
            return result[0]
        return f"User {user_id}"

    def get_all_users(self) -> Dict[int, str]:
        """Get all users as dict {user_id: name}"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('SELECT user_id, name FROM users')
        results = cursor.fetchall()
        conn.close()

        return {user_id: name for user_id, name in results}

    def mark_task(self, user_id: int, task_name: str, completed: bool = True) -> bool:
        """Mark a task as completed or not completed for today"""
        conn = self.get_connection()
        cursor = conn.cursor()
        today = date.today()

        cursor.execute('''
            INSERT OR REPLACE INTO completions (user_id, date, task_name, completed, completed_at)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, today, task_name, completed, datetime.now() if completed else None))

        conn.commit()
        conn.close()

        # Update streak if all tasks are completed
        if completed:
            self.update_streak(user_id)

        return True

    def get_today_status(self, user_id: int) -> Dict[str, bool]:
        """Get today's completion status for a user"""
        conn = self.get_connection()
        cursor = conn.cursor()
        today = date.today()

        cursor.execute('''
            SELECT task_name, completed
            FROM completions
            WHERE user_id = ? AND date = ?
        ''', (user_id, today))

        results = cursor.fetchall()
        conn.close()

        return {task: bool(completed) for task, completed in results}

    def get_daily_tasks(self) -> List[str]:
        """Get all task names for today based on schedule"""
        tasks = []

        # Morning tasks
        for task_id, task_name in config.MORNING_TASKS:
            tasks.append(task_id)

        # Afternoon tasks (including dynamic writing)
        for task_id, task_name in config.AFTERNOON_TASKS:
            tasks.append(task_id)

        return tasks

    def is_day_complete(self, user_id: int, check_date: Optional[date] = None) -> bool:
        """Check if user completed all tasks for a given day"""
        if check_date is None:
            check_date = date.today()

        conn = self.get_connection()
        cursor = conn.cursor()

        # Get expected tasks for that day
        expected_tasks = self.get_daily_tasks()

        cursor.execute('''
            SELECT COUNT(*)
            FROM completions
            WHERE user_id = ? AND date = ? AND completed = 1
        ''', (user_id, check_date))

        completed_count = cursor.fetchone()[0]
        conn.close()

        return completed_count >= len(expected_tasks)

    def update_streak(self, user_id: int):
        """Update user's streak based on completion history"""
        conn = self.get_connection()
        cursor = conn.cursor()
        today = date.today()

        # Get current streak info
        cursor.execute('SELECT current_streak, best_streak, last_completion_date FROM streaks WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()

        if not result:
            return

        current_streak, best_streak, last_date_str = result

        # Check if today is complete
        if not self.is_day_complete(user_id, today):
            return

        # Parse last completion date
        if last_date_str:
            last_date = datetime.strptime(last_date_str, '%Y-%m-%d').date()
            days_diff = (today - last_date).days

            if days_diff == 1:
                # Continue streak
                current_streak += 1
            elif days_diff == 0:
                # Same day, no change
                pass
            else:
                # Streak broken, restart
                current_streak = 1
        else:
            # First completion
            current_streak = 1

        # Update best streak
        best_streak = max(best_streak, current_streak)

        cursor.execute('''
            UPDATE streaks
            SET current_streak = ?, best_streak = ?, last_completion_date = ?
            WHERE user_id = ?
        ''', (current_streak, best_streak, today, user_id))

        conn.commit()
        conn.close()

    def get_streak(self, user_id: int) -> Tuple[int, int]:
        """Get current and best streak for user"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('SELECT current_streak, best_streak FROM streaks WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()
        conn.close()

        if result:
            return result
        return (0, 0)

    def get_week_stats(self, user_id: int) -> Dict[str, int]:
        """Get weekly statistics for user"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT task_name, COUNT(*)
            FROM completions
            WHERE user_id = ?
            AND date >= date('now', '-7 days')
            AND completed = 1
            GROUP BY task_name
        ''', (user_id,))

        results = cursor.fetchall()
        conn.close()

        return {task: count for task, count in results}

# Initialize database
db = Database()

# Add preconfigured users from config
for user_id, name in config.STUDY_BUDDIES.items():
    db.add_user(user_id, name)
