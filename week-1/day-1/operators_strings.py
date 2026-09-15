price = 49.99  # float (decimal number)
quantity = 3     # int (integer)

print(f"Total: ${price * quantity:.2f}")

total_minutes = 130
full_hours = total_minutes // 60
leftover_minutes = total_minutes % 60  
print(f"Full hours: {full_hours}, Leftover minutes: {leftover_minutes}")

message = "  Hello, World  "
result = message.strip().lower()  # Convert string to lowercase
print(result)

word = "snowflake"
first_word= word[0:4]
second_word= word[4:9]
print(first_word, second_word)