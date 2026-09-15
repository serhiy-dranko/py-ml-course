students = [
    {"name": "Alex", "grades": [88, 92, 79]},
    {"name": "Bob", "grades": [65, 70, 60]},
    {"name": "Caren", "grades": [95, 100, 98]},
    {"name": "Dima", "grades": [55, 60, 58]},
    {"name": "Serhiy", "grades": [90, 85, 93]},
]
## calculate average grade for each student and assign letter grade
def average_grade(grades):
    return sum(grades) / len(grades)
## get letter grade based on average
def letter_grade(avg):
    if avg >= 90:
        return "A"
    elif avg >= 80:
        return "B"
    elif avg >= 70:
        return "C"
    elif avg >= 60:
        return "D"
    else:
        return "F"
## calculate average grade for each student and assign letter grade
all_averages = []
## calculate average grade for each student and assign letter grade
for student in students:
    avg = average_grade(student["grades"])
    grade = letter_grade(avg)
    all_averages.append(avg)
    print(f"{student['name']}: Average {avg:.1f} — Grade {grade}")
## calculate class average and honor roll
honor_roll = [s["name"] for s in students if average_grade(s["grades"]) >= 90]
## get unique letter grades in class
unique_grades = {letter_grade(average_grade(s["grades"])) for s in students}
## calculate class average
class_average = sum(all_averages) / len(all_averages)
## print summary
print(f"\nTotal students: {len(students)}")
print(f"Class average: {class_average:.1f}")
print(f"Honor roll: {honor_roll}")
print(f"Unique letter grades in class: {unique_grades}")

# Stretch goal: sort students by average grade, highest to lowest

sorted_students = sorted(students, key=lambda s: average_grade(s["grades"]), reverse=True)
print("\nSorted by average (high to low):")
for s in sorted_students:
    print(s["name"], f"{average_grade(s['grades']):.1f}")