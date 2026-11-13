# Q5: Functions, Parameters and Scope


# Buggy function: uses a mutable default list
def add_item_buggy(item, order=[]):
    order.append(item)
    return order


# Correct function: uses None as the default value
def add_item(item, order=None):

    if order is None:
        order = []

    order.append(item)

    return order


# Function using positional and keyword arguments
def calculate_bill(price, quantity=1, gst=5):
    total = price * quantity
    tax = total * gst / 100

    final_amount = total + tax

    return total, tax, final_amount


# Global variable
canteen_name = "SIMATS Canteen"


def display_canteen():
    local_message = "Welcome to the canteen"
    print(local_message)
    print("Canteen:", canteen_name)


# Nonlocal variable example
def counter():

    count = 0

    def increase():
        nonlocal count
        count += 1
        print("Counter:", count)

    increase()
    increase()
    increase()


# Testing buggy and corrected functions
print("BUGGY FUNCTION")
print("----------------")

print(add_item_buggy("Tea"))
print(add_item_buggy("Vada"))

print("Default values:", add_item_buggy.__defaults__)


print("\nCORRECT FUNCTION")
print("----------------")

print(add_item("Tea"))
print(add_item("Vada"))
print(add_item("Coffee"))


# Testing order with an explicitly supplied list
print("\nCUSTOMER ORDER")

customer_order = []

add_item("Tea", customer_order)
add_item("Vada", customer_order)

print("Customer order:", customer_order)


# Testing function parameters and return values
print("\nBILL CALCULATION")

total, tax, final_amount = calculate_bill(100, quantity=2, gst=5)

print("Total:", total)
print("GST:", tax)
print("Final Amount:", final_amount)


# Testing local and global variables
print("\nSCOPE EXAMPLE")

display_canteen()


# Testing nonlocal variable
print("\nNONLOCAL EXAMPLE")

counter()
