
import csv
from pathlib import Path

# Find the folder containing this Python file
folder = Path(__file__).resolve().parent

input_file = folder / "air_quality.csv"
output_file = folder / "cleaned_air_quality.csv"

print("AIR QUALITY DATA CLEANING AND NORMALISATION")
print("-------------------------------------------")

# Required columns
required_columns = [
    "station", "date", "hour",
    "pm25", "pm10", "no2", "temperature"
]

# Read CSV file
with open(input_file, "r", newline="", encoding="utf-8-sig") as file:
    reader = csv.DictReader(file)
    records = list(reader)

print("\nSTEP 1: ORIGINAL DATA")
print("Total records:", len(records))

# Check required columns
if reader.fieldnames is None or not all(
    column in reader.fieldnames for column in required_columns
):
    raise ValueError("CSV file does not contain the required columns.")

# STEP 2: REMOVE DUPLICATE RECORDS
unique_records = []
seen = set()

for row in records:
    key = tuple(row.get(column, "") for column in required_columns)

    if key not in seen:
        seen.add(key)
        unique_records.append(row)

print("\nSTEP 2: DUPLICATE REMOVAL")
print("Records after duplicate removal:", len(unique_records))

# STEP 3: HANDLE MISSING AND INVALID VALUES
cleaned_records = []
damaged_records = 0

for row in unique_records:
    try:
        # Check missing text values
        if not row["station"].strip():
            raise ValueError("Missing station")

        if not row["date"].strip() or not row["hour"].strip():
            raise ValueError("Missing date or hour")

        # Convert numeric columns
        pm25 = float(row["pm25"])
        pm10 = float(row["pm10"])
        no2 = float(row["no2"])
        temperature = float(row["temperature"])

        # Validate values
        if pm25 < 0 or pm10 < 0 or no2 < 0:
            raise ValueError("Negative pollution value")

        if not -50 <= temperature <= 60:
            raise ValueError("Invalid temperature")

        cleaned_records.append({
            "station": row["station"].strip(),
            "date": row["date"].strip(),
            "hour": row["hour"].strip(),
            "pm25": pm25,
            "pm10": pm10,
            "no2": no2,
            "temperature": temperature
        })

    except (ValueError, TypeError, KeyError):
        damaged_records += 1

print("\nSTEP 3: DATA VALIDATION")
print("Valid records:", len(cleaned_records))
print("Damaged records:", damaged_records)

# STEP 4: MIN-MAX NORMALISATION
numeric_columns = ["pm25", "pm10", "no2", "temperature"]

for column in numeric_columns:
    values = [row[column] for row in cleaned_records]

    if values:
        minimum = min(values)
        maximum = max(values)

        for row in cleaned_records:
            if maximum == minimum:
                row[column + "_normalised"] = 0.0
            else:
                row[column + "_normalised"] = round(
                    (row[column] - minimum) / (maximum - minimum), 3
                )

print("\nSTEP 4: MIN-MAX NORMALISATION")
print("Normalised values are between 0 and 1.")

# STEP 5: SAVE CLEANED DATA
fieldnames = required_columns + [
    "pm25_normalised",
    "pm10_normalised",
    "no2_normalised",
    "temperature_normalised"
]

with open(output_file, "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(cleaned_records)

print("\nSTEP 5: CLEANED DATA SAVED")
print("Output file:", output_file.name)

# STEP 6: DISPLAY RESULTS
print("\nCLEANED DATA")
print("-------------------------------------------")

for row in cleaned_records:
    print(
        row["station"],
        "PM2.5:", row["pm25"],
        "Normalised:", row["pm25_normalised"]
    )

