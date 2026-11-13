
import csv
import time
import cProfile
import pstats
import logging
from pathlib import Path

# Find the folder containing this Python file
folder = Path(__file__).resolve().parent
input_file = folder / "cleaned_air_quality.csv"

# Configure logging
logging.basicConfig(
    filename=folder / "debug_log.txt",
    level=logging.INFO,
    format="%(levelname)s: %(message)s"
)

print("DEBUGGING AND PROFILING AIR QUALITY DATA")
print("----------------------------------------")

# STEP 1: LOAD DATA
print("\nSTEP 1: LOADING DATA")

with open(input_file, "r", newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    records = list(reader)

print("Total records loaded:", len(records))
logging.info("CSV file loaded successfully.")

# STEP 2: DEBUGGING AND VALIDATION
print("\nSTEP 2: DEBUGGING AND VALIDATION")

assert len(records) > 0, "Dataset is empty."

for row in records:
    assert row["station"].strip() != "", "Station name is missing."

    pm25 = float(row["pm25"])
    assert pm25 >= 0, "Invalid PM2.5 value."

print("All records passed validation.")
logging.info("All records passed validation.")

# STEP 3: DEFINE ANALYSIS FUNCTION
def analyse_data(data):
    station_values = {}

    for row in data:
        station = row["station"]
        pm25 = float(row["pm25"])

        if station not in station_values:
            station_values[station] = []

        station_values[station].append(pm25)

    averages = {}

    for station, values in station_values.items():
        averages[station] = sum(values) / len(values)

    return averages


# STEP 4: MEASURE EXECUTION TIME
print("\nSTEP 3: MEASURING EXECUTION TIME")

start_time = time.perf_counter()

averages = analyse_data(records)

end_time = time.perf_counter()

execution_time = end_time - start_time

print("Execution time:", round(execution_time, 6), "seconds")

# Display analysis
print("\nAVERAGE PM2.5 BY STATION")

for station, average in averages.items():
    print(station, ":", round(average, 2))


# STEP 5: PROFILE THE PROGRAM
print("\nSTEP 4: PROFILING THE PROGRAM")

profiler = cProfile.Profile()

profiler.enable()

for i in range(1000):
    analyse_data(records)

profiler.disable()

profile_file = folder / "profiling_report.txt"

with open(profile_file, "w") as file:
    statistics = pstats.Stats(profiler, stream=file)
    statistics.sort_stats("cumulative")
    statistics.print_stats()

print("Profiling report saved as:", profile_file.name)


# STEP 6: SAVE DEBUGGING REPORT
print("\nSTEP 5: SAVING DEBUGGING REPORT")

debug_file = folder / "debugging_report.txt"

with open(debug_file, "w") as file:
    file.write("AIR QUALITY DEBUGGING REPORT\n")
    file.write("----------------------------\n")
    file.write("Total records: " + str(len(records)) + "\n")
    file.write("Validation: Successful\n")
    file.write(
        "Execution time: " +
        str(round(execution_time, 6)) +
        " seconds\n"
    )

    file.write("\nAverage PM2.5 values:\n")

    for station, average in averages.items():
        file.write(
            station + ": " + str(round(average, 2)) + "\n"
        )

print("Debugging report saved as:", debug_file.name)

print("\nTASK A4 COMPLETED SUCCESSFULLY.")
