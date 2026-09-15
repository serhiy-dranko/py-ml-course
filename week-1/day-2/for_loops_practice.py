
fruits = ["apple", "banana", "cherry", "orange", "grape"]
for index, fruit in enumerate(fruits):
    print(f"I like {index}: {fruit}")

fruits = ["apple", "banana", "cherry", "orange", "grape"]
for fruit in fruits:
    print(f"I like {fruit}")

fruits = ["apple", "banana", "cherry", "orange", "grape"]
for i in range(5):        
    print(f"I like {fruits[i]}")

numbers = [4, 8, 15, 16, 23, 42]
total = 0 

for num in numbers:
    total += num 

print(total) 

for num in range(1, 101):
    if num % 7 == 0 and num % 11 == 0:
        print(f"Found: {num}")
        break