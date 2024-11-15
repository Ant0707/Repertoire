from api.User import User
from api.get_db_connection import get_db_connection


def get_user_by_id(user_id):
    try:
        conn = get_db_connection()
        if conn is None:
            print("Erreur : Échec de la connexion à la base de données.")
            return None

        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", [user_id])
        row = cursor.fetchone()

        if row is None:
            print(f"Aucun utilisateur trouvé avec l'ID : {user_id}")
            return None
        else:
            user = User(id=row[0], first_name=row[1], last_name=row[2], phone_number=row[3], address=row[4])
            print(f"Utilisateur récupéré : {user}")
            return user
    except Exception as e:
        print(f"Erreur lors de la récupération de l'utilisateur : {e}")
        return None
    finally:
        if conn:
            conn.close()
