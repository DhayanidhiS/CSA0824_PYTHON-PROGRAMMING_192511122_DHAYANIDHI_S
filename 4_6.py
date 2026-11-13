
import os
import re
from pathlib import Path

# ---------------------------------------
# 1. SET FOLDER LOCATION
# ---------------------------------------

folder = Path(__file__).resolve().parent

departments = ["CSE", "ECE", "EEE", "MECH", "CIVIL"]

registrations = {}
event_participants = {}
error_records = []

total_records = 0
duplicate_records = 0
invalid_records = 0


# ---------------------------------------
# 2. VALIDATE EMAIL
# ---------------------------------------

def validate_email(email):

    pattern = r"^[\w.-]+@[\w.-]+\.[A-Za-z]{2,}$"

    return re.match(pattern, email) is not None


# ---------------------------------------
# 3. PROCESS DEPARTMENT FILES
# ---------------------------------------

def process_department_files():

    global total_records
    global duplicate_records
    global invalid_records

    for department in departments:

        filename = folder / f"{department}.txt"

        if not filename.exists():

            error_records.append(
                f"{department}.txt: File not found"
            )

            invalid_records += 1
            continue

        with open(filename, "r") as file:

            for line_number, line in enumerate(file, start=1):

                if not line.strip():
                    continue

                total_records += 1

                parts = line.strip().split(",")

                # Check number of fields
                if len(parts) != 5:

                    error_records.append(
                        f"{department}.txt, line {line_number}: Invalid format"
                    )

                    invalid_records += 1
                    continue

                reg_id, name, dept, email, events = [
                    item.strip() for item in parts
                ]

                # Validate student details
                if (
                    not reg_id
                    or not name
                    or dept not in departments
                    or not validate_email(email)
                    or not events
                ):

                    error_records.append(
                        f"{department}.txt, line {line_number}: Invalid student details"
                    )

                    invalid_records += 1
                    continue

                event_list = [
                    event.strip().title()
                    for event in events.split(";")
                    if event.strip()
                ]

                if not event_list:

                    error_records.append(
                        f"{department}.txt, line {line_number}: No valid events"
                    )

                    invalid_records += 1
                    continue

                # Remove duplicate event names
                event_list = list(dict.fromkeys(event_list))

                # Check duplicate registration
                if reg_id in registrations:

                    duplicate_records += 1

                    # Merge new events for existing student
                    for event in event_list:

                        if event not in registrations[reg_id]["events"]:
                            registrations[reg_id]["events"].add(event)

                    continue

                # Store new registration
                registrations[reg_id] = {
                    "name": name,
                    "department": dept,
                    "email": email,
                    "events": set(event_list)
                }


# ---------------------------------------
# 4. ORGANIZE EVENT PARTICIPANTS
# ---------------------------------------

def organize_events():

    for reg_id, details in registrations.items():

        for event in details["events"]:

            if event not in event_participants:
                event_participants[event] = []

            event_participants[event].append(
                (
                    reg_id,
                    details["name"],
                    details["department"],
                    details["email"]
                )
            )


# ---------------------------------------
# 5. CREATE EVENT-WISE FILES
# ---------------------------------------

def create_event_files():

    event_folder = folder / "event_files"

    event_folder.mkdir(exist_ok=True)

    for event, participants in event_participants.items():

        filename = event_folder / f"{event.lower()}.txt"

        with open(filename, "w") as file:

            file.write(f"{event.upper()} PARTICIPANTS\n")
            file.write("====================\n\n")

            for participant in sorted(participants):

                reg_id, name, department, email = participant

                file.write(
                    f"{reg_id},{name},{department},{email}\n"
                )


# ---------------------------------------
# 6. CREATE MASTER REGISTRATION FILE
# ---------------------------------------

def create_master_file():

    filename = folder / "master_registrations.txt"

    with open(filename, "w") as file:

        file.write("MASTER REGISTRATION LIST\n")
        file.write("========================\n\n")

        for reg_id, details in sorted(registrations.items()):

            events = ";".join(sorted(details["events"]))

            file.write(
                f"{reg_id},{details['name']},"
                f"{details['department']},"
                f"{details['email']},{events}\n"
            )


# ---------------------------------------
# 7. GENERATE SUMMARY REPORT
# ---------------------------------------

def generate_summary():

    filename = folder / "summary_report.txt"

    with open(filename, "w") as file:

        file.write("COLLEGE FEST REGISTRATION SUMMARY\n")
        file.write("=================================\n\n")

        file.write(
            f"Total input records: {total_records}\n"
        )

        file.write(
            f"Unique registrations: {len(registrations)}\n"
        )

        file.write(
            f"Duplicate registrations: {duplicate_records}\n"
        )

        file.write(
            f"Invalid or missing records: {invalid_records}\n\n"
        )

        file.write("EVENT-WISE PARTICIPANT COUNT\n")
        file.write("----------------------------\n")

        for event, participants in sorted(event_participants.items()):

            file.write(
                f"{event}: {len(participants)}\n"
            )


# ---------------------------------------
# 8. CREATE ERROR LOG
# ---------------------------------------

def create_error_log():

    filename = folder / "error_log.txt"

    with open(filename, "w") as file:

        file.write("REGISTRATION ERROR LOG\n")
        file.write("======================\n\n")

        if error_records:

            for error in error_records:
                file.write(error + "\n")

        else:
            file.write("No errors found.\n")


# ---------------------------------------
# 9. MAIN PROGRAM
# ---------------------------------------

def main():

    print("COLLEGE FEST REGISTRATION SYSTEM")
    print("--------------------------------")

    # Process all department files
    process_department_files()

    # Organize participants by event
    organize_events()

    # Generate output files
    create_event_files()

    create_master_file()

    generate_summary()

    create_error_log()

    # Display results
    print("\nRegistration processing completed.")

    print("Total input records:", total_records)

    print("Unique registrations:", len(registrations))

    print("Duplicate registrations:", duplicate_records)

    print("Invalid or missing records:", invalid_records)

    print("\nEvent-wise participants:")

    for event, participants in sorted(event_participants.items()):

        print(event, ":", len(participants))

    print("\nFiles created:")

    print("1. master_registrations.txt")
    print("2. summary_report.txt")
    print("3. error_log.txt")
    print("4. event_files folder")


# ---------------------------------------
# 10. EXECUTE PROGRAM
# ---------------------------------------

if __name__ == "__main__":
    main()
