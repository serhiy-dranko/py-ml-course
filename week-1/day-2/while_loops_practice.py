count = 10

while count >= 1:
    print(count)
    count -= 1 

print("Liftoff!")

target = 7
guess = None

while guess != target:
    guess = int(input("Guess the number: "))
    if guess != target:
        print("Try again")

print("You got it!")

count = 0
while count < 5:
    print(count)
    count += 1