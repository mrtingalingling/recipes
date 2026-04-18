-- T3: User profile schema for SQLite
CREATE TABLE IF NOT EXISTS user_profile (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  budget REAL NOT NULL,
  household_size INTEGER NOT NULL,
  dietary_preferences TEXT,
  cooking_time INTEGER NOT NULL
);
