# Q4: String Building Performance

import time


# Generate 200,000 bill items
items = [f"Item{i}:Rs{i % 50}" for i in range(200_000)]


# Method 1: Using + operator
def build_plus(parts):
    text = ""

    for p in parts:
        text += p + ";"

    return text


# Method 2: Using join()
def build_join(parts):
    return ";".join(parts) + ";"


# Method 3: Using f-string
def build_fstring(parts):
    result = ""

    for i, p in enumerate(parts):
        result += f"{p};"

    return result


# Measure execution time of +
start = time.perf_counter()
a = build_plus(items)
t_plus = time.perf_counter() - start


# Measure execution time of join()
start = time.perf_counter()
b = build_join(items)
t_join = time.perf_counter() - start


# Measure execution time of f-string method
start = time.perf_counter()
c = build_fstring(items)
t_fstring = time.perf_counter() - start


# Display results
print("SMS BILL STATEMENT")
print("------------------")

print("Same text:", a == b == c)
print("Length:", len(b))

print(f"+ operator time : {t_plus:.4f} seconds")
print(f"join() time     : {t_join:.4f} seconds")
print(f"f-string time   : {t_fstring:.4f} seconds")
