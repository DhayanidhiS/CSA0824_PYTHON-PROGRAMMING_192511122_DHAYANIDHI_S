
import copy
import sys
import time

# Bus stops represented by tuples
stops = {
    (13.0827, 80.2707): "Chennai Central",
    (13.0418, 80.2341): "T. Nagar",
    (13.0569, 80.2425): "Guindy"
}

print("Bus Stop Details:")

for coordinates, name in stops.items():
    latitude, longitude = coordinates
    print(name, ":", latitude, longitude)

print("\nSearching for a bus stop:")
print(stops[(13.0418, 80.2341)])

# Incorrect grid: all rows refer to the same list
rows, cols = 3, 4

bad = [[0] * cols] * rows
bad[0][1] = 7

# Correct grid using list comprehension
good = [[0 for j in range(cols)] for i in range(rows)]
good[0][1] = 7

print("\nBad grid:", bad)
print("Good grid:", good)

print("Bad rows identical:", bad[0] is bad[1])
print("Good rows identical:", good[0] is good[1])

# Aliasing
original = [10, 20, 30]
alias = original

alias.append(40)

print("\nOriginal list:", original)
print("Alias list:", alias)
print("Same object:", original is alias)

# Shallow copy
shallow1 = [10, 20, 30]
shallow2 = copy.copy(shallow1)

shallow2.append(40)

print("\nShallow copy original:", shallow1)
print("Shallow copy new list:", shallow2)

# Deep copy
nested = [[1, 2], [3, 4]]
deep = copy.deepcopy(nested)

deep[0][0] = 99

print("\nOriginal nested list:", nested)
print("Deep copied list:", deep)

# Tuple containing a mutable list
data = (100, 200, [300, 400])
data[2].append(500)

print("\nTuple with modified list:", data)

# Memory comparison
values = list(range(1000000))
tuple_values = tuple(values)

print("\nList memory:", sys.getsizeof(values), "bytes")
print("Tuple memory:", sys.getsizeof(tuple_values), "bytes")

# Creation and indexing time
start = time.perf_counter()
list_data = list(range(1000000))
list_creation = time.perf_counter() - start

start = time.perf_counter()
tuple_data = tuple(range(1000000))
tuple_creation = time.perf_counter() - start

start = time.perf_counter()
x = list_data[500000]
list_indexing = time.perf_counter() - start

start = time.perf_counter()
y = tuple_data[500000]
tuple_indexing = time.perf_counter() - start

print("\nList creation time:", list_creation)
print("Tuple creation time:", tuple_creation)
print("List indexing time:", list_indexing)
print("Tuple indexing time:", tuple_indexing)

# Demonstrate invalid list dictionary key
try:
    sample = {[13.0418, 80.2341]: "T. Nagar"}
except TypeError as error:
    print("\nDictionary key error:", error)
