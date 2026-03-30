# Vylepšený Task Manager

Konzolová aplikace v Pythonu pro správu úkolů s využitím MySQL databáze.  
Aplikace ukládá úkoly do databáze a umožňuje jejich správu pomocí CRUD operací (Create, Read, Update, Delete).

## Funkce

- přidání úkolu
- zobrazení úkolů (filtr: Nezahájeno, Probíhá)
- aktualizace stavu úkolu
- odstranění úkolu
- textové menu v konzoli

## Struktura projektu

vylepseny_task_manager/
- main.py
- db.py
- task_manager.py
- requirements.txt
- tests/
  - test_task_manager.py

## Použité technologie

- Python
- MySQL
- mysql-connector-python
- pytest
- python-dotenv

## Požadavky

- Python 3.14
- MySQL Server

## Databáze

Projekt používá dvě databáze:

- task_manager_db (hlavní databáze)
- task_manager_test_db (testovací databáze)

Tabulka: ukoly

- id (INT, primární klíč)
- nazev (VARCHAR)
- popis (TEXT)
- stav (ENUM: Nezahájeno, Probíhá, Hotovo)
- datum_vytvoreni (TIMESTAMP)

Databáze i tabulka se při spuštění vytvoří automaticky, pokud ještě neexistují.

## Instalace

Vytvoření virtuálního prostředí:

python -m venv venv

Aktivace prostředí (Windows):

venv\Scripts\activate

Instalace závislostí:

python -m pip install -r requirements.txt

## Spuštění aplikace

python main.py

## Spuštění testů

python -m pytest -v

## Testování

Testy ověřují:

- přidání úkolu (pozitivní a negativní případ)
- aktualizaci úkolu (pozitivní a negativní případ)
- odstranění úkolu (pozitivní a negativní případ)

Testy používají testovací databázi a po každém testu mažou testovací data.

## Konfigurace

Přihlašovací údaje k databázi jsou uložené v souboru .env, který není součástí repozitáře.

Příklad obsahu .env:

DB_HOST=127.0.0.1
DB_USER=root
DB_PASSWORD=tvé_heslo
MAIN_DB_NAME=task_manager_db
TEST_DB_NAME=task_manager_test_db

## Stav projektu

Projekt je funkční a obsahuje automatizované testy. testy.