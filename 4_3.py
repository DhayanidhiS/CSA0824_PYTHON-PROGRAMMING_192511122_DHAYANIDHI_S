
import os
import tempfile

# Custom exception
class InvalidRecord(Exception):
    pass


# Validate one attendance line
def parse_line(line):
    parts = line.strip().split(",")

    if len(parts) != 3:
        raise InvalidRecord(
            f"Expected 3 fields, found {len(parts)}"
        )

    reg_no, date, status = parts

    if not reg_no or not date:
        raise InvalidRecord(
            "Register number or date is empty"
        )

    if status not in ("P", "A"):
        raise InvalidRecord(
            f"Invalid status '{status}'"
        )

    return reg_no, date, status


# Process attendance file
def summarise(path):

    present = 0
    absent = 0
    errors = []

    try:
        with open(path, "r", encoding="utf-8") as file:

            for line_number, line in enumerate(file, start=1):

                if not line.strip():
                    continue

                try:
                    reg_no, date, status = parse_line(line)

                    if status == "P":
                        present += 1
                    else:
                        absent += 1

                except InvalidRecord as error:
                    errors.append(
                        (line_number, str(error))
                    )

    except FileNotFoundError as error:
        raise RuntimeError(
            f"Attendance file not found: {path}"
        ) from error

    except PermissionError as error:
        raise RuntimeError(
            f"Permission denied: {path}"
        ) from error

    except UnicodeDecodeError as error:
        raise RuntimeError(
            f"File encoding error: {path}"
        ) from error

    else:
        print("File processing completed successfully.")

    finally:
        print("File processing attempt finished.")

    return present, absent, errors


# Create a temporary attendance file
data = (
    "192311001,2026-10-08,P\n"
    "192311002,2026-10-08,A\n"
    "192311003,2026-10-08\n"
    "192311004,2026-10-08,L\n"
)

# Write sample data into temporary file
with tempfile.NamedTemporaryFile(
    mode="w",
    suffix=".csv",
    delete=False,
    encoding="utf-8"
) as tmp:

    tmp.write(data)
    filename = tmp.name


# Execute the program
try:
    result = summarise(filename)
    print("Attendance Summary:", result)

except RuntimeError as error:
    print("Error:", error)

finally:
    if os.path.exists(filename):
        os.remove(filename)


# Test missing file
print("\nMissing file test:")

try:
    summarise("missing_attendance.csv")

except RuntimeError as error:
    print(error)
    print(
        "Original cause:",
        type(error.__cause__).__name__
    )
