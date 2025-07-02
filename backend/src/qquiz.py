import os
import sqlite3
import json
import time
from datetime import datetime

from consts import ROOT_DIR
import qlogs

DB_PATH = os.path.join(ROOT_DIR, 'db/quiz.db')

CONNECTION = sqlite3.connect(DB_PATH)
CURSOR = CONNECTION.cursor()

CURSOR.execute('''
CREATE TABLE IF NOT EXISTS quiz (
    guild INTEGER,
    month INTEGER,
    year INTEGER,
    questions TEXT,
    join_message INTEGER,
    leaderboard_message INTEGER,
    active INTEGER,
    PRIMARY KEY(guild, month, year)
)''')

CURSOR.execute('''
CREATE TABLE IF NOT EXISTS questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question TEXT UNIQUE,
    A TEXT,
    B TEXT,
    C TEXT,
    D TEXT,
    answer TEXT,
    category TEXT,
    difficulty TEXT
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


def add_question(question: dict) -> int:
    """Insert *question* into the questions table if new and return its id."""
    CURSOR.execute('SELECT id FROM questions WHERE question=?', (question["q"],))
    row = CURSOR.fetchone()
    if row:
        return row[0]
    CURSOR.execute(
        'INSERT INTO questions (question, A, B, C, D, answer, category, difficulty) '
        'VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
        (
            question["q"],
            question["A"],
            question["B"],
            question["C"],
            question["D"],
            question["answer"],
            question.get("category", ""),
            question.get("difficulty", ""),
        ),
    )
    CONNECTION.commit()
    qlogs.info(f"ADDED QUESTION :: {question['q']} [{question.get('category','')}]")
    return CURSOR.lastrowid


def get_question(qid: int) -> dict | None:
    CURSOR.execute(
        'SELECT question, A, B, C, D, answer, category, difficulty FROM questions WHERE id=?',
        (qid,),
    )
    row = CURSOR.fetchone()
    if not row:
        return None
    keys = ["q", "A", "B", "C", "D", "answer", "category", "difficulty"]
    return dict(zip(keys, row))


def start_quiz(guild: int, month: int, year: int, questions: list, join_message: int, leaderboard_message: int):
    ids = [add_question(q) for q in questions]
    CURSOR.execute(
        '''INSERT OR REPLACE INTO quiz (guild, month, year, questions, join_message, leaderboard_message, active)
           VALUES (?, ?, ?, ?, ?, ?, 1)''',
        (guild, month, year, json.dumps(ids), join_message, leaderboard_message),
    )
    CONNECTION.commit()
    qlogs.info(f"LAUNCHED QUIZ :: guild {guild} {month}/{year}")


def end_quiz(guild: int, month: int, year: int):
    CURSOR.execute('UPDATE quiz SET active = 0 WHERE guild = ? AND month = ? AND year = ?',
                   (guild, month, year))
    CONNECTION.commit()
    qlogs.info(f"END QUIZ :: guild {guild} {month}/{year}")


def get_active_quiz(guild: int):
    CURSOR.execute('SELECT month, year, questions, join_message, leaderboard_message FROM quiz WHERE guild = ? AND active = 1',
                   (guild,))
    row = CURSOR.fetchone()
    if not row:
        return None
    month, year, qids, join_msg, lb_msg = row
    questions = [get_question(i) for i in json.loads(qids)]
    answers = [q["answer"] for q in questions if q]
    return month, year, questions, answers, join_msg, lb_msg


def get_quiz(guild: int, month: int, year: int):
    CURSOR.execute('SELECT questions, join_message, leaderboard_message FROM quiz WHERE guild=? AND month=? AND year=?',
                   (guild, month, year))
    row = CURSOR.fetchone()
    if not row:
        return None
    qids, join_msg, lb_msg = row
    questions = [get_question(i) for i in json.loads(qids)]
    answers = [q["answer"] for q in questions if q]
    return questions, answers, join_msg, lb_msg


def add_score(guild: int, month: int, year: int, user: str, score: int, timetaken: int, disqualified: bool = False):
    CURSOR.execute(
        '''INSERT OR REPLACE INTO scores
           (guild, month, year, user, score, timetaken, timepart, disqualified)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
        (guild, month, year, user, score, timetaken, int(time.time()), int(disqualified)),
    )
    CONNECTION.commit()
    qlogs.info(
        f"LEADERBOARD ENTRY :: {user} {score}pts {timetaken}s ({'DQ' if disqualified else 'OK'})"
    )


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
        CURSOR.execute('SELECT question FROM questions WHERE category=?', (category,))
    else:
        # only questions that already appeared in quizzes on this guild
        CURSOR.execute('SELECT questions FROM quiz WHERE guild=?', (guild,))
        ids = set()
        for row in CURSOR.fetchall():
            ids.update(json.loads(row[0]))
        if not ids:
            return []
        marks = ','.join('?' for _ in ids)
        CURSOR.execute(
            f'SELECT question FROM questions WHERE id IN ({marks}) AND category=?',
            (*ids, category),
        )
    return [r[0] for r in CURSOR.fetchall()]

