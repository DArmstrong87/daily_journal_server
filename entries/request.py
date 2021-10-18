import sqlite3
import json
from models import Entry
from models import Mood


def get_all_entries():
    # Open a connection to the database
    with sqlite3.connect("./daily_journal.db") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT *, e.id, m.id mid
        FROM Entries e
        JOIN Moods m
            ON m.id = e.mood_id
        """)

        # Initialize an empty list to hold all entries representations
        entries = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:

            entry = Entry(row['id'], row['concept'],
                          row['entry'], row['mood_id'], row['date'])

            mood = Mood(row['mid'], row['label'])

            entry.mood = mood.__dict__
            entries.append(entry.__dict__)

    # Use `json` package to properly serialize list as JSON
    return json.dumps(entries)


def get_single_entry(id):
    # Open a connection to the database
    with sqlite3.connect("./daily_journal.db") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            a.id,
            a.concept,
            a.entry,
            a.mood_id,
            a.date,
            a.mood
        FROM entries a
        JOIN Moods
        ON mood_id = moods.id
        WHERE a.id = ?
        """, (id, ))

        # Convert rows of data into a Python list
        data = db_cursor.fetchone()

        entry = Entry(data['id'], data['concept'],
                      data['entry'], data['mood_id'], data['date'])

    # Use `json` package to properly serialize list as JSON
    return json.dumps(entry.__dict__)


def delete_entry(id):
    # Delete entry
    with sqlite3.connect("./daily_journal.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
            DELETE FROM entries
            WHERE id = ?
            """, (id,))


def get_entries_by_term(term):
    with sqlite3.connect("./daily_journal.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            a.id,
            a.concept,
            a.entry,
            a.mood_id,
            a.date
        FROM entries a
        WHERE a.entry LIKE ?;
        """, (f"%{term}%", ))

        entries = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            entry = Entry(row['id'], row['concept'],
                          row['entry'], row['mood_id'], row['date'])

            entries.append(entry.__dict__)

    return json.dumps(entries)


def create_journal_entry(new_entry):
    with sqlite3.connect("./daily_journal.db") as conn:
        db_cursor = conn.cursor()
        db_cursor.execute("""
        INSERT INTO Entries
            (concept, entry, mood_id, date)
        VALUES (?,?,?,?)
        """,
                          (new_entry['concept'], new_entry['entry'],
                           new_entry['mood_id'], new_entry['date'])
                          )

        id = db_cursor.lastrowid
        new_entry['id'] = id

    return json.dumps(new_entry)


def update_entry(id, new_entry):
    with sqlite3.connect("./daily_journal.db") as conn:
        db_cursor = conn.cursor()
        db_cursor.execute("""
        UPDATE entries
        SET concept = ?,
            entry = ?,
            mood_id = ?,
            date = ?
        WHERE id = ?
        """, (new_entry['concept'], new_entry['entry'], new_entry['mood_id'], new_entry['date'], id))