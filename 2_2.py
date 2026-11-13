# Q2: Bank OTP Verification

correct_otp = "1234"

print("BANK OTP VERIFICATION")
print("---------------------")

# WHILE LOOP
print("\nUsing WHILE loop")

attempts = 0
max_attempts = 3

while attempts < max_attempts:
    otp = input("Enter OTP: ")

    if otp == "":
        print("Blank entry! Please enter OTP.")
        continue

    attempts += 1

    if otp == correct_otp:
        print("OTP verified successfully!")
        break
    else:
        print("Incorrect OTP!")
        print("Attempts remaining:", max_attempts - attempts)

else:
    print("Account locked for 30 minutes.")

# FOR LOOP
print("\nUsing FOR loop")

for attempt in range(1, 4):
    otp = input("Enter OTP: ")

    if otp == "":
        print("Blank entry! Please enter OTP.")
        continue

    if otp == correct_otp:
        print("OTP verified successfully!")
        break
    else:
        print("Incorrect OTP!")

else:
    print("Account locked for 30 minutes.")

# PASS EXAMPLE
print("\nPASS statement example")

if True:
    pass

print("Program completed.")
