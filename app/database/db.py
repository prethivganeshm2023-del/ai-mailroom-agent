

import sqlite3
import os


DATABASE_PATH = os.getenv(
    "DATABASE_PATH",
    "data/mailroom.db"
)


def get_connection():

    os.makedirs(
        os.path.dirname(DATABASE_PATH) or ".",
        exist_ok=True
    )

    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")

    return conn


def initialize_database():

    with get_connection() as conn:

        conn.execute("""
            CREATE TABLE IF NOT EXISTS emails (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sender TEXT NOT NULL,
                subject TEXT NOT NULL,
                body TEXT NOT NULL,
                status TEXT NOT NULL,
                analysis TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS audit_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email_id INTEGER NOT NULL,
                event TEXT NOT NULL,
                details TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(email_id) REFERENCES emails(id)
            )
        """)

        conn.commit()


def save_email(sender, subject, body):

    with get_connection() as conn:

        cursor = conn.execute("""
            INSERT INTO emails (sender, subject, body, status)
            VALUES (?, ?, ?, ?)
        """, (sender, subject, body, "received"))

        conn.commit()

        return cursor.lastrowid


def update_email(email_id, status, analysis):

    with get_connection() as conn:

        conn.execute("""
            UPDATE emails
            SET status = ?, analysis = ?
            WHERE id = ?
        """, (status, analysis, email_id))

        conn.commit()


def get_emails():

    with get_connection() as conn:

        rows = conn.execute("""
            SELECT id, sender, subject, status,
                   analysis, created_at
            FROM emails
            ORDER BY id DESC
        """).fetchall()

        return [dict(row) for row in rows]


def get_email(email_id):

    with get_connection() as conn:

        row = conn.execute("""
            SELECT * FROM emails WHERE id = ?
        """, (email_id,)).fetchone()

        return dict(row) if row else None


def log_event(email_id, event, details=""):

    with get_connection() as conn:

        conn.execute("""
            INSERT INTO audit_logs
            (email_id, event, details)
            VALUES (?, ?, ?)
        """, (email_id, event, details))

        conn.commit()


def get_audit_logs(email_id):

    with get_connection() as conn:

        rows = conn.execute("""
            SELECT * FROM audit_logs
            WHERE email_id = ?
            ORDER BY id DESC
        """, (email_id,)).fetchall()

        return [dict(row) for row in rows]
