try:
    value = int(input("Enter a number to divide 100 by: "))
    result = 100 / value
    print(f"100 / {value} = {result}")
except ValueError:
    print("That wasn't a valid number.")
except ZeroDivisionError:
    print("Can't divide by zero.")
finally:
    print("Attempt finished.")


def celsius_to_fahrenheit(celsius):
    return celsius * 9 / 5 + 32

try:
    temp_input = input("Enter temperature in Celsius: ")
    temp_celsius = float(temp_input)  # тут може впасти ValueError, якщо ввели не число
    temp_fahrenheit = celsius_to_fahrenheit(temp_celsius)
    print(f"{temp_celsius}°C = {temp_fahrenheit}°F")
except ValueError:
    print("That's not a valid temperature.")



def safe_divide(a, b):
    if b == 0:
        print("Warning: cannot divide by zero.")
        return None
    return a / b

num_a = float(input("Enter the first number: "))
num_b = float(input("Enter the second number (divisor): "))

result = safe_divide(num_a, num_b)
print(result)