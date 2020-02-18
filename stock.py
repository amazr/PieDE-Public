import json
import requests
import math
import sched, time
import discord
import asyncio
from discord.ext import commands
import threading
from queue import Queue
import time

#API KEY
APIKEY="insert key here"


s = sched.scheduler(time.time, time.sleep)
watchList = {}


#Returns printable stock quote
def stock(symbol):
  jsonData = grabStock(symbol)
  if not 'Meta Data' in jsonData:
    returnString = "Symbol not found"
  else:
    mySymbol = jsonData["Meta Data"]["2. Symbol"]
    lastRefreshed = jsonData["Meta Data"]["3. Last Refreshed"]
    timeZone = jsonData["Meta Data"]["6. Time Zone"]
    recentPrice = float(jsonData["Time Series (5min)"][lastRefreshed]["4. close"])
    previousPrice = float(jsonData["Time Series (5min)"][lastRefreshed]["1. open"])
    delta = ""
    if previousPrice != recentPrice:
        delta = recentPrice - previousPrice
        delta = round(delta,3)
        if delta < 0:
            delta = " (-"+str(delta)+")"
        else:
            delta = " (+"+str(delta)+")"

    
    returnString = "$" + mySymbol.upper() + " is at $" + str(round(recentPrice,3)) + delta + " as of " + lastRefreshed + " " + timeZone
    return returnString

def grabStock(symbol):
    response = requests.get("https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol="+symbol+"&interval=5min&apikey="+APIKEY)
    jsonData = response.json()
    return (jsonData)

def alert(symbol):
    jsonData = grabStock(symbol)

    if not 'Meta Data' in jsonData:
        returnString = "Symbol not found"
    else:
        lastRefreshed = jsonData["Meta Data"]["3. Last Refreshed"]
        watchList[symbol] = float(jsonData["Time Series (5min)"][lastRefreshed]["4. close"])
        returnString = "$" + symbol.upper() + " added to watchlist!"
    return returnString

async def checkList():
    for key, value in watchList.items():
        thisValue = grabStock(symbol)
        if getChange(float(value),float(thisValue)) > 2:
            await channel.send("$"+ key + " has INCREASED " + getChange(float(value),float(thisValue)) + "%!")
        if getChange(float(value),float(thisValue)) < -2:
            await channel.send("$"+ key + " has DROPPED " + getChange(float(value),float(thisValue)) + "%!")

def getChange(current, previous):
    if current == previous:
        return 0
    try:
        return (abs(current - previous) / previous) * 100.0
    except ZeroDivisionError:
        return 0


    
s.enter(300, 1, checkList)
s.run(blocking=False)
