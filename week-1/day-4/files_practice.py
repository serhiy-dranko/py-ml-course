notes = [
    "Python was named after the British comedy group Monty Python, not the snake.",
    "Python uses indentation instead of curly braces to define blocks of code.",
    "Guido van Rossum released the first version of Python in 1991.",
    "Python is an interpreted language, meaning code is executed line by line.",
    "It is the dominant programming language used for artificial intelligence and machine learning.",
]
# Write notes to a file
with open("notes.txt", "w") as f:
    for note in notes:
        f.write(note + "\n")
# Read and print notes from the file
with open("notes.txt", "r") as f:
    for index, line in enumerate(f):
        print(index, line.strip())
# Append a new note to the file
with open("notes.txt", "a") as f:
    f.write("Python is the primary language used to operate NASA's open-source Core Flight System and analyze data from space missions.\n")
# Read and print notes from the file again
with open("notes.txt", "r") as f:
    print(f.read())


# Overwrite the file with a new note
with open("notes.txt", "w") as f:
    f.write("Only this line survives now.\n")
# Read and print notes from the file again
with open("notes.txt", "r") as f:
    print(f.read())


# "w" mode truncates (erases) the file the moment it's opened, before any
# writing happens so all previous lines were wiped out 
# unlike "a" mode which adds to the end and preserves existing content.