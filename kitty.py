import requests
import json
import urllib.request

def getCatLink():
    url = "http://aws.random.cat/meow"
    response = requests.get(url)
    link = response.json()["file"]
    print("Getting a cat from: " + link)
    urllib.request.urlretrieve(link, "img/temp-cat.jpg")

