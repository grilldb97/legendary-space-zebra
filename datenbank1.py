import sqlite3
verbindung = sqlite3.connect("datenbank1.db")
zeiger = verbindung.cursor()

sql_anweisung = """
CREATE TABLE IF NOT EXISTS personen (
vorname VARCHAR(20),
nachname VARCHAR(20),
geburtstag DATE
);"""

zeiger.execute(sql_anweisung)

verbindung.commit()
verbindung.close()