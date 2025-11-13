import sqlite3

def get_conn():
    conn = sqlite3.connect("./data/database.db")
    conn.row_factory = sqlite3.Row
    return conn

conn = get_conn()
cur = conn.cursor()

#usuários
# cur.execute("""
#      CREATE TABLE IF NOT EXISTS users (
#          id INTEGER PRIMARY KEY AUTOINCREMENT,  
#          username TEXT UNIQUE,
#          password TEXT
#      )
#  """)

# cur.execute("""
#             INSERT INTO users (username, password) VALUES (?,?)
#             """, ("pablo","2112"))

conn.commit()

conn.close()