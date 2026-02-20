import statistics as st
from collections import Counter
import json


student_records= []
stats= {}
unique_scores= set()

for i in range(1,7):
    name= input(f"Student {i} name: ")
    score= int(input(f"Student {i} score: "))

    student_records.append((name, score))

scores= [score for name, score in student_records]

stats['highest']= max(scores)
stats['lowest']= min(scores)
stats['average']= sum(scores)/len(scores)

#Challenge Extension
stats['median']= st.median(scores)

#Challenge Extension
above_avg= [name for name, 
            score in student_records if score > stats['average']]
below_avg= [name for name,
            score in student_records if score <= stats['average']]

unique_scores= set(scores)

#Challenge Extension
def letter_grade(score):
    if score >= 90: return 'A'
    elif score >= 80: return 'B'
    elif score >= 70: return 'C'
    elif score >= 60: return 'D'
    else: return 'F'

print("\n---> CLASS RESULTS <---")
for i, (name, score) in enumerate(student_records, 1):
    print(f"{i}. {name}: {score} ({letter_grade(score)})")

print("\n---> CLASS STATISTICS <---")
for key, value in stats.items():
    print(f"{key.capitalize()} Score: {value}")

print(f"\n---> UNIQUE SCORES <---\n{unique_scores}")
print(f"Total Unique Scores: {len(unique_scores)}")

print("\n---> GRADE DISTRIBUTION <---")
grade_counts= Counter(scores)
for score, count in grade_counts.items():
    print(f"Score {score}: {count} {'student' if count == 1 else 'students'}")


print("\n---> PERFORMANCE GROUPS <---")
print(f"Above Average: {', '.join(above_avg)}")
print(f"Below Average: {', '.join(below_avg)}")

#Challenge Extension
report_data= {"records": student_records, "statistics": stats,
              "unique scores": list(unique_scores)}


with open("grade_report.json", "w") as f:
    json.dump(report_data, f, indent= 4)

