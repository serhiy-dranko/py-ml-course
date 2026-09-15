location = (6.4563074, 51.1315683)

print(location[0])
print(location[1])

# location[0] = 10 location[0] = 10    ~~~~~~~~^^^ TypeError: 'tuple' object does not support item assignment

def get_min_max(numbers):
    return min(numbers), max(numbers)

low, high = get_min_max([4, 1, 9, 2])
print(low, high)

