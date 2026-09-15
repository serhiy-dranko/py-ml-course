movies = ["Die Hard", "John Wick", "The Dark Knight", "Back to the Future", "Good Luck, Have Fun, Don't Die", "Disclosure Day", "Thunderbolts"]

movies.append("The Day After Tomorrow")
movies.insert(2, "Fight Club")
movies.remove("Thunderbolts")

print(movies[::-1])          # reversed via slicing
print(movies[:3])            # first 3
print(movies[-2:])           # last 2

movies.sort()                # alphabetical order
print(movies)

print("Barbie" in movies)   # Check if "Barbie" is in the list