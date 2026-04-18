-- T27: Shopping list schema for SQLite
CREATE TABLE IF NOT EXISTS shopping_lists (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER,
  week_start DATE,
  list_json TEXT,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
