
import os

# ---------------------------------------
# 1. SET FOLDER AND FILE PATHS
# ---------------------------------------

folder = os.path.dirname(os.path.abspath(__file__))

log_file = os.path.join(folder, "book_log.txt")
error_file = os.path.join(folder, "error_log.txt")

print("FILE HANDLING AND EXCEPTION FORENSICS")
print("-------------------------------------")


# ---------------------------------------
# 2. DEMONSTRATE FILE HANDLING BUGS
# ---------------------------------------

print("\nPART 1: Demonstrating file handling bugs")

# Bug 1: Write mode overwrites existing content
with open(log_file, "w") as file:
    file.write("Python Programming\n")

with open(log_file, "w") as file:
    file.write("Database Systems\n")

print("Bug 1: Previous content was overwritten.")

# Bug 2: Missing newline character
with open(log_file, "w") as file:
    file.write("Database Systems")
    file.write("Software Engineering")

with open(log_file, "r") as file:
    content = file.read()

print("Bug 2: Joined content:", repr(content))

# Bug 3: File not closed automatically
file = open(log_file, "w")
file.write("File opened without using with statement.")
file.close()

print("Bug 3: File was closed manually.")


# ---------------------------------------
# 3. CORRECT FILE HANDLING
# ---------------------------------------

print("\nPART 2: Correcting file handling bugs")

# Create a fresh corrected log
with open(log_file, "w") as file:
    file.write("Corrected Book Log\n")

# Book names to store
books = [
    "Python Programming",
    "Database Systems",
    "Software Engineering",
    "Computer Networks"
]

# Use append mode to preserve existing data
with open(log_file, "a") as file:
    for book in books:
        file.write(book + "\n")

print("Data successfully appended.")

# Read corrected file
with open(log_file, "r") as file:

    print("\nCorrected book log:")

    for line in file:
        print(line.strip())


# ---------------------------------------
# 4. EXCEPTION HANDLING
# ---------------------------------------

print("\nPART 3: Exception handling")

try:

    # Attempt to open a file that does not exist
    with open(
        os.path.join(folder, "missing_file.txt"), "r"
    ) as file:

        content = file.read()
        print(content)

except FileNotFoundError:

    message = "Error: Requested file was not found."

    print(message)

    with open(error_file, "a") as error:
        error.write(message + "\n")

except PermissionError:

    message = "Error: Permission denied."

    print(message)

    with open(error_file, "a") as error:
        error.write(message + "\n")

except OSError as error:

    message = "File error: " + str(error)

    print(message)

    with open(error_file, "a") as error_log:
        error_log.write(message + "\n")

else:

    print("File read successfully.")

finally:

    print("File handling operation completed.")


# ---------------------------------------
# 5. DISPLAY ERROR LOG
# ---------------------------------------

print("\nPART 4: Displaying error log")

if os.path.exists(error_file):

    with open(error_file, "r") as file:

        print(file.read())

else:

    print("No error log found.")


# ---------------------------------------
# 6. FINAL MESSAGE
# ---------------------------------------

print("Program completed successfully.")
