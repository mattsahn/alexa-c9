
import requests
import json

ticker = "BLK"
print("submitting request")
portfolioAnalysisRequest = requests.get("https://www.blackrock.com/tools/hackathon/security-data", params= {'identifiers':ticker})
print("request received")

data = json.loads(portfolioAnalysisRequest.text)
print("json loaded")
print(data["success"])

if (data["success"] != True):
    print("security not found. exiting")
    quit()

assetType = data["resultMap"]["SECURITY"][0]["assetType"]

print(assetType)

if(assetType == "Stock"):
    print(ticker + " is a stock")
    description =  data["resultMap"]["SECURITY"][0]["description"]
    peRatio =  str(data["resultMap"]["SECURITY"][0]["peRatio"])
    msg = ticker + " is the stock for " + description + ". It has a P E ratio of " + peRatio
    print(msg)

if(assetType == "Fund"):
    print("this is a fund")
    morningstarCategory = data["resultMap"]["SECURITY"][0]["characteristicsMap"]["morningstarCategory"]
    print(morningstarCategory)

print("end")

