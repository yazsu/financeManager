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
#         CREATE TABLE IF NOT EXISTS users (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             username TEXT UNIQUE NOT NULL,
#             email TEXT UNIQUE,
#             password_hash TEXT NOT NULL,
#             salario REAL DEFAULT 0.0,
#             created_at DATETIME DEFAULT CURRENT_TIMESTAMP
#         )
#     """)

# cur.execute("""
#                UPDATE users SET password = 2004 WHERE id = 2;
#                """)
# muda o valor na coluna da tabela localizando pelo id

#coloca colunas na tabela
# cur.execute("""ALTER TABLE demandas 
#              ADD descricao TEXT""")


# cur.execute("""
#              DROP TABLE users""")

conn.commit()

conn.close()