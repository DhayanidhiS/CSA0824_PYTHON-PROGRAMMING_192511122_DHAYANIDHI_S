
import random
import time

# Generate rainfall readings for 365 days
random.seed(10)
readings = [random.randint(0, 20) for _ in range(365)]

# Weekly totals using slicing
weekly_totals = []

for i in range(0, len(readings), 7):
    week = readings[i:i + 7]
    weekly_totals.append(sum(week))

# Wettest and driest weeks
wettest_week = weekly_totals.index(max(weekly_totals)) + 1
driest_week = weekly_totals.index(min(weekly_totals)) + 1

# Maximum and minimum daily readings
print("Maximum rainfall:", max(readings), "mm")
print("Maximum rainfall day:", readings.index(max(readings)) + 1)

print("Minimum rainfall:", min(readings), "mm")
print("Minimum rainfall day:", readings.index(min(readings)) + 1)

print("\nWettest week:", wettest_week)
print("Wettest weekly total:", max(weekly_totals), "mm")

print("Driest week:", driest_week)
print("Driest weekly total:", min(weekly_totals), "mm")

# Naive moving average
def naive_average(data):
    averages = []

    for i in range(len(data) - 6):
        total = sum(data[i:i + 7])
        averages.append(total / 7)

    return averages

# Running-sum moving average
def running_average(data):
    averages = []

    if len(data) < 7:
        return averages

    current_sum = sum(data[:7])
    averages.append(current_sum / 7)

    for i in range(7, len(data)):
        current_sum += data[i] - data[i - 7]
        averages.append(current_sum / 7)

    return averages

naive = naive_average(readings)
running = running_average(readings)

print("\nNumber of moving averages:", len(running))
print("First 5 moving averages:", running[:5])

# Dry days
dry_days = []

for i in range(len(readings)):
    if readings[i] == 0:
        dry_days.append(i + 1)

print("\nDry days:", dry_days)

# Compare execution times
for size in [365, 36500, 365000]:
    data = [random.randint(0, 20) for _ in range(size)]

    start = time.perf_counter()
    naive_average(data)
    naive_time = time.perf_counter() - start

    start = time.perf_counter()
    running_average(data)
    running_time = time.perf_counter() - start

    print("\nData size:", size)
    print("Naive time:", round(naive_time, 6), "seconds")
    print("Running-sum time:", round(running_time, 6), "seconds")

# Test empty and short lists
print("\nEmpty list result:", running_average([]))
print("Short list result:", running_average([2, 3, 4, 5]))
