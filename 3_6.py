
# Railway timetable using nested data structures

timetable = {
    "12601": {
        "name": "Chennai Express",
        "stops": [
            ("Chennai", "06:00", "06:15"),
            ("Katpadi", "08:00", "08:05"),
            ("Bangalore", "11:00", "11:15")
        ],
        "days": {"Monday", "Wednesday", "Friday"}
    },

    "12602": {
        "name": "Kaveri Express",
        "stops": [
            ("Chennai", "07:00", "07:15"),
            ("Katpadi", "09:00", "09:05"),
            ("Mysore", "13:00", "13:15")
        ],
        "days": {"Tuesday", "Thursday", "Saturday"}
    },

    "12603": {
        "name": "Vaigai Express",
        "stops": [
            ("Madurai", "05:00", "05:10"),
            ("Chennai", "10:00", "10:15"),
            ("Katpadi", "12:00", "12:05")
        ],
        "days": {"Monday", "Tuesday", "Friday"}
    },

    "12604": {
        "name": "Pandian Express",
        "stops": [
            ("Chennai", "08:00", "08:15"),
            ("Villupuram", "10:00", "10:05"),
            ("Madurai", "14:00", "14:15")
        ],
        "days": {"Wednesday", "Thursday", "Sunday"}
    },

    "12605": {
        "name": "Coimbatore Express",
        "stops": [
            ("Chennai", "09:00", "09:15"),
            ("Katpadi", "11:00", "11:05"),
            ("Coimbatore", "15:00", "15:15")
        ],
        "days": {"Monday", "Tuesday", "Wednesday",
                 "Thursday", "Friday", "Saturday", "Sunday"}
    }
}

# Display complete timetable
print("RAILWAY TIMETABLE")
print("-" * 60)

for train_no, details in timetable.items():
    print("\nTrain Number:", train_no)
    print("Train Name:", details["name"])
    print("Running Days:", sorted(details["days"]))

    print("Stations:")
    for station, arrival, departure in details["stops"]:
        print(station, "Arrival:", arrival,
              "Departure:", departure)

# Search station and day
search_station = input("\nEnter station name: ").strip()
search_day = input("Enter day: ").strip().title()

matching_trains = []

for train_no, details in timetable.items():

    if search_day not in details["days"]:
        continue

    for station, arrival, departure in details["stops"]:

        if station.lower() == search_station.lower():

            matching_trains.append({
                "number": train_no,
                "name": details["name"],
                "arrival": arrival,
                "departure": departure
            })

            break

# Sort trains by departure time
matching_trains = sorted(
    matching_trains,
    key=lambda train: train["departure"]
)

# Display search results
print("\nSEARCH RESULTS")
print("-" * 60)

if matching_trains:
    for train in matching_trains:
        print("Train Number:", train["number"])
        print("Train Name:", train["name"])
        print("Arrival:", train["arrival"])
        print("Departure:", train["departure"])
        print()
else:
    print("No trains found for the given station and day.")

# Build station index for faster searches
station_index = {}

for train_no, details in timetable.items():
    for station, arrival, departure in details["stops"]:

        station_index.setdefault(station.lower(), []).append(
            (train_no, arrival, departure)
        )

print("Station Index:")
for station, trains in station_index.items():
    print(station, ":", trains)

# Search using station index
print("\nSearching using station index:")

indexed_results = station_index.get(search_station.lower(), [])

found = False

for train_no, arrival, departure in indexed_results:

    if search_day in timetable[train_no]["days"]:
        print(train_no, timetable[train_no]["name"],
              "Arrival:", arrival, "Departure:", departure)
        found = True

if not found:
    print("No trains found.")
