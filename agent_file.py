from agent import Agent

def printHeader(header):
    print("=====================================================")
    print(header)
    print("=====================================================")

# Konstruktor 
# Create instance of Agent-Class
agent = Agent(name = 'muma1234', debug=True)

# Declaration available quotes
quotes_list = ["Amazon",
                "Apple", 
                "Lufthansa",
                "Bitcoin",
                "Tesla",
                "Pfizer",
                "Nokia",
                "SAP",
                "AMD",
                "Daimler",
                "Siemens Energy", 
                "Honeywell", 
                "Cisco",
                "1&1",
                "SMA",
                "Volkswagen",
                "Airbus",
                "Allianz",
                "Coca-Cola",
                "IBM",
                "NIKE",
                "Intel",
                "ATVI",
                "Netflix",
                "Googel",
                "Dogecoin",
                "Ethereum",
                "Infineon",
                "GameStop",
                "Boeing"]

# =====================================================
# Show user overview
# =====================================================
printHeader("User overview")

# Print current balance users
print("[Print] Current balance users:")
agent.print_balance(all=True)
print("\n")

# Print current balance
print("[Print] Current balance:")
agent.print_balance()
print("\n")

# Get current balance
print("[GET] Current balance:")
response_balance = agent.get_balance(all=False)
print(response_balance)
print("\n")

# Print current quotes owned
print("[Print] Current quotes owned:")
for quote in quotes_list:
    agent.print_quotes(quote)
print("\n")

# Get current quotes owned
print("[GET] Current quotes owned:")
for quote in quotes_list:
    response_quotes = agent.get_quotes(quote)
    print(response_quotes)
print("\n")

# Print current (local) blockchain
print("Current blockchain:")
agent.print_chain()
print("\n")

# =====================================================
# Show the current share price
# =====================================================
printHeader("Current share prices")

# Get all quotes
response_quote = agent.quote(quote_list=[], debug=True)
if response_quote["Status"] == True:
    print("Current share prices:")
    print(response_quote["Response"])
else:
    print("Error occurred")

# Get "Lufthansa" quote
response_quote = agent.quote(["Lufthansa"], debug=True)
if response_quote["Status"] == True:
    print("Current share price for Lufthansa:")
    print(response_quote["Response"]["Lufthansa"])
else:
    print("Error occurred")
print("\n")

# =====================================================
# Buy 2 Lufthansa quotes
# =====================================================
printHeader("Buy 2 Lufthansa quotes")

# Buy 
print("Transaction: Purchase of 2 Lufthansa shares")
response_buy = agent.buy(product="Lufthansa", quantity=2, debug=True)
if response_buy["Status"] == True:
    print("The transaction was carried out successfully.")
else:
    print("The transaction could not be carried out.")

# Print current balance
print("Current balance:")
agent.print_balance()

# Print current Lufthansa quotes owned
print("Current Lufthansa quotes owned:")
agent.print_quotes('Lufthansa')

# =====================================================
# Sell 1 Lufthansa quote
# =====================================================
printHeader("Sell 1 Lufthansa quote")

# Sell 
print("Transaction: Sell 1 Lufthansa quote")
response_sell = agent.sell("Lufthansa", 1, debug=True)
if response_sell["Status"] == True:
    print("The transaction was carried out successfully.")
else:
    print("The transaction could not be carried out.")

# Print current balance
print("Current balance:")
agent.print_balance()

# Print current Lufthansa quotes owned
print("Current Lufthansa quotes owned:")
agent.print_quotes('Lufthansa')


# =====================================================
# Buy (too much)
# =====================================================
printHeader("Buy (too much)")

# Buy (to much)
print("Transaction: Buy 20000 Lufthansa quotes")
response_buy = agent.buy("Lufthansa", 20000, debug=True)
if response_buy["Status"] == True:
    print("The transaction was carried out successfully.")
else:
    print("The transaction could not be carried out.")

# Print current balance
print("Current balance:")
agent.print_balance()

# Print current Lufthansa quotes owned
print("Current Lufthansa quotes owned:")
agent.print_quotes('Lufthansa')


# =====================================================
# Sell (too much)
# =====================================================
printHeader("Sell (too much)")

# Sell (to much)
print("Transaction: Sell 15000 Lufthansa quotes")
response_sell = agent.sell("Lufthansa", 15000, debug=True)
if response_sell["Status"] == True:
    print("The transaction was carried out successfully.")
else:
    print("The transaction could not be carried out.")

# Print current balance
print("Current balance:")
agent.print_balance()

# Print current Lufthansa quotes owned
print("Current Lufthansa quotes owned:")
agent.print_quotes('Lufthansa')



# =====================================================

# Print current (local) blockchain
print("Current blockchain:")
agent.print_chain()
print("\n")

