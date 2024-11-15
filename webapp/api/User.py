import re
import string
from faker import Faker
from api.get_db_connection import get_db_connection
from api.create_tables import create_tables


class User:
    def __init__(self, first_name: str, last_name: str = "", phone_number: str = "", address: str = "", id: int = None):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
        self.address = address

    def __repr__(self):
        return f"User({self.first_name}, {self.last_name})"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def _checks(self):
        self._check_names()
        self._check_phone_number()

    def _check_phone_number(self):
        phone_number = re.sub(r"[+()\s]*", "", self.phone_number)
        if len(phone_number) < 10 or not phone_number.isdigit():
            raise ValueError(f"Numéro de téléphone {self.phone_number} invalide")

    def _check_names(self):
        if not (self.first_name and self.last_name):
            raise ValueError("Le prénom et le nom de famille ne peuvent pas être vides.")

        special_characters = string.punctuation + string.digits
        for character in self.first_name + self.last_name:
            if character in special_characters:
                raise ValueError(f"Nom invalide {self.full_name}")

    def exists(self):
        conn = get_db_connection()
        if conn is None:
            return False

        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM users WHERE first_name = ? AND last_name = ?
        ''', (self.first_name, self.last_name))
        user = cursor.fetchone()
        conn.close()
        return user is not None

    def save(self, validate_data: bool = False) -> int:
        if validate_data:
            self._checks()
        if self.exists():
            print(f"L'utilisateur {self.full_name} existe déjà.")
            return -1

        conn = get_db_connection()
        if conn is None:
            print("Échec de la connexion à la base de données lors de l'insertion.")
            return -1

        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO users (first_name, last_name, phone_number, address)
                VALUES (?, ?, ?, ?)
            ''', (self.first_name, self.last_name, self.phone_number, self.address))
            conn.commit()
            print(f"Utilisateur {self.full_name} ajouté avec succès.")
            user_id = cursor.lastrowid
        except Exception as e:
            print(f"Erreur lors de l'insertion de l'utilisateur {self.full_name} : {e}")
            user_id = -1
        finally:
            conn.close()
        return user_id

    def delete(self) -> bool:
        conn = get_db_connection()
        if conn is None:
            print("Échec de la connexion à la base de données lors de la suppression.")
            return False

        cursor = conn.cursor()
        try:
            cursor.execute('''
                DELETE FROM users WHERE first_name = ? AND last_name = ?
            ''', (self.first_name, self.last_name))
            if cursor.rowcount == 0:
                print(f"Utilisateur {self.full_name} non trouvé dans la base de données.")
                return False
            conn.commit()
            print(f"Utilisateur {self.full_name} supprimé avec succès.")
            return True
        except Exception as e:
            print(f"Erreur lors de la suppression de l'utilisateur {self.full_name} : {e}")
            return False
        finally:
            conn.close()

    def update(self, phone_number: str, address: str) -> bool:
        conn = get_db_connection()
        if conn is None:
            print("Échec de la connexion à la base de données lors de la modification.")
            return False

        cursor = conn.cursor()
        try:
            cursor.execute('''
                SELECT * FROM users WHERE first_name = ? AND last_name = ?
            ''', (self.first_name, self.last_name))

            if cursor.rowcount == 0:
                print(f"Utilisateur {self.full_name} non trouvé dans la base de données.")
                return False

            cursor.execute('''
                UPDATE users 
                SET phone_number = ?, address = ?
                WHERE first_name = ? AND last_name = ?
            ''', (phone_number, address, self.first_name, self.last_name))

            conn.commit()
            print(f"Utilisateur {self.full_name} mis à jour avec succès.")
            return True
        except Exception as e:
            print(f"Erreur lors de la modification de l'utilisateur {self.full_name} : {e}")
            return False
        finally:
            conn.close()
