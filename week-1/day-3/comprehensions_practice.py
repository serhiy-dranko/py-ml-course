numbers = list(range(1, 21))

evens = [n for n in numbers if n % 2 == 0]
print(evens)

squares_over_10 = [n ** 2 for n in numbers if n > 10]
print(squares_over_10)


names = ["alice", "BOB", "Carla", "dave"]
capitalized = [name.capitalize() for name in names]
print(capitalized)

day2_numbers = [4, 8, 15, 16, 23, 42]
total_loop = 0
for n in day2_numbers:
    total_loop += n

total_comprehension = sum([n for n in day2_numbers])
print(total_loop, total_comprehension)

# Comment: for a plain sum, sum(day2_numbers) alone is clearest — wrapping it
# in a comprehension here is unnecessary, since there's no transformation or filter.