import sqlite3
import json
from models import EntryTag


def get_all_entry_tags():
    # Open a connection to the database
    with sqlite3.connect("./daily_journal.db") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT *
        FROM entry_tag
        """)

        # Initialize an empty list to hold all entries representations
        entry_tags = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:

            entry = EntryTag(row['id'], row['entry_id'], row['tag_id'])
            entry_tags.append(entry.__dict__)

    # Use `json` package to properly serialize list as JSON
    return json.dumps(entry_tags)


def create_entry_tag(entry_tag):
    with sqlite3.connect("./daily_journal.db") as conn:
        db_cursor = conn.cursor()
        db_cursor.execute("""
        INSERT INTO entry_tag
            (entry_id, tag_id)
        VALUES (?, ?)
        """, (entry_tag['entry_id'], entry_tag['tag_id']))

        id = db_cursor.lastrowid
        entry_tag['id'] = id

    return json.dumps(entry_tag)


def delete_entrytag(id):
# Delete entry
    with sqlite3.connect("./daily_journal.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
            DELETE FROM entry_tag
            WHERE id = ?
            """, (id,))