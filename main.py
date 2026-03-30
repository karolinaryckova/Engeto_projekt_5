from db import pripojeni_db, vytvoreni_tabulky
from task_manager import (
    pridat_ukol,
    zobrazit_ukoly,
    aktualizovat_ukol,
    odstranit_ukol
)


def hlavni_menu(connection):
    """
    Zobrazí hlavní menu programu a umožní uživateli vybrat akci.
    """
    while True:
        print("\n--- SPRÁVCE ÚKOLŮ ---")
        print("1. Přidat úkol")
        print("2. Zobrazit úkoly")
        print("3. Aktualizovat úkol")
        print("4. Odstranit úkol")
        print("5. Ukončit program")

        volba = input("Vyber možnost: ").strip()

        if volba == "1":
            pridat_ukol(connection)
        elif volba == "2":
            zobrazit_ukoly(connection)
        elif volba == "3":
            aktualizovat_ukol(connection)
        elif volba == "4":
            odstranit_ukol(connection)
        elif volba == "5":
            print("👋 Program byl ukončen.")
            break
        else:
            print("❌ Neplatná volba, zkus to znovu.")


def main():
    connection = pripojeni_db()

    if connection:
        print("✅ Připojení k databázi bylo úspěšné.")
        vytvoreni_tabulky(connection)
        hlavni_menu(connection)
        connection.close()
        print("Připojení bylo ukončeno.")


if __name__ == "__main__":
    main()