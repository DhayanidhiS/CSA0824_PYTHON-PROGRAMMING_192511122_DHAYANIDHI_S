# Q3: Vehicle Registration Number Validator

def normalise(text):
    """Remove spaces and hyphens and convert to uppercase."""
    return text.replace(" ", "").replace("-", "").strip().upper()


def is_valid(reg):
    """Validate the vehicle registration number."""

    if len(reg) not in (9, 10):
        return False

    # First two characters must be letters
    if not reg[0:2].isalpha():
        return False

    # Next two characters must be digits
    if not reg[2:4].isdigit():
        return False

    # Last four characters must be digits
    if not reg[-4:].isdigit():
        return False

    # Middle part must contain one or two letters
    middle = reg[4:-4]

    if len(middle) not in (1, 2):
        return False

    if not middle.isalpha():
        return False

    return True


def format_number(reg):
    """Format a valid registration number for printing."""

    if not is_valid(reg):
        return "Invalid Registration Number"

    return reg[:2] + " " + reg[2:4] + " " + reg[4:-4] + " " + reg[-4:]


# Test registration numbers
numbers = [
    "tn 09 ab 1234",
    "KA-01-M-0007",
    "TN9AB1234",
    "TN 22 1234 AB",
    "Tn09Ab1234",
    "KL 07 CD 5678"
]

print("VEHICLE REGISTRATION VALIDATOR")
print("--------------------------------")

for raw in numbers:
    reg = normalise(raw)

    if is_valid(reg):
        print(f"{raw:18} -> {reg:11} VALID")
        print("Receipt Format:", format_number(reg))
    else:
        print(f"{raw:18} -> {reg:11} INVALID")
