import time
from sqlite3 import Cursor, Connection

from database.init import create_tables


def init_db(cur: Cursor) -> None:
    create_tables(cur)


def save_email(con: Connection, email: str, spam_state: int):
    spam_state_str = ""

    if spam_state == 1:
        spam_state_str = "Spam"
    else:
        spam_state_str = "Not Spam"

    result = con.cursor().execute("""
    INSERT INTO email_history (email_body, spam_state, date_created) VALUES (?, ?, ?);
    """, (email, spam_state_str, time.time()))
    con.commit()


def get_email(con: Connection) -> list[dict]:
    cur = con.cursor()
    cur.execute("""SELECT id,email_body, spam_state, date_created FROM email_history ORDER BY date_created DESC;""")
    rows = cur.fetchall()
    return rows
