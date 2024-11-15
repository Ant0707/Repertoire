import pytest
from api.User import User
from api.create_tables import create_tables
from api.get_db_connection import get_db_connection
from api.get_all_users import get_all_users


@pytest.fixture
def setup_db():
    """Setup the database connection and ensure tables are created before tests."""
    conn = get_db_connection()
    if conn is None:
        pytest.fail("Database connection failed")

    create_tables()  # Make sure tables exist
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users")  # Clean up the users table before each test
    conn.commit()
    conn.close()

@pytest.fixture
def user(setup_db):
    """Fixture for creating a test user."""
    u = User(first_name="Robert", last_name="Dupont", address="1 rue du chemin, 75000 Paris", phone_number="0123456789")
    u.save()
    return u


def test_first_name(user):
    assert user.first_name == "Robert"

def test_last_name(user):
    assert user.last_name == "Dupont"

def test_address(user):
    assert user.address == "1 rue du chemin, 75000 Paris"

def test_phone_number(user):
    assert user.phone_number == "0123456789"


def test_full_name(user):
    assert user.full_name == "Robert Dupont"


def test__check_phone_number(setup_db):
    user_good = User(first_name="Jean",
                     last_name="Martin",
                     address="1 rue du chemin, 75000 Paris",
                     phone_number="0123456789")
    user_bad = User(first_name="Jean",
                    last_name="Martin",
                    address="1 rue du chemin, 75000 Paris",
                    phone_number="fsdrhg")

    with pytest.raises(ValueError) as err:
        user_bad._check_phone_number()

    assert "invalide" in str(err.value)

    user_good.save(validate_data=True)
    assert user_good.exists() is True


def test__check_names_empty(setup_db):
    user_bad = User(first_name="",
                    last_name="",
                    address="1 rue du chemin, 75000 Paris",
                    phone_number="0123456789")

    with pytest.raises(ValueError) as err:
        user_bad._check_names()

    assert "Le prénom et le nom de famille ne peuvent pas être vides." in str(err.value)


def test__check_names_invalid_characters(setup_db):
    user_good = User(first_name="Jean",
                     last_name="Martin",
                     address="1 rue du chemin, 75000 Paris",
                     phone_number="0123456789")
    user_bad = User(first_name="P?ie%rre&",
                    last_name="Dur!an:d",
                    address="1 rue du chemin, 75000 Paris",
                    phone_number="0123456789")

    with pytest.raises(ValueError) as err:
        user_bad._check_names()

    assert "Nom invalide" in str(err.value)

    user_good.save(validate_data=True)
    assert user_good.exists() is True


def test_exists(user):
    """Test that the user exists in the database."""
    assert user.exists() == True


def test_not_exists(setup_db):
    """Test that a user that was not saved doesn't exist."""
    u = User(first_name="Robert", last_name="Dupont", address="1 rue du chemin, 75000 Paris", phone_number="0123456789")
    assert u.exists() == False


def test_delete(setup_db):
    user_test = User(first_name="Jean", last_name="Martin", address="1 rue du chemin, 75000 Paris", phone_number="0123456789")
    user_test.save()

    # Suppression de l'utilisateur via l'API
    assert user_test.delete() is True

    # Vérification que l'utilisateur n'existe plus
    assert user_test.exists() is False



def test_save(setup_db):
    user_test = User(first_name="Jean",
                     last_name="Martin",
                     address="1 rue du chemin, 75000 Paris",
                     phone_number="0123456789")
    user_test_duplicated = User(first_name="Jean",
                                last_name="Martin",
                                address="1 rue du chemin, 75000 Paris",
                                phone_number="0123456789")

    first = user_test.save()
    second = user_test_duplicated.save()
    assert isinstance(first, int)
    assert isinstance(second, int)
    assert first > 0
    assert second == -1

def test_get_all_users(setup_db):
    user1 = User(first_name="Jean", last_name="Martin", phone_number="0123456789", address="1 rue du chemin, Paris")
    user1.save()
    user2 = User(first_name="Paul", last_name="Durand", phone_number="0987654321", address="2 rue de la Paix, Lyon")
    user2.save()

    users = get_all_users()
    assert len(users) == 2
    assert users[0].first_name == "Jean"
    assert users[1].last_name == "Durand"
