import pytest

from task_manager import (
    pridat_ukol_db,
    aktualizovat_ukol_db,
    odstranit_ukol_db
)


@pytest.mark.parametrize(
    "nazev, popis",
    [
        ("", "něco"),        # prázdný název
        ("něco", ""),        # prázdný popis
    ]
)
def test_pridat_ukol_negativni(test_connection, nazev, popis):
    vysledek = pridat_ukol_db(test_connection, nazev, popis)
    assert vysledek is False


def test_pridat_ukol_pozitivni(test_connection):
    vysledek = pridat_ukol_db(test_connection, "Test", "Popis")
    assert vysledek is True


def test_aktualizovat_ukol_pozitivni(test_connection):
    pridat_ukol_db(test_connection, "Test", "Popis")

    cursor = test_connection.cursor()
    cursor.execute("SELECT id FROM ukoly WHERE nazev = %s", ("Test",))
    ukol_id = cursor.fetchone()[0]
    cursor.close()

    vysledek = aktualizovat_ukol_db(test_connection, ukol_id, "Probíhá")
    assert vysledek is True


def test_aktualizovat_ukol_neexistujici_id(test_connection):
    vysledek = aktualizovat_ukol_db(test_connection, 99999, "Hotovo")
    assert vysledek is False


def test_aktualizovat_ukol_neplatny_stav(test_connection):
    pridat_ukol_db(test_connection, "Test", "Popis")

    cursor = test_connection.cursor()
    cursor.execute("SELECT id FROM ukoly WHERE nazev = %s", ("Test",))
    ukol_id = cursor.fetchone()[0]
    cursor.close()

    vysledek = aktualizovat_ukol_db(test_connection, ukol_id, "Blbost")
    assert vysledek is False


def test_odstranit_ukol_pozitivni(test_connection):
    pridat_ukol_db(test_connection, "Test", "Popis")

    cursor = test_connection.cursor()
    cursor.execute("SELECT id FROM ukoly WHERE nazev = %s", ("Test",))
    ukol_id = cursor.fetchone()[0]
    cursor.close()

    vysledek = odstranit_ukol_db(test_connection, ukol_id)
    assert vysledek is True


def test_odstranit_ukol_negativni(test_connection):
    vysledek = odstranit_ukol_db(test_connection, 99999)
    assert vysledek is False