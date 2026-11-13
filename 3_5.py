
import time
import sys

# Temperature readings in Celsius
readings = [4, 7, 55, 3, -60, 9, 6, 12, 2, 45]

# Method 1: For loop and append()
valid_loop = []

for temp in readings:
    if -50 <= temp <= 50:
        valid_loop.append(temp)

fahrenheit_loop = []

for temp in valid_loop:
    fahrenheit_loop.append((temp * 9/5) + 32)

# Method 2: List comprehension
valid_comprehension = [
    temp for temp in readings
    if -50 <= temp <= 50
]

fahrenheit_comprehension = [
    (temp * 9/5) + 32
    for temp in valid_comprehension
]

# Method 3: filter(), map() and lambda
valid_filter = list(
    filter(lambda temp: -50 <= temp <= 50, readings)
)

fahrenheit_map = list(
    map(lambda temp: (temp * 9/5) + 32, valid_filter)
)

# Find alarm minutes: temperature outside 2–8 Celsius
alarm_minutes = [
    minute
    for minute, temp in enumerate(readings, start=1)
    if -50 <= temp <= 50 and not (2 <= temp <= 8)
]

# Display results
print("Original readings:", readings)

print("\nValid Celsius readings:", valid_loop)
print("Fahrenheit readings:", fahrenheit_loop)

print("\nUsing list comprehension:")
print("Valid readings:", valid_comprehension)
print("Fahrenheit readings:", fahrenheit_comprehension)

print("\nUsing filter and map:")
print("Valid readings:", valid_filter)
print("Fahrenheit readings:", fahrenheit_map)

print("\nAlarm minutes:", alarm_minutes)

# Verify all three methods
print("\nAll methods give same result:",
      valid_loop == valid_comprehension == valid_filter)

# Dictionary comprehension
temperature_dictionary = {
    minute: temp
    for minute, temp in enumerate(readings, start=1)
    if -50 <= temp <= 50
}

print("\nTemperature dictionary:", temperature_dictionary)

# Set comprehension
temperature_set = {
    temp for temp in readings
    if -50 <= temp <= 50
}

print("Temperature set:", temperature_set)

# Generator expression
generator = (
    temp for temp in readings
    if -50 <= temp <= 50
)

print("Generator values:", list(generator))

# Memory comparison
list_data = [x for x in range(100000)]
generator_data = (x for x in range(100000))

print("\nList memory:", sys.getsizeof(list_data), "bytes")
print("Generator memory:", sys.getsizeof(generator_data), "bytes")

# Performance comparison
for size in [10000, 100000, 1000000]:
    data = [x % 60 for x in range(size)]

    start = time.perf_counter()
    result1 = [x for x in data if -50 <= x <= 50]
    loop_time = time.perf_counter() - start

    start = time.perf_counter()
    result2 = list(filter(lambda x: -50 <= x <= 50, data))
    filter_time = time.perf_counter() - start

    start = time.perf_counter()
    result3 = []
    for x in data:
        if -50 <= x <= 50:
            result3.append(x)
    append_time = time.perf_counter() - start

    print("\nData size:", size)
    print("List comprehension:", loop_time)
    print("Filter method:", filter_time)
    print("Append method:", append_time)

# Test all-valid and all-invalid readings
print("\nAll valid:", [x for x in [2, 3, 4] if -50 <= x <= 50])
print("All invalid:", [x for x in [55, 60, -70] if -50 <= x <= 50])
