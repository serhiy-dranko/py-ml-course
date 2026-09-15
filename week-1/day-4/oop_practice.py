class Student:
    def __init__(self, name, grades):
        self.name = name
        self.grades = grades

    def average_grade(self):
        return sum(self.grades) / len(self.grades)

    def letter_grade(self):
        avg = self.average_grade()
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

    def pass_or_fail(self):
        return "Pass" if self.average_grade() >= 60 else "Fail"

    def add_grade(self, new_grade):
        self.grades.append(new_grade)

    def __str__(self):
        return f"{self.name} — Avg: {self.average_grade():.1f}, Grade: {self.letter_grade()}, Status: {self.pass_or_fail()}"


alex = Student("Alex", [88, 92, 79])
bob = Student("Bob", [65, 70, 60])
caren = Student("Caren", [95, 100, 98])
dima = Student("Dima", [55, 60, 58])

all_students = [alex, bob, caren, dima]

for s in all_students:
    print(s)   # uses __str__ automatically

alex.add_grade(100)
print(f"\nAfter adding a grade, {alex}")