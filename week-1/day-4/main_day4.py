import grade_helpers
from grade_helpers import average_grade

students = [
    {"name": "Alex", "grades": [88, 92, 79]},
    {"name": "Bob", "grades": [65, 70, 60]},
    {"name": "Caren", "grades": [95, 100, 98]},
    {"name": "Dima", "grades": [55, 60, 58]},
    {"name": "Serhiy", "grades": [90, 85, 93]},
]

def main():
    for student in students:
        avg = average_grade(student["grades"])                  # imported directly
        grade = grade_helpers.letter_grade(avg)                 # imported via module prefix
        status = grade_helpers.pass_or_fail(avg)
        print(f"{student['name']}: Average {avg:.1f}, Grade {grade}, {status}")

if __name__ == "__main__":
    main()