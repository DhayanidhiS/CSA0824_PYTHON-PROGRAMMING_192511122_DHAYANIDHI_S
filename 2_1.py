# Q1: Electricity Subsidy Eligibility

def subsidy_separate(units, ration_card, senior_citizen):
    print("Using separate if statements:")

    if units <= 100:
        print("Full Subsidy")

    if 101 <= units <= 200 and ration_card:
        print("Partial Subsidy")

    if units > 200 and senior_citizen:
        print("Special Subsidy")

    if units > 200 and not senior_citizen:
        print("No Subsidy")

    if 101 <= units <= 200 and not ration_card:
        print("No Subsidy")


def subsidy_if_elif(units, ration_card, senior_citizen):
    if units <= 100:
        return "Full Subsidy"

    elif 101 <= units <= 200:
        if ration_card:
            return "Partial Subsidy"
        else:
            return "No Subsidy"

    elif units > 200:
        if senior_citizen:
            return "Special Subsidy"
        else:
            return "No Subsidy"


# Eight test households
households = [
    (100, True, False),
    (101, True, False),
    (101, False, False),
    (150, True, False),
    (200, False, False),
    (201, True, True),
    (201, False, False),
    (250, True, True)
]

print("ELECTRICITY SUBSIDY ELIGIBILITY")
print("--------------------------------")

for i, household in enumerate(households, start=1):
    units, ration_card, senior = household

    result = subsidy_if_elif(units, ration_card, senior)

    print(f"Household {i}:")
    print(f"Units: {units}")
    print(f"Ration Card: {ration_card}")
    print(f"Senior Citizen: {senior}")
    print("Decision:", result)
    print()
