import sqlite3
import json
from models import Mood

def get_all_moods():
    # Open a connection to the database
    with sqlite3.connect("./daily_journal.db") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            m.id,
            m.label
        FROM moods m
        """)

        # Initialize an empty list to hold all entries representations
        moods = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:

            # Create an moods instance from the current row.
            # Note that the database fields are specified in
            # exact order of the parameters defined in the
            # moods class above.
            mood = Mood(row['id'], row['label'])

            moods.append(mood.__dict__)

    # Use `json` package to properly serialize list as JSON
    return json.dumps(moods)

def get_single_mood(id):
    # Open a connection to the database
    with sqlite3.connect("./daily_journal.db") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            m.id,
            m.label
        FROM moods m
        WHERE m.id = ?
        """, (id, ))

        # Convert rows of data into a Python list
        data = db_cursor.fetchone()

        mood = Mood(data['id'], data['label'])

    # Use `json` package to properly serialize list as JSON
    return json.dumps(mood.__dict__)


def delete_mood(id):
    # Delete entry
    with sqlite3.connect("./daily_journal.db") as conn:
            db_cursor = conn.cursor()

            db_cursor.execute("""
            DELETE FROM moods
            WHERE id = ?
            """, (id,))
