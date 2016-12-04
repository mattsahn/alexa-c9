import logging
import requests
import json
import urllib2
from googlefinance import getQuotes
from xml.etree import ElementTree as etree
from random import randint
from flask import Flask, render_template
from flask_ask import Ask, statement, question, session


app = Flask(__name__)

ask = Ask(app, "/")

logging.getLogger("flask_ask").setLevel(logging.DEBUG)


@ask.launch

def welome():

    welcome_msg = render_template('welcome')

    return question(welcome_msg)

@ask.intent("SecurityInfoIntent")
## User must say at least one letter for a security symbol. The remaining 4 slots will default to empty string
## if user doesn't say them. So 'FB' and 'GOOG' and 'MALOX' will all work.

def security_info(ticker):

    print("Intent: SecurityInfoIntent")
    print("raw response: " + ticker)
    ticker = str(ticker)
    ticker = filter(str.isalnum, ticker)
    ticker = ticker.upper()
    ticker_spaced = " ".join(ticker)
    print("input: " + ticker)

    try:
        data = getQuotes(str(ticker))
    except:
        print("Problem loading ticker " + ticker)
        return question("Problem loading ticker " + ticker_spaced + ". Please try again")

    print(data[0])
    price = data[0]['LastTradePrice']
    price = str(round(float(price),2))
    print(ticker + "|" + price)
    msg = "The current price of ticker " + ticker_spaced + " is " + price + " dollars. " 

    return question(msg) 

@ask.intent("SecurityInfoIntentBLK",default={"B":"","C":"","D":"","E":""})
## !! This intent is for the BLK API which I cannot access as of 11/19/2016. When it is available, will convert
## !! to using this intent/code.
## User must say at least one letter for a security symbol. The remaining 4 slots will default to empty string
## if user doesn't say them. So 'FB' and 'GOOG' and 'MALOX' will all work.

def security_infoBLK(A,B,C,D,E):

    print("Intent: SecurityInfoIntent")
    ticker = A + B + C + D + E
    print("input: " + ticker)
   
    SecurityRequest = requests.get("https://www.blackrock.com/tools/hackathon/security-data", params= {'identifiers':ticker})

    data = json.loads(SecurityRequest.text)

    print("json loaded")

    if (data["success"] != True):
        print("security not found. exiting")
        return question("I could not find that security. Please try again")

    assetType = data["resultMap"]["SECURITY"][0]["assetType"]

    print(assetType)

    if(assetType == "Stock"):
        print(ticker + " is a stock")
        description =  data["resultMap"]["SECURITY"][0]["description"]
        peRatio =  data["resultMap"]["SECURITY"][0]["peRatio"]
        #msg = ticker + " is the stock for " + description + ". It has a P E ratio of " + str(peRatio)
        msg = render_template('stockInfo',ticker=ticker,description=description,peRatio=str(peRatio))

    if(assetType == "Fund"):
        print("this is a fund")
        morningstarCategory = data["resultMap"]["SECURITY"][0]["characteristicsMap"]["morningstarCategory"]
        print(morningstarCategory)
        msg = ticker + " is a " + morningstarCategory + " fund"
   
    return question(msg) 

@ask.intent("MarketUpdateIntent")

def market_update():

    print("Intent: MarketUpdateIntent")
    blk_file = urllib2.urlopen('https://www.blackrockblog.com/feed/')
    #convert to string:
    blk_data = blk_file.read()
    #close file because we dont need it anymore:
    blk_file.close()

    #entire feed
    blk_root = etree.fromstring(blk_data)
    item = blk_root.findall('channel/item')

    stories = "Here are the three latest stories from the Blackrock blog: "
    num = 1

    for entry in item:
        #get description
        stories += " Number " + str(num) + ". "
        stories += entry.findtext('description')
        if num == 3:
            break
        num += 1

    stories += " Go to blackrock blog dot com to read the full stories."
    print("reponse : " + stories)
    return question(stories)


#@ask.intent("YesIntent")

#def next_round():

#    numbers = [randint(0, 9) for _ in range(3)]

#    round_msg = render_template('round', numbers=numbers)

#    session.attributes['numbers'] = numbers[::-1]  # reverse

#    return question(round_msg)


#@ask.intent("AnswerIntent", convert={'first': int, 'second': int, 'third': int})

#def answer(first, second, third):

#    winning_numbers = session.attributes['numbers']

#    if [first, second, third] == winning_numbers:

#        msg = render_template('win')

#    else:

#        msg = render_template('lose')

#    return statement(msg)

@ask.intent("AMAZON.StopIntent")

def stop():
    print ("Intent: AMAZON.StopIntent")
    return statement("Goodbye.")

if __name__ == '__main__':

    app.run(debug=True)
