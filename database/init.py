from sqlite3 import Cursor


def create_tables(cursor: Cursor) -> None:
    print("Creating tables...")
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS email_history(
    id   INTEGER PRIMARY KEY AUTOINCREMENT,
    email_body   TEXT    NOT NULL,
    spam_state   TEXT    NOT NULL,
    date_created INTEGER NOT NULL
   );
   """

                   )
