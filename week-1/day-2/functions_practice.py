def is_even(number):
    return number % 2 == 0

num1 = int(input("Enter a number to check even/odd: "))
print(is_even(num1))

def celsius_to_fahrenheit(celsius):
    return celsius * 9 / 5 + 32

temp = float(input("Enter temperature in Celsius: "))
print(celsius_to_fahrenheit(temp))



def get_stats(numbers):
    minimum = min(numbers)
    maximum = max(numbers)
    average = sum(numbers) / len(numbers)
    return minimum, maximum, average

raw_numbers = input("Enter numbers separated by spaces (e.g. 4 1 9 2): ")
numbers_list = [int(n) for n in raw_numbers.split()] 

low, high, avg = get_stats(numbers_list)
print(f"Min: {low}, Max: {high}, Average: {avg}")




def greet_user(name, greeting="Hello"):
    return f"{greeting}, {name}!"

user_name = input("Enter your name: ")
custom_greeting = input("Enter a custom greeting: ")

print(greet_user(user_name))                          
print(greet_user(user_name, "Hi"))                     
if custom_greeting:                                    
    print(greet_user(user_name, greeting=custom_greeting))  



def describe_grade(score):
    if score >= 90:
        return "A"
    elif score >= 80:
        return "B"
    elif score >= 70:
        return "C"
    elif score >= 60:
        return "D"
    else:
        return "F"

score1 = int(input("Enter first exam score: "))
score2 = int(input("Enter second exam score: "))
score3 = int(input("Enter third exam score: "))

print(describe_grade(score1))
print(describe_grade(score2))
print(describe_grade(score3))