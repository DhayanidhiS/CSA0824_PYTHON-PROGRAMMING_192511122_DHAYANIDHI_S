
import csv
import sqlite3
import time
from pathlib import Path

folder = Path(__file__).resolve().parent

print("LOOPS VS LIBRARIES VS SQL PERFORMANCE")
print("--------------------------------------")

# STEP 1: GENERATE SAMPLE DATA
print("\nSTEP 1: GENERATING SAMPLE DATA")

data = []

for i in range(10000):
    station = "Station_" + str(i % 10)
    pm25 = (i % 100) + 20

    data.append({
        "station": station,
        "pm25": pm25
    })

print("Total records generated:", len(data))


# STEP 2: PYTHON LOOP METHOD
print("\nSTEP 2: PYTHON LOOP METHOD")

start = time.perf_counter()

loop_result = {}

for row in data:
    station = row["station"]

    if station not in loop_result:
        loop_result[station] = []

    loop_result[station].append(row["pm25"])

loop_average = {}

for station, values in loop_result.items():
    loop_average[station] = sum(values) / len(values)

loop_time = time.perf_counter() - start

print("Stations analysed:", len(loop_average))
print("Execution time:", round(loop_time, 6), "seconds")


# STEP 3: BUILT-IN LIBRARY METHOD
print("\nSTEP 3: BUILT-IN LIBRARY METHOD")

start = time.perf_counter()

library_result = {}

for row in data:
    station = row["station"]

    if station not in library_result:
        library_result[station] = [0, 0]

    library_result[station][0] += row["pm25"]
    library_result[station][1] += 1

library_average = {}

for station, values in library_result.items():
    library_average[station] = values[0] / values[1]

library_time = time.perf_counter() - start

print("Stations analysed:", len(library_average))
print("Execution time:", round(library_time, 6), "seconds")


# STEP 4: SQL METHOD
print("\nSTEP 4: SQL METHOD")

db_file = folder / "b3_database.db"

con = sqlite3.connect(db_file)
cur = con.cursor()

cur.execute("DROP TABLE IF EXISTS readings")

cur.execute("""
CREATE TABLE readings (
    station TEXT,
    pm25 REAL
)
""")

start = time.perf_counter()

cur.executemany(
    "INSERT INTO readings VALUES (?, ?)",
    [(row["station"], row["pm25"]) for row in data]
)

con.commit()

cur.execute("""
SELECT station, AVG(pm25)
FROM readings
GROUP BY station
""")

sql_result = cur.fetchall()

sql_time = time.perf_counter() - start

print("Stations analysed:", len(sql_result))
print("Execution time:", round(sql_time, 6), "seconds")

con.close()


# STEP 5: DISPLAY COMPARISON
print("\nSTEP 5: PERFORMANCE COMPARISON")
print("--------------------------------------")

print("Python Loop Time :", round(loop_time, 6), "seconds")
print("Built-in Library :", round(library_time, 6), "seconds")
print("SQL Method       :", round(sql_time, 6), "seconds")


# STEP 6: DISPLAY RESULTS
print("\nSTEP 6: AVERAGE PM2.5 VALUES")
print("--------------------------------------")

for station in sorted(loop_average):
    print(station, ":", round(loop_average[station], 2))

# STEP 7: SAVE REPORT
report_file = folder / "b3_performance_report.txt"

with open(report_file, "w", encoding="utf-8") as file:
    file.write("PERFORMANCE COMPARISON REPORT\n")
    file.write("-----------------------------\n")
    file.write("Total records: " + str(len(data)) + "\n")
    file.write("Python Loop: " + str(round(loop_time, 6)) + " seconds\n")
    file.write("Built-in Library: " + str(round(library_time, 6)) + " seconds\n")
    file.write("SQL Method: " + str(round(sql_time, 6)) + " seconds\n")

print("\nReport saved:", report_file.name)
print("\nTASK B3 COMPLETED SUCCESSFULLY.")
