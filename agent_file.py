from agent import Agent

agent = Agent(name = 'Agent2', debug=True)

print("======================================== Ausgabe: Aktuelle Übersicht ========================================")
print("Aktuelle Bilanz:")
agent.print_balance()
print("\n")
print("Aktuelle Anzahl an Aktien:")
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
    "Cisco"]
for quote in quotes_list:
    agent.print_quotes(quote)

print("\n")
print("Aktuelle Blockchain:")
agent.print_chain()
print("\n")

# ======================================== Quotes ========================================
print("======================================== Funktionsaufruf: Quote ========================================")
# Get all Quotes
response_quote = agent.quote(debug=True)
if response_quote["Status"] == True:
    print("Preise der Aktien:")
    print(response_quote["Response"])

# Get "Amazon" Quote
print("Funktionsaufruf: Quote")
response_quote = agent.quote(["Lufthansa"], debug=True)
if response_quote["Status"] == True:
    print("Der Preis der Aktie Lufthansa beträgt:")
    print(response_quote["Response"]["Lufthansa"])
print("\n")

# ======================================== Buy & Sell ========================================
print("======================================== Funktionsaufrufe: Buy & Sell ========================================")
# Buy 
print("Transaction: Kauf von 2 Lufthansa Aktien")
response_buy = agent.buy("Lufthansa", 2, debug=True)
if response_buy["Status"] == True:
    print("Die Transaktion wurde erfolgreich durchgeführt.")
else:
    print("Die Transaktion konnte nicht durchgeführt werden.")

print("Aktuelle Bilanz:")
agent.print_balance()
print("Aktuelle Anzahl an Lufthansa Aktien:")
agent.print_quotes('Lufthansa')
#print("Neue Blockchain:")
#agent.print_chain()
print("\n")

# Sell 
print("Transaction: Verkauf von 1 Lufthansa Aktie")
response_sell = agent.sell("Lufthansa", 1, debug=True)
if response_sell["Status"] == True:
    print("Die Transaktion wurde erfolgreich durchgeführt.")
else:
    print("Die Transaktion konnte nicht durchgeführt werden.")

print("Aktuelle Bilanz:")
agent.print_balance()
print("Aktuelle Anzahl an Lufthansa Aktien:")
agent.print_quotes('Lufthansa')
#print("Neue Blockchain:")
#agent.print_chain()
print("\n")

# Buy (to much)
print("Transaction: Kauf von 200 Lufthansa Aktien")
response_buy = agent.buy("Lufthansa", 200, debug=True)
if response_buy["Status"] == True:
    print("Die Transaktion wurde erfolgreich durchgeführt.")
else:
    print("Die Transaktion konnte nicht durchgeführt werden.")

print("Aktuelle Bilanz:")
agent.print_balance()
print("Aktuelle Anzahl an Lufthansa Aktien:")
agent.print_quotes('Lufthansa')
#print("Neue Blockchain:")
#agent.print_chain()
print("\n")

# Sell (to much)
print("Transaction: Verkauf von 15 Lufthansa Aktien")
response_sell = agent.sell("Lufthansa", 15, debug=True)
if response_sell["Status"] == True:
    print("Die Transaktion wurde erfolgreich durchgeführt.")
else:
    print("Die Transaktion konnte nicht durchgeführt werden.")

print("Aktuelle Bilanz:")
agent.print_balance()
print("Aktuelle Anzahl an Lufthansa Aktien:")
agent.print_quotes('Lufthansa')
#print("Neue Blockchain:")
#agent.print_chain()
print("\n")

print("Aktuelle Blockchain:")
agent.print_chain()













