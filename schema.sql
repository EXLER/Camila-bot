CREATE TABLE events
(
    creator_id      INTEGER NOT NULL,
    event_title     TEXT PRIMARY KEY,
    event_date      TEXT NOT NULL,
    event_group     TEXT NOT NULL
);