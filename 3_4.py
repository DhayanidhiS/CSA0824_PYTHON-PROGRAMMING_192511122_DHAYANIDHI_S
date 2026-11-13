
# Students registered for electives
ai_elective = {
    "192311001", "192311004",
    "192311007", "192311009"
}

iot_elective = {
    "192311002", "192311004",
    "192311009", "192311010"
}

# All students
all_students = {
    f"1923110{i:02d}" for i in range(1, 11)
}

# Set operations
both = ai_elective & iot_elective

exactly_one = ai_elective ^ iot_elective

neither = all_students - (ai_elective | iot_elective)

# Display results
print("AI students:", sorted(ai_elective))
print("IoT students:", sorted(iot_elective))

print("\nclash      :", sorted(both))
print("exactly one:", sorted(exactly_one))
print("neither    :", sorted(neither))

# Repeat using set methods
both_method = ai_elective.intersection(iot_elective)

exactly_one_method = ai_elective.symmetric_difference(iot_elective)

neither_method = all_students.difference(
    ai_elective.union(iot_elective)
)

print("\nUsing set methods:")
print("clash      :", sorted(both_method))
print("exactly one:", sorted(exactly_one_method))
print("neither    :", sorted(neither_method))

# Remove duplicate registrations automatically
registrations = [
    "192311001",
    "192311004",
    "192311004",
    "192311007"
]

unique_registrations = set(registrations)

print("\nOriginal registrations:", registrations)
print("Unique registrations:", sorted(unique_registrations))

# Membership testing
student = "192311004"

print("\nIs student registered in AI?", student in ai_elective)
print("Is student registered in IoT?", student in iot_elective)
