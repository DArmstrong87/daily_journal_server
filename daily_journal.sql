CREATE TABLE Entries(
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    concept VARCHAR(20),
    entry text,
    mood_id int,
    date date,
    FOREIGN KEY (mood_id) REFERENCES Moods(id)
);
CREATE TABLE Moods(
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, label VARCHAR(15));


INSERT INTO `Entries`
VALUES (
        null,
        'SQL',
        "Learned a bit on what the .execute() does and its syntax.",
        1,
        '2021-10-14'
    );


SELECT *
FROM Entries;

SELECT *, e.id, m.id mood_id
FROM entries e
JOIN Moods m
ON e.mood_id = mood_id
WHERE e.id = 2;

SELECT *, e.id
FROM Entries e
JOIN Moods m
    ON m.id = e.mood_id;

SELECT *
FROM Moods;

SELECT *
FROM Entries
WHERE entry LIKE '%sql%';