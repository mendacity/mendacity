#!/usr/bin/python3

import json
import datetime

import feedparser


# articles per site to download
maxArticles = 15

#to hold all scraped data from this running
thisScrape = []

with open('sitesToScrape.json') as data_file:
	sites = json.load(data_file)

#can reference this data as so:
# print(sites["cnn"]["link"])


# for site, value in sites.items():

#just use one for testing for now
site = 'cnn'
category = 'top_stories'

print("Pulling articles from: ", site, " ", category, " ", sites[site][category]['link'])
feed_link = sites[site][category]['link']
feed = feedparser.parse(feed_link)

print(feed.keys())




#do some stuff here




try:
    with open('scraped_articles_{}.json'.format(datetime.datetime.now().strftime("%Y-%m-%d")), 'w') as outfile:
        json.dump(thisScrape, outfile)
except Exception as e: print(e)

