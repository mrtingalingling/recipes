# T8: Save normalized deal data in SQLite
def save_store_deals(deals):
    import sqlite3
    conn = sqlite3.connect('user_data.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS store_deals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        store_name TEXT NOT NULL,
        product_name TEXT NOT NULL,
        price REAL NOT NULL,
        validity_start DATE,
        validity_end DATE,
        geo_location TEXT
    )''')
    for deal in deals:
        c.execute('''INSERT INTO store_deals (store_name, product_name, price, validity_start, validity_end, geo_location) VALUES (?, ?, ?, ?, ?, ?)''',
                  (deal['store_name'], deal['product_name'], deal['price'], deal['validity_start'], deal['validity_end'], deal.get('geo_location')))
    conn.commit()
    conn.close()
