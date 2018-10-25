#!/usr/bin/python3

import json
from datetime import datetime as dt

#to read rss feeds
import feedparser

#to open article url
import urllib.request
#to parse html
from bs4 import BeautifulSoup


# articles per feed to download
maxArticles = 5

#to hold all scraped data from this running
thisScrape = []

with open('sitesToScrape.json') as data_file:
	sites = json.load(data_file)

#can reference this data as so:
# print(sites["cnn"]["link"])


# for site, value in sites.items():


#just use one for testing for now
site = 'cnn'
# category = 'top_stories'
for category in sites[site].keys():
	print(category)

	feed_link = sites[site][category]['link']

	print("Pulling articles from: ", site, " ", category, " ", sites[site][category]['link'])
	feed = feedparser.parse(feed_link)


	# maxArticles = 1
	for article in feed.entries[0:maxArticles]:
		scrapedArticle = {}
		scrapedArticle['site'] = site
		scrapedArticle['category'] = category
		scrapedArticle['feed_link'] = feed_link
		# print(article.keys())
		scrapedArticle['title'] = article['title']
		scrapedArticle['article_link'] = article['link']
		scrapedArticle['media'] = article['media_content']
		# print("Datetime: ", dt.now().strftime("%Y-%m-%d %H:%M:%S"))
		scrapedArticle['accessed_time'] = dt.now().strftime("%Y-%m-%d %H:%M:%S")
		
		# article_link_temp = 'http://rss.cnn.com/~r/rss/cnn_topstories/~3/QYbsqqnKZLo/index.html'
		# article_html = urllib.request.urlopen(article_link_temp)
		
		article_html = urllib.request.urlopen(scrapedArticle['article_link'])
		#don't need to use read for beautiful soup
		# article_html = article_html.read()
		
		#others parsers may perform better, or differently depending on site
		article_soup = BeautifulSoup(article_html, features="html.parser")
		article_text = ""
		# this zn-body__paragraph thing works for cnn, may not for all others
		# try story-body__link for bbc
		for paragraph in article_soup.find_all(class_="zn-body__paragraph"):
			article_text += paragraph.get_text()
			article_text += "\n"
		# print(article_text)
		
		scrapedArticle['body_paragraphs'] = article_text
		

		thisScrape.append(scrapedArticle)


try:
    with open('scraped_articles_{}.json'.format(dt.now().strftime("%Y-%m-%d")), 'w') as outfile:
        json.dump(thisScrape, outfile)
except Exception as e: print(e)

