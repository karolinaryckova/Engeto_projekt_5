import mysql.connector
from mysql.connector import Error


def pripojeni_db(database="task_manager_db"):
    """
    Vytvoří připojení k MySQL databázi.
    """
    try:
        connection = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="#G1ng3r89",
            database=database
        )

        if connection.is_connected():
            return connection

    except Error as e:
        print(f"❌ Chyba při připojení k databázi: {e}")
        return None


def vytvoreni_tabulky(connection):
    """
    Vytvoří tabulku ukoly, pokud ještě neexistuje.
    """
    if connection is None:
        print("❌ Není dostupné připojení k databázi.")
        return

    query = """
    CREATE TABLE IF NOT EXISTS ukoly (
        id INT AUTO_INCREMENT PRIMARY KEY,
        nazev VARCHAR(255) NOT NULL,
        popis TEXT NOT NULL,
        stav ENUM('Nezahájeno', 'Probíhá', 'Hotovo') NOT NULL DEFAULT 'Nezahájeno',
        datum_vytvoreni TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """

    try:
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
        cursor.close()
    except Error as e:
        print(f"❌ Chyba při vytváření tabulky: {e}")
        