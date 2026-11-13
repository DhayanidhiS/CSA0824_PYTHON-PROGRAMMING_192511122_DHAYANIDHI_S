
import re
import time
from collections import Counter

# Complaint records
calls = [
    {
        "district": "Chennai",
        "crop": "Rice",
        "text": "seeds not received seeds delayed"
    },
    {
        "district": "Madurai",
        "crop": "Wheat",
        "text": "fertiliser price high"
    },
    {
        "district": "Chennai",
        "crop": "Rice",
        "text": "seeds price high subsidy not received"
    },
    {
        "district": "Salem",
        "crop": "Cotton",
        "text": "cotton seeds required urgently"
    }
]

STOP = {"not", "high", "the", "is", "a", "and"}

# Count word frequencies using get()
def frequencies(texts, stop):
    counts = {}

    for text in texts:
        words = re.findall(r"\b[a-zA-Z]+\b", text.lower())

        for word in words:
            if word not in stop:
                counts[word] = counts.get(word, 0) + 1

    return counts

# Find top k words
def top(counts, k):
    return sorted(
        counts.items(),
        key=lambda item: (-item[1], item[0])
    )[:k]

# Group complaints by district using setdefault()
district_complaints = {}

for complaint in calls:
    district = complaint["district"]
    district_complaints.setdefault(district, []).append(complaint["text"])

# Group complaints by crop
crop_complaints = {}

for complaint in calls:
    crop = complaint["crop"]
    crop_complaints.setdefault(crop, []).append(complaint["text"])

texts = [complaint["text"] for complaint in calls]

# Display word frequencies
word_counts = frequencies(texts, STOP)

print("Word Frequencies:")
print(word_counts)

print("\nTop 3 Words:")
print(top(word_counts, 3))

print("\nComplaints by District:")
for district, complaints in district_complaints.items():
    print(district, ":", complaints)

print("\nComplaints by Crop:")
for crop, complaints in crop_complaints.items():
    print(crop, ":", complaints)

# Alternative method using Counter
counter_result = Counter()

for text in texts:
    words = re.findall(r"\b[a-zA-Z]+\b", text.lower())
    counter_result.update(word for word in words if word not in STOP)

print("\nCounter Result:")
print(counter_result)

# Compare dictionary and list.count()
sample_words = [
    word
    for text in texts
    for word in re.findall(r"\b[a-zA-Z]+\b", text.lower())
    if word not in STOP
]

start = time.perf_counter()
dictionary_result = frequencies(texts, STOP)
dictionary_time = time.perf_counter() - start

start = time.perf_counter()
distinct_words = set(sample_words)
list_count_result = {
    word: sample_words.count(word)
    for word in distinct_words
}
list_count_time = time.perf_counter() - start

print("\nDictionary time:", dictionary_time)
print("List count time:", list_count_time)

# Test empty text and punctuation
print("\nEmpty text result:", frequencies([""], STOP))
print("Punctuation result:", frequencies(["Seeds!!! PRICE, seeds."], STOP))
