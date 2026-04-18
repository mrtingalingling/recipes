-- T21: Meal plan schema for SQLite
CREATE TABLE IF NOT EXISTS meal_plans (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER,
  week_start DATE,
  plan_json TEXT,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
