def average_grade(grades):
    return sum(grades) / len(grades)

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

def pass_or_fail(avg):
    return "Pass" if avg >= 60 else "Fail"