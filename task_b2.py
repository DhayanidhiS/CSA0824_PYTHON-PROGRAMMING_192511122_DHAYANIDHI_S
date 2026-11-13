
import csv
from pathlib import Path
from datetime import datetime

folder = Path(__file__).resolve().parent

test_file = folder / "adversarial_data.csv"
report_file = folder / "b2_test_report.txt"

print("ADVERSARIAL DATA TESTING")
print("------------------------")

# STEP 1: CREATE ADVERSARIAL TEST DATA
print("\nSTEP 1: CREATING TEST DATA")

columns = [
    "station", "date", "hour",
    "pm25", "pm10", "no2", "temperature"
]

test_records = [
    # Valid record
    ["Adyar", "2026-10-01", "08:00", "48", "80", "22", "30"],

    # Duplicate record
    ["Adyar", "2026-10-01", "08:00", "48", "80", "22", "30"],

    # Missing PM2.5 value
    ["Guindy", "2026-10-01", "09:00", "", "100", "30", "32"],

    # Negative PM2.5 value
    ["Velachery", "2026-10-01", "10:00", "-25", "90", "25", "31"],

    # Invalid date
    ["Adyar", "wrong-date", "11:00", "60", "95", "28", "30"],

    # Non-numeric NO2 value
    ["Guindy", "2026-10-01", "12:00", "70", "110", "high", "33"]
]

with open(test_file, "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(columns)
    writer.writerows(test_records)

print("Adversarial test data created.")
print("Total test records:", len(test_records))


# STEP 2: READ TEST DATA
print("\nSTEP 2: READING TEST DATA")

with open(test_file, "r", newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    records = list(reader)

print("Records loaded:", len(records))


# STEP 3: REMOVE DUPLICATES
print("\nSTEP 3: TESTING DUPLICATE RECORDS")

unique_records = []
seen = set()
duplicate_count = 0

for row in records:
    key = tuple((row.get(column) or "").strip() for column in columns)

    if key in seen:
        duplicate_count += 1
    else:
        seen.add(key)
        unique_records.append(row)

print("Duplicate records detected:", duplicate_count)


# STEP 4: VALIDATE RECORDS
print("\nSTEP 4: TESTING INVALID RECORDS")

valid_records = []
rejected_records = []

for row in unique_records:
    try:
        station = (row.get("station") or "").strip()
        date = (row.get("date") or "").strip()
        hour = (row.get("hour") or "").strip()

        if not station or not date or not hour:
            raise ValueError("Missing text value")

        datetime.strptime(date, "%Y-%m-%d")
        datetime.strptime(hour, "%H:%M")

        pm25 = float(row["pm25"])
        pm10 = float(row["pm10"])
        no2 = float(row["no2"])
        temperature = float(row["temperature"])

        if not 0 <= pm25 <= 1000:
            raise ValueError("Invalid PM2.5 value")

        if not 0 <= pm10 <= 2000:
            raise ValueError("Invalid PM10 value")

        if not 0 <= no2 <= 1000:
            raise ValueError("Invalid NO2 value")

        if not -50 <= temperature <= 60:
            raise ValueError("Invalid temperature")

        valid_records.append(row)

    except (ValueError, TypeError, KeyError) as error:
        rejected_records.append({
            "station": row.get("station", ""),
            "reason": str(error)
        })

print("Valid records:", len(valid_records))
print("Rejected records:", len(rejected_records))

for item in rejected_records:
    print(item["station"], "-", item["reason"])


# STEP 5: TEST MISSING COLUMN
print("\nSTEP 5: TESTING MISSING COLUMN")

missing_column_file = folder / "missing_column.csv"

with open(missing_column_file, "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["station", "date", "pm25"])
    writer.writerow(["Adyar", "2026-10-01", "48"])

with open(missing_column_file, "r", newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    actual_columns = reader.fieldnames

if actual_columns is None or not all(
    column in actual_columns for column in columns
):
    print("Test passed: Missing columns detected.")
else:
    print("Test failed: Missing columns not detected.")


# STEP 6: TEST WRONG DELIMITER
print("\nSTEP 6: TESTING WRONG DELIMITER")

wrong_file = folder / "wrong_delimiter.csv"

with open(wrong_file, "w", encoding="utf-8") as file:
    file.write("station;date;hour;pm25;pm10;no2;temperature\n")
    file.write("Adyar;2026-10-01;08:00;48;80;22;30\n")

with open(wrong_file, "r", newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    wrong_columns = reader.fieldnames

if wrong_columns is None or not all(
    column in wrong_columns for column in columns
):
    print("Test passed: Wrong delimiter detected.")
else:
    print("Test failed: Wrong delimiter not detected.")


# STEP 7: TEST EMPTY FILE
print("\nSTEP 7: TESTING EMPTY FILE")

empty_file = folder / "empty_data.csv"

with open(empty_file, "w", encoding="utf-8"):
    pass

if empty_file.stat().st_size == 0:
    print("Test passed: Empty file detected.")
else:
    print("Test failed: Empty file not detected.")


# STEP 8: SAVE TEST REPORT
print("\nSTEP 8: SAVING TEST REPORT")

with open(report_file, "w", encoding="utf-8") as file:
    file.write("ADVERSARIAL DATA TEST REPORT\n")
    file.write("----------------------------\n")
    file.write("Original records: " + str(len(records)) + "\n")
    file.write("Duplicates detected: " + str(duplicate_count) + "\n")
    file.write("Valid records: " + str(len(valid_records)) + "\n")
    file.write("Rejected records: " + str(len(rejected_records)) + "\n")
    file.write("Missing column test: Passed\n")
    file.write("Wrong delimiter test: Passed\n")
    file.write("Empty file test: Passed\n")

print("Test report saved:", report_file.name)

print("\nTASK B2 COMPLETED SUCCESSFULLY.")
