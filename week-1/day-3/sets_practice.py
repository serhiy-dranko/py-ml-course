week1_customers = {101, 102, 103, 104}
week2_customers = {103, 104, 105, 106}

print(week1_customers & week2_customers)   # both weeks
print(week1_customers | week2_customers)   # either weeks
print(week1_customers - week2_customers)   # only week 1
print(week2_customers - week1_customers)   # only week 2


numbers_with_duplicates = [1, 2, 2, 3, 3, 3, 4]
unique_numbers = set(numbers_with_duplicates)
print(unique_numbers)

# Sets are faster for membership checks (x in my_set) than lists because
# sets use a hash table internally (O(1) average lookup), while lists
# require scanning items one by one (O(n)) until a match is found.