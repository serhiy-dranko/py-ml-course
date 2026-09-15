name = "Serhiy"        # str (string)
age = 32               # int (integer)
height = 1.80            # float (decimal number)
is_active = True        # bool (True/False)

print(name, type(name))
print(age, type(age))
print(height, type(height))
print(is_active, type(is_active))

number_str = "25"
number_int = int(number_str)  # Convert string to integer
result = number_int + 5
print(result, type(result))

number_pi = int(float("3.14"))
print(number_pi, type(number_pi))