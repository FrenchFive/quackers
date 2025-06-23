import os
import sqlite3
import json
import time
from datetime import datetime

from consts import ROOT_DIR

DB_PATH = os.path.join(ROOT_DIR, 'db/quiz.db')

CONNECTION = sqlite3.connect(DB_PATH)
CURSOR = CONNECTION.cursor()

CURSOR.execute('''
CREATE TABLE IF NOT EXISTS quiz (
    guild INTEGER,
    month INTEGER,
    year INTEGER,
    questions TEXT,
    answers TEXT,
    join_message INTEGER,
    leaderboard_message INTEGER,
    active INTEGER,
    PRIMARY KEY(guild, month, year)
)''')

CURSOR.execute('''
CREATE TABLE IF NOT EXISTS scores (
    guild INTEGER,
    month INTEGER,
    year INTEGER,
    user TEXT,
    score INTEGER,
    timetaken INTEGER,
    timepart INTEGER,
    disqualified INTEGER DEFAULT 0,
    PRIMARY KEY(guild, month, year, user)
)''')
CONNECTION.commit()

# Ensure the disqualified column exists in case of older installations
CURSOR.execute("PRAGMA table_info(scores)")
cols = [row[1] for row in CURSOR.fetchall()]
if 'disqualified' not in cols:
    CURSOR.execute('ALTER TABLE scores ADD COLUMN disqualified INTEGER DEFAULT 0')
    CONNECTION.commit()


def start_quiz(guild: int, month: int, year: int, questions: list, answers: list, join_message: int, leaderboard_message: int):
    CURSOR.execute('''INSERT OR REPLACE INTO quiz (guild, month, year, questions, answers, join_message, leaderboard_message, active)
                      VALUES (?, ?, ?, ?, ?, ?, ?, 1)''',
                   (guild, month, year, json.dumps(questions), json.dumps(answers), join_message, leaderboard_message))
    CONNECTION.commit()


def end_quiz(guild: int, month: int, year: int):
    CURSOR.execute('UPDATE quiz SET active = 0 WHERE guild = ? AND month = ? AND year = ?',
                   (guild, month, year))
    CONNECTION.commit()


def get_active_quiz(guild: int):
    CURSOR.execute('SELECT month, year, questions, answers, join_message, leaderboard_message FROM quiz WHERE guild = ? AND active = 1',
                   (guild,))
    row = CURSOR.fetchone()
    if not row:
        return None
    month, year, q, a, join_msg, lb_msg = row
    return month, year, json.loads(q), json.loads(a), join_msg, lb_msg


def get_quiz(guild: int, month: int, year: int):
    CURSOR.execute('SELECT questions, answers, join_message, leaderboard_message FROM quiz WHERE guild=? AND month=? AND year=?',
                   (guild, month, year))
    row = CURSOR.fetchone()
    if not row:
        return None
    q, a, join_msg, lb_msg = row
    return json.loads(q), json.loads(a), join_msg, lb_msg


def add_score(guild: int, month: int, year: int, user: str, score: int, timetaken: int, disqualified: bool = False):
    CURSOR.execute('''INSERT OR REPLACE INTO scores
                      (guild, month, year, user, score, timetaken, timepart, disqualified)
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                   (guild, month, year, user, score, timetaken, int(time.time()), int(disqualified)))
    CONNECTION.commit()


def start_attempt(guild: int, month: int, year: int, user: str):
    """Register a user starting the quiz as disqualified by default."""
    CURSOR.execute('''INSERT OR IGNORE INTO scores
                      (guild, month, year, user, score, timetaken, timepart, disqualified)
                      VALUES (?, ?, ?, ?, 0, 0, ?, 1)''',
                   (guild, month, year, user, int(time.time())))
    CONNECTION.commit()


def has_participated(guild: int, month: int, year: int, user: str) -> bool:
    CURSOR.execute('SELECT 1 FROM scores WHERE guild=? AND month=? AND year=? AND user=?',
                   (guild, month, year, user))
    return CURSOR.fetchone() is not None


def get_leaderboard(guild: int, month: int, year: int):
    CURSOR.execute('''SELECT user, score, timetaken, timepart FROM scores
                      WHERE guild=? AND month=? AND year=? AND disqualified=0
                      ORDER BY score DESC, timetaken ASC''',
                   (guild, month, year))
    return CURSOR.fetchall()


def get_questions_by_category(category: str, guild: int | None = None):
    """Return all questions matching a category.

    If *guild* is provided only questions from that guild are returned,
    otherwise questions from every guild are collected.
    """
    if guild is None:
        CURSOR.execute('SELECT questions FROM quiz')
    else:
        CURSOR.execute('SELECT questions FROM quiz WHERE guild=?', (guild,))
    rows = CURSOR.fetchall()
    res = []
    for row in rows:
        qlist = json.loads(row[0])
        for q in qlist:
            if q.get("category") == category:
                res.append(q["q"])
    return res

