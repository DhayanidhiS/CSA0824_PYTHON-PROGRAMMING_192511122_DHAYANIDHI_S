
import csv
from pathlib import Path
from datetime import datetime

# Find the folder containing this Python file
folder = Path(__file__).resolve().parent

input_file = folder / "air_quality.csv"
cleaned_file = folder / "b1_cleaned_data.csv"
rejected_file = folder / "b1_rejected_data.csv"

print("DATA CLEANING AND VALIDATION PIPELINE")
print("-------------------------------------")

required_columns = [
    "station", "date", "hour",
    "pm25", "pm10", "no2", "temperature"
]

# STEP 1: READ THE ORIGINAL DATA
print("\nSTEP 1: READING ORIGINAL DATA")

with open(input_file, "r", newline="", encoding="utf-8-sig") as file:
    reader = csv.DictReader(file)

    if reader.fieldnames is None or not all(
        column in reader.fieldnames for column in required_columns
    ):
        raise ValueError("CSV file has missing or incorrect column names.")

    records = list(reader)

print("Total records:", len(records))

# STEP 2: REMOVE DUPLICATE RECORDS
print("\nSTEP 2: REMOVING DUPLICATES")

unique_records = []
seen = set()
duplicate_count = 0

for row in records:
    key = tuple(
        (row.get(column) or "").strip()
        for column in required_columns
    )

    if key in seen:
        duplicate_count += 1
    else:
        seen.add(key)
        unique_records.append(row)

print("Duplicate records removed:", duplicate_count)

# STEP 3: VALIDATE AND CLEAN DATA
print("\nSTEP 3: VALIDATING DATA")

cleaned_records = []
rejected_records = []

for row in unique_records:
    try:
        station = (row.get("station") or "").strip()
        date = (row.get("date") or "").strip()
        hour = (row.get("hour") or "").strip()

        # Check missing values
        if not station or not date or not hour:
            raise ValueError("Missing station, date or hour")

        # Validate date and time formats
        datetime.strptime(date, "%Y-%m-%d")
        datetime.strptime(hour, "%H:%M")

        # Convert numerical values
        pm25 = float(row["pm25"])
        pm10 = float(row["pm10"])
        no2 = float(row["no2"])
        temperature = float(row["temperature"])

        # Check numerical ranges
        if not 0 <= pm25 <= 1000:
            raise ValueError("Invalid PM2.5 value")

        if not 0 <= pm10 <= 2000:
            raise ValueError("Invalid PM10 value")

        if not 0 <= no2 <= 1000:
            raise ValueError("Invalid NO2 value")

        if not -50 <= temperature <= 60:
            raise ValueError("Invalid temperature")

        cleaned_records.append({
            "station": station,
            "date": date,
            "hour": hour,
            "pm25": pm25,
            "pm10": pm10,
            "no2": no2,
            "temperature": temperature
        })

    except (ValueError, TypeError, KeyError) as error:
        rejected_records.append({
            "station": row.get("station", ""),
            "date": row.get("date", ""),
            "hour": row.get("hour", ""),
            "pm25": row.get("pm25", ""),
            "pm10": row.get("pm10", ""),
            "no2": row.get("no2", ""),
            "temperature": row.get("temperature", ""),
            "reason": str(error)
        })

print("Valid records:", len(cleaned_records))
print("Rejected records:", len(rejected_records))

# STEP 4: NORMALISE NUMERICAL VALUES
print("\nSTEP 4: NORMALISING DATA")

numeric_columns = ["pm25", "pm10", "no2", "temperature"]

for column in numeric_columns:
    values = [row[column] for row in cleaned_records]

    if values:
        minimum = min(values)
        maximum = max(values)

        for row in cleaned_records:
            if maximum == minimum:
                normalised_value = 0.0
            else:
                normalised_value = (
                    (row[column] - minimum) / (maximum - minimum)
                )

            row[column + "_normalised"] = round(
                normalised_value, 3
            )

print("Min-Max normalisation completed.")

# STEP 5: SAVE CLEANED DATA
print("\nSTEP 5: SAVING CLEANED DATA")

cleaned_columns = required_columns + [
    "pm25_normalised",
    "pm10_normalised",
    "no2_normalised",
    "temperature_normalised"
]

with open(cleaned_file, "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=cleaned_columns)
    writer.writeheader()
    writer.writerows(cleaned_records)

print("Cleaned data saved:", cleaned_file.name)

# STEP 6: SAVE REJECTED DATA
rejected_columns = required_columns + ["reason"]

with open(rejected_file, "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=rejected_columns)
    writer.writeheader()
    writer.writerows(rejected_records)

print("Rejected data saved:", rejected_file.name)

# STEP 7: DISPLAY FINAL SUMMARY
print("\nFINAL CLEANING SUMMARY")
print("-------------------------------------")
print("Original records:", len(records))
print("Duplicate records:", duplicate_count)
print("Valid records:", len(cleaned_records))
print("Rejected records:", len(rejected_records))

print("\nTASK B1 COMPLETED SUCCESSFULLY.")
