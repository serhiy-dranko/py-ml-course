import csv
from oop_practice import Student   # reuse the class from Block 4

with open("students.csv", "r") as f:
    reader = csv.DictReader(f)
    student_objects = [Student(row["name"], [int(row["grade"])]) for row in reader]

for s in student_objects:
    print(s)

top_student = max(student_objects, key=lambda s: s.average_grade())
print(f"\nTop student: {top_student.name}")