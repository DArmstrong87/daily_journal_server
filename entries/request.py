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
        SELECT
            e.id,
            e.concept,
            e.entry,
            e.mood_id,
            e.date,
            m.id,
            m.label
        FROM Entries e
        JOIN Moods m
            ON e.mood_id = m.id
        """)

        dataset = db_cursor.fetchall()
        entries = []

        # Iterate list of data returned from database
        for row in dataset:
            entry = Entry(row['id'],
                          row['concept'],
                          row['entry'],
                          row['mood_id'],
                          row['date'],
                          []
                          )
            entries.append(entry.__dict__)
            mood = Mood(row['id'], row['label'])
            entry.mood = mood.__dict__

            db_cursor.execute("""
            SELECT t.id, t.name
            from entries e
            join entry_tag et on e.id = et.entry_id
            join tag t on t.id = et.tag_id
            WHERE et.entry_id = ?
            """, (entry.id,))

            tag_set = db_cursor.fetchall()
            print(tag_set)
            for tag_data in tag_set:
                tag = {'id': tag_data['id'], 'name': tag_data['name']}
                entry.tags.append(tag)

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
            e.id,
            e.concept,
            e.entry,
            e.mood_id emid,
            e.date,
            e.tags,
            m.id mid,
            m.label
        FROM Entries e
        JOIN Moods m
            ON mid = e.mood_id
        WHERE e.id = ?
        """, (id, ))

        # Convert rows of data into a Python list
        data = db_cursor.fetchone()

        entry = Entry(data['id'],
                      data['concept'],
                      data['entry'],
                      data['emid'],
                      data['date'],
                      data['tags'])
        mood = Mood(data['mid'], data['label'])
        entry.mood = mood.__dict__

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
            e.id,
            e.concept,
            e.entry,
            e.mood_id,
            e.date,
            e.tags
        FROM entries e
        WHERE e.entry LIKE ?;
        """, (f"%{term}%", ))

        entries = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            entry = Entry(row['id'], row['concept'],
                          row['entry'], row['mood_id'], row['date'], row['tags'])

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
                          (new_entry['concept'],
                           new_entry['entry'],
                           new_entry['mood_id'],
                           new_entry['date']
                           )
                          )

        id = db_cursor.lastrowid
        new_entry['id'] = id

        for tag in new_entry['tags']:
            db_cursor.execute("""
            INSERT INTO entry_tag
                (entry_id, tag_id)
                values (?, ?)
            """, (id, tag))

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

        was_updated = db_cursor.rowcount

        if was_updated:
            return True
        else:
            return False
