import sqlite3
import hashlib
from pathlib import Path


# ==========================================
# DATABASE
# ==========================================

BASE_DIR = Path(__file__).resolve().parent.parent
DB_FILE = BASE_DIR / "data" / "users.db"

DB_FILE.parent.mkdir(parents=True, exist_ok=True)


def get_connection():
    return sqlite3.connect(DB_FILE)


# ==========================================
# CREATE USERS TABLE
# ==========================================

def create_users_table():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


# ==========================================
# PASSWORD
# ==========================================

def hash_password(password):

    return hashlib.sha256(
        password.encode("utf-8")
    ).hexdigest()


# ==========================================
# REGISTER
# ==========================================

def register_user(username, password):

    conn = get_connection()
    cursor = conn.cursor()

    try:

        cursor.execute(
            """
            INSERT INTO users
            (username, password)
            VALUES (?, ?)
            """,
            (
                username.strip(),
                hash_password(password)
            )
        )

        conn.commit()

        return True

    except sqlite3.IntegrityError:

        return False

    finally:

        conn.close()


# ==========================================
# LOGIN
# ==========================================

def login_user(username, password):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, username
        FROM users
        WHERE username = ?
        AND password = ?
        """,
        (
            username.strip(),
            hash_password(password)
        )
    )

    user = cursor.fetchone()

    conn.close()

    return user