from api.User import User
from api.get_db_connection import get_db_connection


def get_all_users():
    conn = get_db_connection()
    if conn is None:
        return []

    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    conn.close()

    return [User(id=user[0], first_name=user[1], last_name=user[2], phone_number=user[3], address=user[4]) for user in
            users]
