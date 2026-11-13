
import sqlite3
import csv
import time
from pathlib import Path
from collections import Counter

folder = Path(__file__).resolve().parent

db_file = folder / "b4_complaints.db"
report_file = folder / "b4_final_report.txt"
csv_file = folder / "b4_complaints.csv"

print("FINAL ENGINEERING DECISION SYSTEM")
print("---------------------------------")

# STEP 1: CREATE SAMPLE COMPLAINT DATA
print("\nSTEP 1: GENERATING CITIZEN COMPLAINTS")

complaints = [
    "Water leakage problem in our street",
    "Road has many potholes",
    "Garbage collection is delayed",
    "Electricity supply is poor",
    "Drainage system is blocked",
    "Streetlight is not working",
    "Water supply is not available",
    "Road maintenance is required",
    "Garbage is not collected",
    "Power failure in our area"
]

# Generate 50 complaints
citizen_data = []

for i in range(50):
    complaint = complaints[i % len(complaints)]

    citizen_data.append({
        "complaint_id": i + 1,
        "complaint": complaint
    })

print("Total complaints generated:", len(citizen_data))


# STEP 2: CLASSIFY COMPLAINTS
print("\nSTEP 2: CLASSIFYING COMPLAINTS")

def classify_complaint(complaint):

    text = complaint.lower()

    if "water" in text or "leakage" in text:
        return "Water Supply"

    elif "road" in text or "potholes" in text:
        return "Road Maintenance"

    elif "garbage" in text:
        return "Sanitation"

    elif "electricity" in text or "power" in text:
        return "Electricity"

    elif "drainage" in text:
        return "Drainage"

    elif "streetlight" in text:
        return "Street Lighting"

    else:
        return "General"


# STEP 3: SENTIMENT ANALYSIS
print("\nSTEP 3: ANALYSING SENTIMENT")

negative_words = [
    "problem", "poor", "blocked", "delayed",
    "failure", "not", "potholes"
]

def analyse_sentiment(complaint):

    words = complaint.lower().split()

    for word in words:
        if word.strip(".,!?") in negative_words:
            return "Negative"

    return "Neutral"


# STEP 4: PROCESS ALL COMPLAINTS
print("\nSTEP 4: PROCESSING COMPLAINTS")

processed_data = []

for item in citizen_data:

    complaint = item["complaint"]

    category = classify_complaint(complaint)
    sentiment = analyse_sentiment(complaint)

    processed_data.append({
        "complaint_id": item["complaint_id"],
        "complaint": complaint,
        "category": category,
        "sentiment": sentiment
    })

print("Complaint processing completed.")
print("Processed complaints:", len(processed_data))


# STEP 5: STORE DATA IN SQLITE
print("\nSTEP 5: STORING DATA IN DATABASE")

con = sqlite3.connect(db_file)
cur = con.cursor()

cur.execute("DROP TABLE IF EXISTS complaints")

cur.execute("""
CREATE TABLE complaints (
    complaint_id INTEGER PRIMARY KEY,
    complaint TEXT,
    category TEXT,
    sentiment TEXT
)
""")

cur.executemany("""
INSERT INTO complaints
(complaint_id, complaint, category, sentiment)
VALUES (?, ?, ?, ?)
""", [
    (
        item["complaint_id"],
        item["complaint"],
        item["category"],
        item["sentiment"]
    )
    for item in processed_data
])

con.commit()

print("Complaint database created successfully.")


# STEP 6: CREATE DATABASE INDEX
print("\nSTEP 6: CREATING DATABASE INDEX")

cur.execute("""
CREATE INDEX idx_category
ON complaints(category)
""")

con.commit()

print("Database index created successfully.")


# STEP 7: CALCULATE CATEGORY STATISTICS
print("\nSTEP 7: COMPLAINT CATEGORY ANALYSIS")

cur.execute("""
SELECT category, COUNT(*)
FROM complaints
GROUP BY category
ORDER BY COUNT(*) DESC
""")

category_results = cur.fetchall()

for category, count in category_results:
    print(category, ":", count)


# STEP 8: SENTIMENT STATISTICS
print("\nSTEP 8: SENTIMENT ANALYSIS")

cur.execute("""
SELECT sentiment, COUNT(*)
FROM complaints
GROUP BY sentiment
""")

sentiment_results = cur.fetchall()

for sentiment, count in sentiment_results:
    print(sentiment, ":", count)


# STEP 9: MEASURE QUERY EXECUTION TIME
print("\nSTEP 9: DATABASE PERFORMANCE")

start = time.perf_counter()

for i in range(100):
    cur.execute("""
    SELECT COUNT(*)
    FROM complaints
    WHERE category = ?
    """, ("Water Supply",))
    cur.fetchone()

query_time = time.perf_counter() - start

print("100 database queries completed.")
print("Total query time:", round(query_time, 6), "seconds")


# STEP 10: EXPORT CSV FILE
print("\nSTEP 10: EXPORTING COMPLAINT DATA")

with open(csv_file, "w", newline="", encoding="utf-8") as file:

    writer = csv.DictWriter(
        file,
        fieldnames=[
            "complaint_id",
            "complaint",
            "category",
            "sentiment"
        ]
    )

    writer.writeheader()
    writer.writerows(processed_data)

print("CSV report created:", csv_file.name)


# STEP 11: GENERATE FINAL ENGINEERING REPORT
print("\nSTEP 11: GENERATING FINAL REPORT")

with open(report_file, "w", encoding="utf-8") as file:

    file.write("FINAL ENGINEERING DECISION REPORT\n")
    file.write("---------------------------------\n")

    file.write("Total complaints: 50\n")

    file.write("\nCATEGORY ANALYSIS\n")

    for category, count in category_results:
        file.write(category + ": " + str(count) + "\n")

    file.write("\nSENTIMENT ANALYSIS\n")

    for sentiment, count in sentiment_results:
        file.write(sentiment + ": " + str(count) + "\n")

    file.write(
        "\nDatabase query execution time: " +
        str(round(query_time, 6)) + " seconds\n"
    )

    file.write("\nENGINEERING DECISION\n")
    file.write(
        "SQLite is suitable for structured complaint storage "
        "and category-based retrieval.\n"
    )
    file.write(
        "Keyword-based classification is suitable for a basic "
        "demonstration but should be improved for real-world use.\n"
    )

print("Final report saved:", report_file.name)

con.close()

print("\nTASK B4 COMPLETED SUCCESSFULLY.")
