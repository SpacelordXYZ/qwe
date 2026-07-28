import sqlite3
from datetime import datetime

DB = "bot.db"


def connect():
    return sqlite3.connect(DB)


def setup():
    con = connect()
    cur = con.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS cases(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        moderator_id INTEGER,
        action TEXT,
        reason TEXT,
        time TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS warnings(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        moderator_id INTEGER,
        reason TEXT,
        time TEXT
    )
    """)

    con.commit()
    con.close()


def add_case(user_id, moderator_id, action, reason):
    con = connect()
    cur = con.cursor()

    cur.execute(
        """
        INSERT INTO cases
        (user_id, moderator_id, action, reason, time)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            user_id,
            moderator_id,
            action,
            reason,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
    )

    case = cur.lastrowid

    con.commit()
    con.close()

    return case


def get_history(user_id):
    con = connect()
    cur = con.cursor()

    cur.execute(
        """
        SELECT *
        FROM cases
        WHERE user_id=?
        ORDER BY id DESC
        """,
        (user_id,)
    )

    data = cur.fetchall()

    con.close()

    return data


def add_warning(user_id, moderator_id, reason):
    con = connect()
    cur = con.cursor()

    cur.execute(
        """
        INSERT INTO warnings
        (user_id, moderator_id, reason, time)
        VALUES (?, ?, ?, ?)
        """,
        (
            user_id,
            moderator_id,
            reason,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
    )

    warn_id = cur.lastrowid

    con.commit()
    con.close()

    return warn_id


def get_warnings(user_id):
    con = connect()
    cur = con.cursor()

    cur.execute(
        """
        SELECT *
        FROM warnings
        WHERE user_id=?
        ORDER BY id DESC
        """,
        (user_id,)
    )

    data = cur.fetchall()

    con.close()

    return data


def remove_warning(warn_id):
    con = connect()
    cur = con.cursor()

    cur.execute(
        """
        DELETE FROM warnings
        WHERE id=?
        """,
        (warn_id,)
    )

    con.commit()
    con.close()


def clear_warnings(user_id):
    con = connect()
    cur = con.cursor()

    cur.execute(
        """
        DELETE FROM warnings
        WHERE user_id=?
        """,
        (user_id,)
    )

    con.commit()
    con.close()