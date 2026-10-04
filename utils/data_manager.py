import sqlite3
from pathlib import Path
import streamlit as st

BASE_DIR = Path(__file__).resolve().parent.parent
DB_FILE = BASE_DIR / "data" / "users.db"

DB_FILE.parent.mkdir(parents=True, exist_ok=True)


def get_connection():
    return sqlite3.connect(DB_FILE)


def create_data_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS quiz_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            score INTEGER NOT NULL,
            total INTEGER NOT NULL,
            accuracy REAL NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            filename TEXT NOT NULL,
            content TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS study_hours (
            user_id INTEGER PRIMARY KEY,
            hours REAL NOT NULL DEFAULT 0
        )
    """)

    conn.commit()
    conn.close()


create_data_tables()


def get_current_user_id():
    return st.session_state.get("user_id")


# ---------------- QUIZ ----------------

def save_quiz_result(score, total, accuracy):
    user_id = get_current_user_id()

    if user_id is None:
        return

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO quiz_results
        (user_id, score, total, accuracy)
        VALUES (?, ?, ?, ?)
    """, (user_id, score, total, float(accuracy)))

    conn.commit()
    conn.close()


def get_quiz_results():
    user_id = get_current_user_id()

    if user_id is None:
        return []

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT score, total, accuracy
        FROM quiz_results
        WHERE user_id = ?
        ORDER BY id
    """, (user_id,))

    rows = cursor.fetchall()
    conn.close()

    return [
        {
            "score": row[0],
            "total": row[1],
            "accuracy": row[2]
        }
        for row in rows
    ]


def get_quiz_stats():
    results = get_quiz_results()

    if not results:
        return {
            "quiz_count": 0,
            "accuracy": 0
        }

    accuracies = [
        float(result["accuracy"])
        for result in results
    ]

    return {
        "quiz_count": len(results),
        "accuracy": round(
            sum(accuracies) / len(accuracies),
            2
        )
    }


# ---------------- NOTES ----------------

def save_note(filename, content):
    user_id = get_current_user_id()

    if user_id is None:
        return

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id
        FROM notes
        WHERE user_id = ?
        AND filename = ?
    """, (user_id, filename))

    existing = cursor.fetchone()

    if existing:
        cursor.execute("""
            UPDATE notes
            SET content = ?
            WHERE id = ?
        """, (content, existing[0]))

    else:
        cursor.execute("""
            INSERT INTO notes
            (user_id, filename, content)
            VALUES (?, ?, ?)
        """, (user_id, filename, content))

    conn.commit()
    conn.close()


def get_notes():
    user_id = get_current_user_id()

    if user_id is None:
        return {}

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT filename, content
        FROM notes
        WHERE user_id = ?
        ORDER BY id
    """, (user_id,))

    rows = cursor.fetchall()
    conn.close()

    return {
        row[0]: row[1]
        for row in rows
    }


def delete_note(filename):
    user_id = get_current_user_id()

    if user_id is None:
        return

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM notes
        WHERE user_id = ?
        AND filename = ?
    """, (user_id, filename))

    conn.commit()
    conn.close()


def get_notes_count():
    user_id = get_current_user_id()

    if user_id is None:
        return 0

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM notes
        WHERE user_id = ?
    """, (user_id,))

    count = cursor.fetchone()[0]

    conn.close()

    return count


# ---------------- STUDY HOURS ----------------

def save_study_hours(hours):
    user_id = get_current_user_id()

    if user_id is None:
        return

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO study_hours
        (user_id, hours)
        VALUES (?, ?)
        ON CONFLICT(user_id)
        DO UPDATE SET hours = excluded.hours
    """, (user_id, float(hours)))

    conn.commit()
    conn.close()


def get_study_hours():
    user_id = get_current_user_id()

    if user_id is None:
        return 0

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT hours
        FROM study_hours
        WHERE user_id = ?
    """, (user_id,))

    result = cursor.fetchone()

    conn.close()

    if result:
        return float(result[0])

    return 0


# ---------------- DASHBOARD ----------------

def get_dashboard_stats():

    quiz_stats = get_quiz_stats()

    return {
        "notes": get_notes_count(),
        "quizzes": quiz_stats["quiz_count"],
        "accuracy": quiz_stats["accuracy"],
        "study_hours": get_study_hours()
    }