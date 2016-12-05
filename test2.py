import requests
import json
from googlefinance import getQuotes

ticker = "BLK"
print("submitting request")


try:
    data = getQuotes(str(ticker))
except:
    print("Problem loading ticker " + ticker)


print(data[0])
price = data[0]['LastTradePrice']
price = str(round(float(price),2))
print(ticker + "|" + price)
msg = "The current price of ticker " + ticker + " is " + price + " dollars. " 