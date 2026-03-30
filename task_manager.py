from mysql.connector import Error


def pridat_ukol_db(connection, nazev, popis):
    """
    Přidá nový úkol do databáze.
    Vrací True při úspěchu, jinak False.
    """
    nazev = nazev.strip()
    popis = popis.strip()

    if not nazev or not popis:
        return False

    query = """
    INSERT INTO ukoly (nazev, popis)
    VALUES (%s, %s)
    """

    try:
        cursor = connection.cursor()
        cursor.execute(query, (nazev, popis))
        connection.commit()
        cursor.close()
        return True
    except Error as e:
        print(f"❌ Chyba při přidávání úkolu: {e}")
        return False


def pridat_ukol(connection):
    """
    Načte údaje od uživatele a přidá úkol.
    """
    nazev = input("Zadej název úkolu: ")
    popis = input("Zadej popis úkolu: ")

    if pridat_ukol_db(connection, nazev, popis):
        print("✅ Úkol byl úspěšně přidán.")
    else:
        print("❌ Název i popis jsou povinné.")


def zobrazit_ukoly(connection):
    """
    Zobrazí úkoly se stavem Nezahájeno nebo Probíhá.
    """
    query = """
    SELECT id, nazev, popis, stav
    FROM ukoly
    WHERE stav IN ('Nezahájeno', 'Probíhá')
    ORDER BY id
    """

    try:
        cursor = connection.cursor()
        cursor.execute(query)
        ukoly = cursor.fetchall()
        cursor.close()

        if not ukoly:
            print("📭 Seznam úkolů je prázdný.")
            return

        print("\n--- SEZNAM ÚKOLŮ ---")
        for ukol in ukoly:
            print(
                f"ID: {ukol[0]} | Název: {ukol[1]} | "
                f"Popis: {ukol[2]} | Stav: {ukol[3]}"
            )

    except Error as e:
        print(f"❌ Chyba při zobrazování úkolů: {e}")


def zobraz_vsechny_ukoly(connection):
    """
    Zobrazí všechny úkoly bez filtru.
    """
    query = """
    SELECT id, nazev, popis, stav
    FROM ukoly
    ORDER BY id
    """

    try:
        cursor = connection.cursor()
        cursor.execute(query)
        ukoly = cursor.fetchall()
        cursor.close()

        if not ukoly:
            print("📭 Seznam úkolů je prázdný.")
            return

        print("\n--- VŠECHNY ÚKOLY ---")
        for ukol in ukoly:
            print(
                f"ID: {ukol[0]} | Název: {ukol[1]} | "
                f"Popis: {ukol[2]} | Stav: {ukol[3]}"
            )

    except Error as e:
        print(f"❌ Chyba při zobrazování úkolů: {e}")


def aktualizovat_ukol_db(connection, ukol_id, novy_stav):
    """
    Aktualizuje stav úkolu podle ID.
    Vrací True při úspěchu, jinak False.
    """
    povolene_stavy = ["Probíhá", "Hotovo"]

    if novy_stav not in povolene_stavy:
        return False

    try:
        cursor = connection.cursor()
        cursor.execute("SELECT id FROM ukoly WHERE id = %s", (ukol_id,))
        existuje = cursor.fetchone()

        if not existuje:
            cursor.close()
            return False

        cursor.execute(
            "UPDATE ukoly SET stav = %s WHERE id = %s",
            (novy_stav, ukol_id)
        )
        connection.commit()
        cursor.close()
        return True

    except Error as e:
        print(f"❌ Chyba při aktualizaci úkolu: {e}")
        return False


def aktualizovat_ukol(connection):
    """
    Načte od uživatele ID a nový stav a provede aktualizaci.
    """
    zobraz_vsechny_ukoly(connection)

    try:
        ukol_id = int(input("\nZadej ID úkolu, který chceš aktualizovat: "))
    except ValueError:
        print("❌ ID musí být číslo.")
        return

    print("\nVyber nový stav:")
    print("1. Probíhá")
    print("2. Hotovo")

    volba = input("Tvoje volba: ").strip()

    if volba == "1":
        novy_stav = "Probíhá"
    elif volba == "2":
        novy_stav = "Hotovo"
    else:
        print("❌ Neplatná volba stavu.")
        return

    if aktualizovat_ukol_db(connection, ukol_id, novy_stav):
        print("✅ Stav úkolu byl úspěšně aktualizován.")
    else:
        print("❌ Úkol s tímto ID neexistuje nebo byl zadán neplatný stav.")


def odstranit_ukol_db(connection, ukol_id):
    """
    Odstraní úkol podle ID.
    Vrací True při úspěchu, jinak False.
    """
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT id FROM ukoly WHERE id = %s", (ukol_id,))
        existuje = cursor.fetchone()

        if not existuje:
            cursor.close()
            return False

        cursor.execute("DELETE FROM ukoly WHERE id = %s", (ukol_id,))
        connection.commit()
        cursor.close()
        return True

    except Error as e:
        print(f"❌ Chyba při odstraňování úkolu: {e}")
        return False


def odstranit_ukol(connection):
    """
    Načte od uživatele ID a odstraní úkol.
    """
    zobraz_vsechny_ukoly(connection)

    try:
        ukol_id = int(input("\nZadej ID úkolu, který chceš odstranit: "))
    except ValueError:
        print("❌ ID musí být číslo.")
        return

    potvrzeni = input("Opravdu chceš tento úkol smazat? (ano/ne): ").strip().lower()

    if potvrzeni != "ano":
        print("Mazání bylo zrušeno.")
        return

    if odstranit_ukol_db(connection, ukol_id):
        print("✅ Úkol byl úspěšně odstraněn.")
    else:
        print("❌ Úkol s tímto ID neexistuje.")