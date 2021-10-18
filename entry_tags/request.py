import sqlite3
import json
from models import Entry_Tag


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

            entry = Entry_Tag(row['id'], row['entry_id'],
                          row['tag_id'])
            entry_tags.append(entry.__dict__)

    # Use `json` package to properly serialize list as JSON
    return json.dumps(entry_tags)