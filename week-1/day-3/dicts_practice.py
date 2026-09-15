product1 = {"name": "LG Smart TV", "price": 999.99, "in_stock": True, "quantity": 13}

print(product1["name"])
print(product1["price"])
print(product1["in_stock"])
print(product1["quantity"])

product1["discount_percent"] = 5

category = product1.get("category", "Uncategorized")
print(category)

for key, value in product1.items():
    print(f"{key}: {value}")

def calculate_final_price(product):
    return product["price"] * (1 - product["discount_percent"] / 100)

print(calculate_final_price(product1))


product2 = {"name": "Keyboard", "price": 25.00, "in_stock": True, "quantity": 50, "discount_percent": 0}

def compare_prices(product1, product2):
    price1 = calculate_final_price(product1)
    price2 = calculate_final_price(product2)
    return product1["name"] if price1 < price2 else product2["name"]

print(compare_prices(product1, product2))