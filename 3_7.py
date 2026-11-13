
import time
import random

# Normalize phone number
def normalize_phone(phone):
    if not phone:
        return ""

    digits = "".join(
        character for character in phone
        if character.isdigit()
    )

    # Remove India's country code for 10-digit local comparison
    if len(digits) == 12 and digits.startswith("91"):
        digits = digits[2:]

    return digits


# Normalize name
def normalize_name(name):
    if not name:
        return ""

    return " ".join(name.lower().strip().split())


# Normalize email
def normalize_email(email):
    if not email:
        return ""

    return email.lower().strip()


# Merge contacts
def merge_contacts(contact_lists):

    # Dictionary: normalized phone -> contact group
    phone_index = {}

    # Dictionary: group ID -> merged contact
    merged = {}

    next_id = 0

    for contacts in contact_lists:

        for contact in contacts:

            name = contact.get("name", "").strip()
            phone = contact.get("phone", "")
            email = contact.get("email", "")

            normalized_name = normalize_name(name)
            normalized_number = normalize_phone(phone)
            normalized_email = normalize_email(email)

            # Find existing contact group by phone number
            existing_id = phone_index.get(normalized_number) if normalized_number else None

            if existing_id is None:
                existing_id = next_id
                next_id += 1

                merged[existing_id] = {
                    "name": name,
                    "normalized_name": normalized_name,
                    "phones": set(),
                    "emails": set()
                }

            # Add contact details
            if name and not merged[existing_id]["name"]:
                merged[existing_id]["name"] = name
                merged[existing_id]["normalized_name"] = normalized_name

            if normalized_number:
                merged[existing_id]["phones"].add(normalized_number)
                phone_index[normalized_number] = existing_id

            if normalized_email:
                merged[existing_id]["emails"].add(normalized_email)

    return list(merged.values())


# Contacts from old phone 1
phone1 = [
    {
        "name": "Dr. Ravi",
        "phone": "+91 98400 12345",
        "email": "Ravi@gmail.com"
    },
    {
        "name": "Anitha",
        "phone": "9876543210",
        "email": "anitha@gmail.com"
    },
    {
        "name": "Kumar",
        "phone": "9000011111",
        "email": "kumar@gmail.com"
    }
]

# Contacts from old phone 2
phone2 = [
    {
        "name": "ravi kumar",
        "phone": "9840012345",
        "email": "ravi@gmail.com"
    },
    {
        "name": "Anitha",
        "phone": "+91 98765 43210",
        "email": "anitha2@gmail.com"
    },
    {
        "name": "Priya",
        "phone": "9123456780",
        "email": "priya@gmail.com"
    }
]

# Contacts from SIM card
sim_card = [
    {
        "name": "Ravi",
        "phone": "98400-12345",
        "email": "ravi.office@gmail.com"
    },
    {
        "name": "Suresh",
        "phone": "9555511111",
        "email": ""
    },
    {
        "name": "",
        "phone": "",
        "email": "unknown@gmail.com"
    }
]

# Merge all contact lists
all_contact_lists = [phone1, phone2, sim_card]

result = merge_contacts(all_contact_lists)

# Display merged contacts
print("MERGED CONTACT LIST")
print("=" * 50)

for index, contact in enumerate(result, start=1):

    print("\nContact", index)
    print("Name:", contact["name"])
    print("Phone Numbers:", sorted(contact["phones"]))
    print("Email Addresses:", sorted(contact["emails"]))


# Performance test
def generate_contacts(size):

    contacts = []

    for i in range(size):
        number = str(9000000000 + (i % max(1, size // 2)))

        contacts.append({
            "name": "Person " + str(i),
            "phone": number,
            "email": "person" + str(i) + "@gmail.com"
        })

    return contacts


print("\nPERFORMANCE TEST")
print("=" * 50)

for size in [1000, 100000]:

    test_contacts = generate_contacts(size)

    start = time.perf_counter()

    merged_contacts = merge_contacts([test_contacts])

    elapsed = time.perf_counter() - start

    print("\nInput contacts:", size)
    print("Merged contacts:", len(merged_contacts))
    print("Execution time:", round(elapsed, 6), "seconds")


# Test normalization
print("\nNORMALIZATION TEST")

print(normalize_phone("+91 98400 12345"))
print(normalize_phone("98400-12345"))
print(normalize_name("  DR. RAVI  KUMAR "))
print(normalize_email(" RAVI@GMAIL.COM "))
