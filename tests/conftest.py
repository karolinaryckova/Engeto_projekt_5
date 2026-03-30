import pytest

from db import pripojeni_db, vytvoreni_tabulky


@pytest.fixture
def test_connection():
    connection = pripojeni_db("task_manager_test_db")
    vytvoreni_tabulky(connection)

    cursor = connection.cursor()
    cursor.execute("DELETE FROM ukoly")
    connection.commit()
    cursor.close()

    yield connection

    cursor = connection.cursor()
    cursor.execute("DELETE FROM ukoly")
    connection.commit()
    cursor.close()
    connection.close()