-- T34: User schema with household link support
CREATE TABLE IF NOT EXISTS user_profiles (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT,
  budget REAL,
  preferences TEXT,
  household_id INTEGER
);
CREATE TABLE IF NOT EXISTS households (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT
);
