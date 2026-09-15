import csv

with open("students.csv", "r") as f:
    reader = csv.DictReader(f)
    students = list(reader)   # перетворюємо ітератор у звичайний список одразу

for row in students:
    print(row["name"], row["grade"])

high_grade_students = [row for row in students if int(row["grade"]) > 80]
print(high_grade_students)

average_grade = sum(int(row["grade"]) for row in students) / len(students)
print(f"Average grade: {average_grade:.1f}")

with open("high_grade_students.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["name", "grade", "city"])
    writer.writeheader()
    writer.writerows(high_grade_students)

with open("high_grade_students.csv", "r") as f:
    print(f.read())