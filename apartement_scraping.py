# -*- coding: utf-8 -*-

#from bs4 import BeautifulSoup
#import urllib.request
#from selenium import webdriver
#import time
import requests
import json
import io

"""
Pitäisikö käyttää with-juttua kun kirjoitetaan tiedostoon?
"""

html_doc = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title"><b>The Dormouse's story</b></p>

<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>

<p class="story">...</p>
"""
#r = requests.get('https://api.github.com/events')

r = requests.get('https://asunnot.oikotie.fi/api/cards?cardType=100&limit=24&offset=0&sortBy=published_desc')
#r.encoding = 'ISO-8859-1'
as_json = r.json()
#print(as_json)
dump = json.dumps(as_json, indent=4, ensure_ascii=False)
#print(dump)
with io.open('test1.txt', 'w', encoding='utf-8') as f:
    f.write(dump)

#parsed = json.loads(str(as_json))
#print(type(as_json))

#print(r.json())

#link = 'https://asunnot.oikotie.fi/myytavat-asunnot?previousSearchId=1'
#link = 'https://asunnot.oikotie.fi/myytavat-asunnot'
#doc = urllib.request.urlopen(link);
#soup = BeautifulSoup(doc, 'html.parser')
#prices = soup.find_all("span", class_="ng-bind")
#prices = soup.select('strong') #soup.select('span[ng-bind="::card.price"]')
#lol= soup.select('body[ng-app="otAsunnot"]')
#print(prices)
#f = open('test.html', 'w')
#f.write(soup.prettify())
#print(soup.prettify())

"""driver = webdriver.PhantomJS(executable_path='')
driver.get("http://pythonscraping.com/pages/javascript/ajaxDemo.html")
time.sleep(3)
print(driver.find_element_by_id("content").text)
driver.close()"""