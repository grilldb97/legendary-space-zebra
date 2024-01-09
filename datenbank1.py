import sqlite3

verbindung = sqlite3.connect("datenbank1.db")
zeiger = verbindung.cursor()

nachname = input("Nachname: ")
vorname = input("Vorname: ")
geburtstag = input("Geburtstag: ")

sql_anweisung = """
CREATE TABLE IF NOT EXISTS personen (
vorname VARCHAR(20),
nachname VARCHAR(20),
geburtstag DATE
);"""

zeiger.execute("""
                INSERT INTO personen 
                       VALUES (?,?,?)
               """,
               (vorname, nachname, geburtstag)
               )
zeiger.execute("SELECT * FROM personen")
inhalt = zeiger.fetchall()

for x in inhalt:
    print(x, "\n")

verbindung.commit()
verbindung.close()
