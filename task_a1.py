
import csv
import sqlite3
from pathlib import Path

# Find the folder containing this Python program
folder = Path(__file__).resolve().parent

csv_file = folder / "air_quality.csv"
db_file = folder / "air_quality.db"

# STEP 1: Inspect the CSV file
print("STEP 1: INSPECTING CSV FILE")
print("---------------------------")

with open(csv_file, "r", newline="") as file:
    reader = csv.DictReader(file)

    print("CSV Columns:", reader.fieldnames)

    records = list(reader)

    print("Total records:", len(records))

    for row in records:
        print(row)


# STEP 2: Create SQLite database
print("\nSTEP 2: CREATING DATABASE")
print("-------------------------")

con = sqlite3.connect(db_file)
cur = con.cursor()

cur.execute("PRAGMA foreign_keys = ON")

cur.execute("""
CREATE TABLE IF NOT EXISTS stations (
    station_id INTEGER PRIMARY KEY,
    station_name TEXT UNIQUE,
    temperature_unit TEXT
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS readings (
    reading_id INTEGER PRIMARY KEY,
    station_id INTEGER,
    reading_date TEXT,
    reading_hour TEXT,
    pm25 REAL,
    pm10 REAL,
    no2 REAL,
    temperature REAL,
    FOREIGN KEY (station_id)
        REFERENCES stations(station_id)
)
""")

print("Database and tables created successfully.")


# STEP 3: Insert station information
print("\nSTEP 3: INSERTING STATIONS")
print("--------------------------")

stations = sorted(set(row["station"] for row in records))

for station in stations:
    cur.execute("""
        INSERT OR IGNORE INTO stations
        (station_name, temperature_unit)
        VALUES (?, ?)
    """, (station, "C"))

print("Stations inserted:", stations)


# STEP 4: Insert readings
print("\nSTEP 4: INSERTING READINGS")
print("--------------------------")

for row in records:
    cur.execute("""
        SELECT station_id
        FROM stations
        WHERE station_name = ?
    """, (row["station"],))

    station_id = cur.fetchone()[0]

    cur.execute("""
        INSERT INTO readings
        (station_id, reading_date, reading_hour,
         pm25, pm10, no2, temperature)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        station_id,
        row["date"],
        row["hour"],
        float(row["pm25"]),
        float(row["pm10"]),
        float(row["no2"]),
        float(row["temperature"])
    ))

con.commit()

print("Readings inserted successfully.")


# STEP 5: Average PM2.5 at Adyar
print("\nSTEP 5: AVERAGE PM2.5 AT ADYAR")
print("------------------------------")

cur.execute("""
SELECT AVG(r.pm25)
FROM readings r
JOIN stations s
ON r.station_id = s.station_id
WHERE s.station_name = 'Adyar'
AND r.reading_date LIKE '2026-10%'
""")

print("Average PM2.5:", round(cur.fetchone()[0], 2))


# STEP 6: Highest PM2.5 by station
print("\nSTEP 6: HIGHEST PM2.5 BY STATION")
print("--------------------------------")

cur.execute("""
SELECT s.station_name, MAX(r.pm25)
FROM readings r
JOIN stations s
ON r.station_id = s.station_id
GROUP BY s.station_name
ORDER BY MAX(r.pm25) DESC
""")

for row in cur.fetchall():
    print(row)


# STEP 7: Daily average PM2.5
print("\nSTEP 7: DAILY AVERAGE PM2.5")
print("---------------------------")

cur.execute("""
SELECT reading_date, AVG(pm25)
FROM readings
GROUP BY reading_date
ORDER BY reading_date
""")

for row in cur.fetchall():
    print(row)


# STEP 8: Display database tables
print("\nSTEP 8: DATABASE COMPLETED")
print("--------------------------")

print("Database file:", db_file.name)

con.close()

print("Task A1 completed successfully.")
