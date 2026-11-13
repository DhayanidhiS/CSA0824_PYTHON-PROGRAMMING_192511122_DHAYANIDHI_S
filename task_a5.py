
import csv
from pathlib import Path
from datetime import datetime

# Find the folder containing this Python file
folder = Path(__file__).resolve().parent

output_file = folder / "citizen_complaints.csv"

print("AI-BASED CITIZEN COMPLAINT ANALYSIS SYSTEM")
print("------------------------------------------")

# STEP 1: DEFINE COMPLAINT CATEGORIES
categories = {
    "Water Supply": ["water", "pipeline", "drinking", "leakage"],
    "Electricity": ["electricity", "power", "current", "streetlight"],
    "Road Maintenance": ["road", "pothole", "bridge", "traffic"],
    "Sanitation": ["garbage", "waste", "drainage", "cleaning"],
    "Public Safety": ["safety", "accident", "crime", "danger"]
}

# STEP 2: DEFINE SENTIMENT WORDS
positive_words = [
    "good", "excellent", "thank", "happy", "resolved",
    "improved", "helpful"
]

negative_words = [
    "bad", "poor", "problem", "issue", "dirty",
    "dangerous", "worst", "delay", "broken"
]


# STEP 3: CLASSIFY COMPLAINT
def classify_complaint(complaint):

    text = complaint.lower()

    for category, keywords in categories.items():
        for keyword in keywords:
            if keyword in text:
                return category

    return "General Complaint"


# STEP 4: ANALYSE SENTIMENT
def analyse_sentiment(complaint):

    words = complaint.lower().split()

    positive_count = sum(
        1 for word in words if word.strip(".,!?") in positive_words
    )

    negative_count = sum(
        1 for word in words if word.strip(".,!?") in negative_words
    )

    if negative_count > positive_count:
        return "Negative"

    elif positive_count > negative_count:
        return "Positive"

    else:
        return "Neutral"


# STEP 5: GENERATE SIMPLE SUMMARY
def generate_summary(complaint):

    words = complaint.split()

    if len(words) <= 12:
        return complaint

    return " ".join(words[:12]) + "..."


# STEP 6: ACCEPT COMPLAINTS
complaints = []

try:
    count = int(input("\nEnter number of complaints: "))

    if count <= 0:
        print("Please enter a number greater than zero.")
    else:
        for i in range(count):

            print("\nComplaint", i + 1)

            citizen_name = input("Enter citizen name: ")
            complaint = input("Enter complaint: ")

            if not citizen_name.strip() or not complaint.strip():
                print("Name and complaint cannot be empty.")
                continue

            category = classify_complaint(complaint)
            sentiment = analyse_sentiment(complaint)
            summary = generate_summary(complaint)

            complaints.append({
                "Complaint_ID": i + 1,
                "Citizen_Name": citizen_name,
                "Complaint": complaint,
                "Category": category,
                "Sentiment": sentiment,
                "Summary": summary,
                "Date": datetime.now().strftime("%Y-%m-%d")
            })

except ValueError:
    print("Invalid input. Please enter a valid number.")


# STEP 7: DISPLAY RESULTS
print("\nCOMPLAINT ANALYSIS RESULTS")
print("------------------------------------------")

for item in complaints:
    print("\nComplaint ID:", item["Complaint_ID"])
    print("Citizen:", item["Citizen_Name"])
    print("Category:", item["Category"])
    print("Sentiment:", item["Sentiment"])
    print("Summary:", item["Summary"])


# STEP 8: SAVE RESULTS TO CSV
if complaints:

    fieldnames = [
        "Complaint_ID",
        "Citizen_Name",
        "Complaint",
        "Category",
        "Sentiment",
        "Summary",
        "Date"
    ]

    with open(output_file, "w", newline="", encoding="utf-8") as file:

        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(complaints)

    print("\nComplaint records saved successfully.")
    print("Output file:", output_file.name)

print("\nTASK A5 COMPLETED SUCCESSFULLY.")
