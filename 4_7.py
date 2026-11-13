
import time

# Function 1: Original method using repeated string concatenation
def old_method(records):
    result = ""

    for item in records:
        result += item + "\n"

    return result


# Function 2: Improved method using list and join()
def improved_method(records):
    result = []

    for item in records:
        result.append(item)

    return "\n".join(result) + "\n"


# Main program
print("DIAGNOSE, REDESIGN AND VALIDATE")
print("--------------------------------")

sizes = [1000, 10000, 200000]

for size in sizes:

    print("\nTesting with", size, "records")

    # Generate sample data
    records = []

    for i in range(size):
        records.append("Student Record " + str(i))

    # Test original method
    start_time = time.perf_counter()
    old_result = old_method(records)
    old_time = time.perf_counter() - start_time

    # Test improved method
    start_time = time.perf_counter()
    new_result = improved_method(records)
    new_time = time.perf_counter() - start_time

    # Validate output
    same_output = (old_result == new_result)

    # Display results
    print("Original method time :", round(old_time, 6), "seconds")
    print("Improved method time :", round(new_time, 6), "seconds")

    if new_time > 0:
        print("Performance ratio    :", round(old_time / new_time, 2), "times")
    else:
        print("Performance ratio    : Too small to calculate")

    print("Same output          :", same_output)

print("\nTesting completed successfully.")
