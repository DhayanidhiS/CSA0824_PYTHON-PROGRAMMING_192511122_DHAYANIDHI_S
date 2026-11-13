
from pathlib import Path

# ----------------------------------
# 1. READ ATTENDANCE FILE
# ----------------------------------

def read_attendance(filename):

    records = []

    try:
        with open(filename, "r") as file:

            for line_number, line in enumerate(file, start=1):

                parts = line.strip().split(",")

                if len(parts) != 3:
                    print("Invalid record at line:", line_number)
                    continue

                student_id, date, status = parts
                status = status.strip().upper()

                if not student_id or not date or status not in ("P", "A"):
                    print("Invalid attendance at line:", line_number)
                    continue

                records.append((student_id, date, status))

    except FileNotFoundError:
        print("Attendance file not found.")

    return records


# ----------------------------------
# 2. CALCULATE ATTENDANCE STATISTICS
# ----------------------------------

def calculate_statistics(records):

    statistics = {}

    for student_id, date, status in records:

        if student_id not in statistics:
            statistics[student_id] = [0, 0]

        statistics[student_id][1] += 1

        if status == "P":
            statistics[student_id][0] += 1

    return statistics


# ----------------------------------
# 3. FIND STUDENTS BELOW 75%
# ----------------------------------

def find_below_75(statistics):

    below_students = []

    for student_id, values in statistics.items():

        present = values[0]
        total = values[1]

        percentage = (present / total) * 100

        if percentage < 75:
            below_students.append((student_id, percentage))

    return below_students


# ----------------------------------
# 4. GENERATE ATTENDANCE REPORT
# ----------------------------------

def generate_attendance_report(statistics, filename):

    with open(filename, "w") as file:

        file.write("STUDENT ATTENDANCE REPORT\n")
        file.write("=========================\n\n")

        for student_id, values in sorted(statistics.items()):

            present = values[0]
            total = values[1]

            percentage = (present / total) * 100

            file.write(
                f"Student ID: {student_id}\n"
            )

            file.write(
                f"Present: {present}/{total}\n"
            )

            file.write(
                f"Attendance: {percentage:.2f}%\n\n"
            )


# ----------------------------------
# 5. GENERATE BELOW 75% REPORT
# ----------------------------------

def generate_below_report(students, filename):

    with open(filename, "w") as file:

        file.write("STUDENTS BELOW 75% ATTENDANCE\n")
        file.write("=============================\n\n")

        for student_id, percentage in sorted(students):

            file.write(
                f"{student_id} - {percentage:.2f}%\n"
            )


# ----------------------------------
# 6. MAIN PROGRAM
# ----------------------------------

def main():

    folder = Path(__file__).resolve().parent

    input_file = folder / "attendance.txt"
    attendance_report = folder / "attendance_report.txt"
    below_report = folder / "below_75.txt"

    print("ATTENDANCE MANAGEMENT SYSTEM")
    print("----------------------------")

    # Read attendance records
    records = read_attendance(input_file)

    # Calculate statistics
    statistics = calculate_statistics(records)

    # Find students below 75%
    below_students = find_below_75(statistics)

    # Generate reports
    generate_attendance_report(
        statistics,
        attendance_report
    )

    generate_below_report(
        below_students,
        below_report
    )

    # Display results
    print("\nAttendance processing completed.")

    print("Records processed:", len(records))

    print("Students processed:", len(statistics))

    print("\nAttendance percentages:")

    for student_id, values in sorted(statistics.items()):

        percentage = (values[0] / values[1]) * 100

        print(
            student_id,
            "-",
            f"{percentage:.2f}%"
        )

    print("\nStudents below 75%:")

    for student_id, percentage in sorted(below_students):

        print(
            student_id,
            "-",
            f"{percentage:.2f}%"
        )

    print("\nReports created:")
    print("1. attendance_report.txt")
    print("2. below_75.txt")


# Execute main program
if __name__ == "__main__":
    main()
