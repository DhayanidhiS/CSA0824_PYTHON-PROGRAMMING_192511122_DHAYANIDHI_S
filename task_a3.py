
import csv
from pathlib import Path
import matplotlib.pyplot as plt

# Find the folder containing this Python file
folder = Path(__file__).resolve().parent

input_file = folder / "cleaned_air_quality.csv"

print("AIR QUALITY DATA ANALYSIS AND VISUALISATION")
print("-------------------------------------------")

# STEP 1: READ CLEANED DATA
with open(input_file, "r", newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    records = list(reader)

print("\nSTEP 1: DATA LOADED")
print("Total records:", len(records))

# STEP 2: CALCULATE AVERAGE PM2.5 FOR EACH STATION
station_values = {}

for row in records:
    station = row["station"]
    pm25 = float(row["pm25"])

    if station not in station_values:
        station_values[station] = []

    station_values[station].append(pm25)

station_averages = {}

for station, values in station_values.items():
    station_averages[station] = sum(values) / len(values)

print("\nSTEP 2: AVERAGE PM2.5 BY STATION")

for station, average in station_averages.items():
    print(station, ":", round(average, 2))

# STEP 3: FIND HIGHEST POLLUTION STATION
highest_station = max(
    station_averages,
    key=station_averages.get
)

print("\nSTEP 3: HIGHEST POLLUTION")
print("Station:", highest_station)
print("Average PM2.5:", round(station_averages[highest_station], 2))

# STEP 4: CREATE BAR CHART
plt.figure(figsize=(8, 5))

plt.bar(
    station_averages.keys(),
    station_averages.values()
)

plt.title("Average PM2.5 by Monitoring Station")
plt.xlabel("Monitoring Station")
plt.ylabel("Average PM2.5")
plt.grid(axis="y")

plt.tight_layout()

bar_file = folder / "pm25_bar_chart.png"
plt.savefig(bar_file)

print("\nSTEP 4: BAR CHART CREATED")
print("Saved as:", bar_file.name)

plt.show()

# STEP 5: CREATE LINE GRAPH
plt.figure(figsize=(8, 5))

for station, values in station_values.items():
    plt.plot(
        range(1, len(values) + 1),
        values,
        marker="o",
        label=station
    )

plt.title("PM2.5 Readings by Station")
plt.xlabel("Reading Number")
plt.ylabel("PM2.5 Level")
plt.legend()
plt.grid(True)

plt.tight_layout()

line_file = folder / "pm25_line_chart.png"
plt.savefig(line_file)

print("\nSTEP 5: LINE GRAPH CREATED")
print("Saved as:", line_file.name)

plt.show()

# STEP 6: SAVE ANALYSIS REPORT
report_file = folder / "analysis_report.txt"

with open(report_file, "w", encoding="utf-8") as file:
    file.write("AIR QUALITY ANALYSIS REPORT\n")
    file.write("---------------------------\n")

    for station, average in station_averages.items():
        file.write(
            station + " Average PM2.5: " +
            str(round(average, 2)) + "\n"
        )

    file.write("\nHighest pollution station: " + highest_station)

print("\nSTEP 6: REPORT CREATED")
print("Saved as:", report_file.name)

print("\nTASK A3 COMPLETED SUCCESSFULLY.")
