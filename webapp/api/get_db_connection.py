import sqlite3

def get_db_connection():
    try:
        conn = sqlite3.connect('db.sqlite3')
        print("Connexion à la base de données SQLite réussie.")
        return conn
    except Exception as e:
        print(f"Erreur lors de la connexion à la base de données : {e}")
        return None
