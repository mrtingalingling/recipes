-- T8: Store normalized deal data in DB
CREATE TABLE IF NOT EXISTS store_deals (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  store_name TEXT NOT NULL,
  product_name TEXT NOT NULL,
  price REAL NOT NULL,
  validity_start DATE,
  validity_end DATE,
  geo_location TEXT
);
