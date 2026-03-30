import pytest

from db import pripojeni_db, vytvoreni_tabulky
from task_manager import (
    pridat_ukol_db,
    aktualizovat_ukol_db,
    odstranit_ukol_db
)


@pytest.fixture
def test_connection():
    """
    Připojí se k testovací databázi, připraví tabulku
    a po testu uklidí testovací data.
    """
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


def test_pridat_ukol_pozitivni(test_connection):
    vysledek = pridat_ukol_db(test_connection, "Nakoupit", "Koupit mléko")

    assert vysledek is True

    cursor = test_connection.cursor()
    cursor.execute(
        "SELECT nazev, popis, stav FROM ukoly WHERE nazev = %s",
        ("Nakoupit",)
    )
    ukol = cursor.fetchone()
    cursor.close()

    assert ukol is not None
    assert ukol[0] == "Nakoupit"
    assert ukol[1] == "Koupit mléko"
    assert ukol[2] == "Nezahájeno"


def test_pridat_ukol_negativni(test_connection):
    vysledek = pridat_ukol_db(test_connection, "", "Nějaký popis")

    assert vysledek is False

    cursor = test_connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM ukoly")
    pocet = cursor.fetchone()[0]
    cursor.close()

    assert pocet == 0


def test_aktualizovat_ukol_pozitivni(test_connection):
    pridat_ukol_db(test_connection, "Úkol 1", "Popis 1")

    cursor = test_connection.cursor()
    cursor.execute("SELECT id FROM ukoly WHERE nazev = %s", ("Úkol 1",))
    ukol_id = cursor.fetchone()[0]
    cursor.close()

    vysledek = aktualizovat_ukol_db(test_connection, ukol_id, "Probíhá")
    assert vysledek is True

    cursor = test_connection.cursor()
    cursor.execute("SELECT stav FROM ukoly WHERE id = %s", (ukol_id,))
    stav = cursor.fetchone()[0]
    cursor.close()

    assert stav == "Probíhá"


def test_aktualizovat_ukol_negativni(test_connection):
    vysledek = aktualizovat_ukol_db(test_connection, 99999, "Hotovo")
    assert vysledek is False


def test_odstranit_ukol_pozitivni(test_connection):
    pridat_ukol_db(test_connection, "Smazat", "Tento úkol zmizí")

    cursor = test_connection.cursor()
    cursor.execute("SELECT id FROM ukoly WHERE nazev = %s", ("Smazat",))
    ukol_id = cursor.fetchone()[0]
    cursor.close()

    vysledek = odstranit_ukol_db(test_connection, ukol_id)
    assert vysledek is True

    cursor = test_connection.cursor()
    cursor.execute("SELECT * FROM ukoly WHERE id = %s", (ukol_id,))
    ukol = cursor.fetchone()
    cursor.close()

    assert ukol is None


def test_odstranit_ukol_negativni(test_connection):
    vysledek = odstranit_ukol_db(test_connection, 99999)
    assert vysledek is False