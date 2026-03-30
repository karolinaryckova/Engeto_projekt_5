import os

import mysql.connector
from dotenv import load_dotenv
from mysql.connector import Error

load_dotenv()


DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
MAIN_DB_NAME = os.getenv("MAIN_DB_NAME", "task_manager_db")
TEST_DB_NAME = os.getenv("TEST_DB_NAME", "task_manager_test_db")


def vytvoreni_databaze(database: str = MAIN_DB_NAME) -> bool:
    """
    Vytvoří databázi, pokud ještě neexistuje.
    Připojuje se nejdříve bez výběru konkrétní databáze.
    """
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cursor = connection.cursor()
        cursor.execute(
            f"CREATE DATABASE IF NOT EXISTS `{database}` "
            "DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_czech_ci"
        )
        connection.commit()
        cursor.close()
        connection.close()
        return True
    except Error as e:
        print(f"Chyba při vytváření databáze: {e}")
        return False


def pripojeni_db(database: str = MAIN_DB_NAME):
    """
    Vytvoří připojení k MySQL databázi.
    Pokud databáze neexistuje, nejdříve ji vytvoří.
    """
    if not vytvoreni_databaze(database):
        return None

    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=database
        )
        return connection
    except Error as e:
        print(f"Chyba při připojení k databázi: {e}")
        return None


def vytvoreni_tabulky(connection) -> None:
    """
    Vytvoří tabulku ukoly, pokud ještě neexistuje.
    """
    if connection is None:
        print("Není dostupné připojení k databázi.")
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
        print(f"Chyba při vytváření tabulky: {e}")
    