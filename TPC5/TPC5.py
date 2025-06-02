import json
import os
from datetime import datetime

# File to store the inventory
INVENTORY_FILE = 'stock.json'

# Coin values in cents
COIN_VALUES = {
    '1e': 100,
    '50c': 50,
    '20c': 20,
    '10c': 10,
    '5c': 5,
    '2c': 2,
    '1c': 1
}

def load_inventory():
    """Load the inventory from the JSON file."""
    if os.path.exists(INVENTORY_FILE):
        try:
            with open(INVENTORY_FILE, 'r') as file:
                return json.load(file)
        except json.JSONDecodeError:
            print("Machine: Error reading inventory file. Starting with empty inventory.")
            return []
    return []  # Return an empty list if the file doesn't exist

def save_inventory(inventory):
    """Write the inventory to the JSON file."""
    with open(INVENTORY_FILE, 'w') as file:
        json.dump(inventory, file, indent=4)

def display_products(inventory):
    """Display the list of available products."""
    print("Code | Product | Stock | Price")
    for item in inventory:
        print(f"{item['cod']} | {item['nome']} | {item['quant']} | €{item['preco']:.2f}")

def insert_coins(balance, coin_input):
    """Add coins to the balance and handle invalid coins."""
    coins = [coin.strip().lower() for coin in coin_input.split(',')]
    invalid_coins = []
    for coin in coins:
        if coin in COIN_VALUES:
            balance += COIN_VALUES[coin]
        else:
            invalid_coins.append(coin)
    if invalid_coins:
        print(f"Machine: Invalid coins detected: {', '.join(invalid_coins)}")
    return balance

def dispense_product(inventory, balance, product_code):
    """Dispense a product if balance and stock allow."""
    for item in inventory:
        if item['cod'] == product_code:
            if item['quant'] <= 0:
                print(f"Machine: Product \"{item['nome']}\" is out of stock.")
                return balance
            price_in_cents = int(item['preco'] * 100)  # Convert price to cents
            if balance >= price_in_cents:
                item['quant'] -= 1
                balance -= price_in_cents
                print(f"Machine: Dispensing product \"{item['nome']}\"")
                return balance
            else:
                print("Machine: Insufficient balance to complete your request.")
                print(f"Machine: Balance = €{balance // 100} {balance % 100}c; Price = €{item['preco']:.2f}")
                return balance
    print(f"Machine: Product code {product_code} not found.")
    return balance

def compute_change(balance):
    """Compute and return the change in coins."""
    if balance == 0:
        return "Machine: No change to return."
    change_coins = []
    remaining = balance
    for coin, value in sorted(COIN_VALUES.items(), key=lambda x: x[1], reverse=True):
        while remaining >= value:
            change_coins.append(coin)
            remaining -= value
    return f"Machine: Please take your change: {', '.join(change_coins)}"

def update_inventory(inventory, code, name, quantity, price):
    """Add or update a product in the inventory."""
    for item in inventory:
        if item['cod'] == code:
            item['quant'] += quantity
            item['preco'] = price
            print(f"Machine: Updated product {code}: Added {quantity} units, new price €{price:.2f}")
            return
    inventory.append({"cod": code, "nome": name, "quant": quantity, "preco": price})
    print(f"Machine: Added product {code}: {name}, {quantity} units, €{price:.2f}")

def run_vending_machine():
    inventory = load_inventory()
    print(f"Machine: {datetime.now().strftime('%Y-%m-%d')}, Inventory loaded, System ready.")
    print("Machine: Hello! Ready to assist you.")
    
    balance = 0
    while True:
        user_input = input("Enter command: ").strip().upper()
        if user_input == "LISTAR":
            display_products(inventory)
        elif user_input.startswith("MOEDA"):
            coin_input = user_input[5:].strip()
            balance = insert_coins(balance, coin_input)
            print(f"Machine: Balance = €{balance // 100} {balance % 100}c")
        elif user_input.startswith("SELECIONAR"):
            product_code = user_input[10:].strip()
            balance = dispense_product(inventory, balance, product_code)
            print(f"Machine: Balance = €{balance // 100} {balance % 100}c")
        elif user_input == "SAIR":
            print(compute_change(balance))
            print("Machine: Goodbye! See you next time.")
            save_inventory(inventory)
            break
        elif user_input.startswith("ADICIONAR"):
            parts = user_input.split()
            if len(parts) == 5:
                code, name, quantity, price = parts[1], parts[2], int(parts[3]), float(parts[4])
                update_inventory(inventory, code, name, quantity, price)
            else:
                print("Machine: Usage: ADICIONAR <code> <name> <quantity> <price>")
        else:
            print("Machine: Invalid command. Use LISTAR, MOEDA, SELECIONAR, ADICIONAR, or SAIR.")

if __name__ == "__main__":
    run_vending_machine()