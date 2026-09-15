name = input("Fill your name: ")                                  # Ask name of the user for personal greeting lower
surname = input("Fill your surname: ")                            # Ask surname of the user for personal greeting lower
age = input("How old are you?: ")                                 # Ask age of the user for personal greeting lower
country = input("Which country do you live in?: ")                # Ask country of the user for personal greeting lower
city = input("Which city do you live in?: ")                      # Ask city of the user for personal greeting lower
language = input("What is your favorite programming language?: ") # Ask favorite programming language of the user for personal greeting lower

age_number = int(age)                                             # Convert age to integer for further calculations

years_until_100 = 100 - age_number                                # Calculate years until the user turns 100

print("==============================")                          # Print separator
print("PROFILE CARD!")                                           # Print profile card title
print("==============================")                          # Print separator
print("Name: {name} {surname}")                                  # Print name and surname
print(f"Age: {age_number}")                                       # Print age
print(f"Country: {country}")                                      # Print country
print(f"City: {city}")                                            # Print city
print(f"Favorite language: {language}")                           # Print favorite programming language
print(f"Years until 100: {years_until_100}")                      # Print years until the user turns 100
print("==============================")                          # Print separator