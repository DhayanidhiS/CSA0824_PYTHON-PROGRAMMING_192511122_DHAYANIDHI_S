
from pathlib import Path

# --------------------------------
# 1. SET FOLDER LOCATION
# --------------------------------

folder_path = Path(r"C:/Users/madhu/OneDrive/Dokumen/d")

# Check whether folder exists
if not folder_path.exists():
    print("Error: Folder not found!")
    print("Expected folder location:", folder_path)
    raise SystemExit

# --------------------------------
# 2. INITIALIZE VARIABLES
# --------------------------------

attendance = {}
files_processed = 0
damaged_records = 0
error_messages = []

file_names = ["day1.txt", "day2.txt", "day3.txt"]

# --------------------------------
# 3. READ ATTENDANCE FILES
# --------------------------------

for filename in file_names:

    file_path = folder_path / filename

    if not file_path.exists():
        print("File not found:", filename)
        error_messages.append(
            f"Missing file: {filename}"
        )
        continue

    files_processed += 1

    try:
        with open(file_path, "r") as file:

            for line_number, line in enumerate(file, start=1):

                line = line.strip()

                if not line:
                    continue

                parts = line.split(",")

                if len(parts) != 2:
                    damaged_records += 1
                    error_messages.append(
                        f"{filename}, line {line_number}: Invalid format"
                    )
                    continue

                student_id = parts[0].strip()
                status = parts[1].strip().upper()

                if not student_id or status not in ["P", "A"]:
                    damaged_records += 1
                    error_messages.append(
                        f"{filename}, line {line_number}: Invalid record"
                    )
                    continue

                if student_id not in attendance:
                    attendance[student_id] = {
                        "present": 0,
                        "total": 0
                    }

                attendance[student_id]["total"] += 1

                if status == "P":
                    attendance[student_id]["present"] += 1

    except OSError as error:
        error_messages.append(
            f"{filename}: {error}"
        )

# --------------------------------
# 4. CREATE ATTENDANCE REPORT
# --------------------------------

report_path = folder_path / "attendance_report.txt"

with open(report_path, "w") as report:

    report.write("STUDENT ATTENDANCE REPORT\n")
    report.write("=========================\n\n")

    for student_id, data in sorted(attendance.items()):

        present = data["present"]
        total = data["total"]

        percentage = (present / total) * 100

        report.write(
            f"Student ID: {student_id}\n"
        )

        report.write(
            f"Present: {present}/{total}\n"
        )

        report.write(
            f"Attendance: {percentage:.2f}%\n\n"
        )

# --------------------------------
# 5. CREATE BELOW 75% REPORT
# --------------------------------

below_path = folder_path / "below_75.txt"

with open(below_path, "w") as report:

    report.write("STUDENTS BELOW 75% ATTENDANCE\n")
    report.write("============================\n\n")

    for student_id, data in sorted(attendance.items()):

        percentage = (
            data["present"] / data["total"]
        ) * 100

        if percentage < 75:

            report.write(
                f"{student_id} - {percentage:.2f}%\n"
            )

# --------------------------------
# 6. CREATE ERROR LOG
# --------------------------------

error_path = folder_path / "attendance_errors.txt"

with open(error_path, "w") as error_file:

    error_file.write("ATTENDANCE ERROR LOG\n")
    error_file.write("===================\n\n")

    if error_messages:

        for message in error_messages:
            error_file.write(message + "\n")

    else:
        error_file.write("No errors found.\n")

# --------------------------------
# 7. DISPLAY FINAL OUTPUT
# --------------------------------

print("\nAttendance processing completed.")

print("Files processed:", files_processed)

print("Students processed:", len(attendance))

print("Damaged records:", damaged_records)

print("Reports created:")
print("1. attendance_report.txt")
print("2. below_75.txt")
print("3. attendance_errors.txt")

print("\nReport folder:", folder_path)
