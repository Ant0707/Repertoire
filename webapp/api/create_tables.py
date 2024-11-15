from api.get_db_connection import get_db_connection

def create_tables():
    conn = get_db_connection()
    if conn is None:
        return

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            phone_number TEXT,
            address TEXT
        )
    """)

    print("Tables créées ou déjà existantes.")
    conn.commit()
    conn.close()
