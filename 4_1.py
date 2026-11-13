
from decimal import Decimal, InvalidOperation

def process_mess_bill(filename):
    total = Decimal("0.00")
    report = []
    rejected = []

    try:
        with open(filename, "r", encoding="utf-8") as file:
            for line_number, line in enumerate(file, start=1):
                line = line.strip()

                if not line:
                    continue

                try:
                    parts = line.split(",")

                    if len(parts) != 3:
                        raise ValueError("Expected 3 fields")

                    register_number, name, amount_text = parts
                    amount = Decimal(amount_text.strip())

                    if not amount.is_finite():
                        raise ValueError("Amount must be finite")

                    total += amount
                    report.append(
                        f"{register_number} - {name} - Rs.{amount:.2f}"
                    )

                except (ValueError, InvalidOperation) as error:
                    rejected.append(
                        f"Line {line_number}: {line} | Error: {error}"
                    )

        print("MESS BILL REPORT")
        print("-------------------------")

        for record in report:
            print(record)

        print("-------------------------")
        print(f"Total Mess Bill: Rs.{total:.2f}")

        print("\nRejected Records:")

        if rejected:
            for record in rejected:
                print(record)
        else:
            print("No rejected records")

    except FileNotFoundError:
        print("Error: File not found:", filename)

    except PermissionError:
        print("Error: Permission denied:", filename)


# Main program
filename = "mess_oct.txt"
process_mess_bill(filename)
