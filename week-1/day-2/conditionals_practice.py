number = int(input("Enter your number: "))  # Ask the user for number

if number  == 0:
    print("It's zero.")
elif number  < 0:
    print("It's negative.")
else:
    print("It's positive.")


score = int(input("Enter your exam score: "))

if score >= 90:
    print("A")
elif score >= 80:
    print("B")
elif score >= 70:
    print("C")
elif score >= 60:
    print("D")
else:
    print("F")

test_list = [1., 2., 3.]  # Example list

if test_list:
    print("The list is not empty.")
else:
    print("The list is empty.")

x = 5
if x > 0:
    print("Positive")