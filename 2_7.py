
# Q7: Diagnose, Redesign and Validate
# Original Method vs Redesigned Method

import time


# Original method using repeated string concatenation
def original_method(items):
    result = ""

    for item in items:
        result += item + ";"

    return result


# Redesigned method using list and join()
def redesigned_method(items):
    parts = []

    for item in items:
        parts.append(item + ";")

    return "".join(parts)


# Test with different input sizes
sizes = [1000, 10000, 200000]

print("STRING BUILDING PERFORMANCE COMPARISON")
print("---------------------------------------")

for size in sizes:

    # Generate input data
    items = [f"Item{i}:Rs{i % 50}" for i in range(size)]

    # Measure original method
    start = time.perf_counter()
    original_result = original_method(items)
    original_time = time.perf_counter() - start

    # Measure redesigned method
    start = time.perf_counter()
    new_result = redesigned_method(items)
    new_time = time.perf_counter() - start

    # Validate both outputs
    same = original_result == new_result

    print("\nNumber of items:", size)
    print("Original time:", round(original_time, 6), "seconds")
    print("Redesigned time:", round(new_time, 6), "seconds")
    print("Same output:", same)

    # Calculate performance ratio
    if new_time > 0:
        ratio = original_time / new_time
        print("Speed ratio:", round(ratio, 2))


print("\nCONCLUSION")
print("----------")
print("Both methods produce the same output.")

print("The redesigned method uses a list and join().")
print("It avoids repeated string concatenation.")
print("The redesigned method is generally suitable for large inputs.")
