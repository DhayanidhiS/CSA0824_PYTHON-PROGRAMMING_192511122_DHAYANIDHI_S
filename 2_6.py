# Q6: Recursion and Memoisation

from functools import lru_cache
import sys


# Count function calls
calls = 0


# Method 1: Normal recursion
def ways_naive(n):

    global calls
    calls += 1

    if n <= 1:
        return 1

    return ways_naive(n - 1) + ways_naive(n - 2)


# Method 2: Recursion with memoisation
calls = 0

@lru_cache(maxsize=None)
def ways_memo(n):

    global calls
    calls += 1

    if n <= 1:
        return 1

    return ways_memo(n - 1) + ways_memo(n - 2)


# Method 3: Iterative approach
def ways_loop(n):

    if n <= 1:
        return 1

    first = 1
    second = 1

    for i in range(2, n + 1):
        current = first + second
        first = second
        second = current

    return second


# Compare naive and memoised recursion
calls = 0
print("Naive:", ways_naive(25), "calls =", calls)

calls = 0
ways_memo.cache_clear()

print("Memo :", ways_memo(25), "calls =", calls)


# Check answers from 1 to 6
print("\nWAYS TO CLIMB")

for n in range(1, 7):
    ways_memo.cache_clear()
    print(f"Steps = {n}, Ways = {ways_memo(n)}")


# Check recursion limit
print("\nRECURSION LIMIT")

print("Current recursion limit:", sys.getrecursionlimit())

try:
    ways_memo.cache_clear()
    print("Ways for 1000 steps:", ways_memo(1000))

except RecursionError:
    print("RecursionError occurred for 1000 steps.")


# Iterative solution for 1000 steps
print("\nITERATIVE SOLUTION")

print("Ways for 1000 steps:", ways_loop(1000))
