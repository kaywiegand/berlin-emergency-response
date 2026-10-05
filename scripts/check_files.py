import os
import duckdb

# Required files relative to project root
REQUIRED_FILES = [
    "data/berlin_emergency.duckdb",
    "models/staging/sources.yml",
    "models/staging/stg_missions_daily.sql",
    "models/intermediate/int_missions_daily_enhanced.sql",
    "models/marts/fct_missions_daily.sql",
]

print("=== 1. DATEI- UND ORDNER-CHECK ===")
all_files_ok = True
for filepath in REQUIRED_FILES:
    exists = os.path.exists(filepath)
    if exists:
        size = os.path.getsize(filepath)
        status = f"OK ({size} bytes)" if size > 0 else "FEHLER: Datei ist LEER!"
        if size == 0:
            all_files_ok = False
    else:
        status = "FEHLER: Datei FEHLT!"
        all_files_ok = False
    print(f"[{'✓' if exists and size > 0 else 'X'}] {filepath} -> {status}")

print("\n=== 2. DUCKDB ROHDATEN-CHECK ===")
db_path = "data/berlin_emergency.duckdb"
if os.path.exists(db_path):
    try:
        con = duckdb.connect(db_path, read_only=True)
        
        # Available tables
        tables = con.sql("SHOW TABLES").fetchall()
        table_names = [t[0] for t in tables]
        print(f"Gefundene Tabellen/Views in DuckDB: {table_names}")

        # Check raw columns if raw table exists
        if "raw_missions_daily" in table_names:
            columns = con.sql("DESCRIBE raw_missions_daily").df()
            print("\nSpalten in 'raw_missions_daily':")
            for _, row in columns.iterrows():
                print(f"  - {row['column_name']} ({row['column_type']})")
        else:
            print("\n[!] 'raw_missions_daily' nicht in DuckDB gefunden.")
            all_files_ok = False
            
        con.close()
    except Exception as e:
        print(f"Fehler beim Verbinden mit DuckDB: {e}")
        all_files_ok = False
else:
    print("DuckDB-Datei existiert nicht. Abbruch der Datenbank-Prüfung.")

print("\n===============================")
if all_files_ok:
    print("FAZIT: Alle Dateien liegen richtig und enthalten Daten! Wir können jetzt die SQL-Spalten abgleichen.")
else:
    print("FAZIT: Es fehlen Dateien oder eine Datei ist leer. Bitte die Rot markierten Punkte korrigieren.")