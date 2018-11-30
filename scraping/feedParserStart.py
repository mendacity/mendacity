#!/usr/bin/python3

import json
from datetime import datetime as dt
import feedparser				#to read rss feeds
import urllib.request			#to open article url
import newspaper				#to extract text from html

# articles per feed to download
maxArticles = 5

#to hold all scraped data from this running
thisScrape = []

#this holds the list of rss feeds to examine
with open('sitesToScrape.json') as data_file:
	sites = json.load(data_file)
#can reference this data as so:
# print(sites["cnn"]["top_stories"]['link'])


for site in sites.keys():
	for category in sites[site].keys():
		feed_link = sites[site][category]['link']

		print("Pulling articles from: ", site, " ", category, " ", sites[site][category]['link'])
		feed = feedparser.parse(feed_link)

		for article in feed.entries[0:maxArticles]:
			scrapedArticle = {}
			scrapedArticle['site'] = site
			scrapedArticle['category'] = category
			scrapedArticle['feed_link'] = feed_link
			scrapedArticle['title'] = article['title']
			#special stuff.........
			if site == 'xinhua' and (category == 'health' or category == 'tech'):
				scrapedArticle['article_link'] = article['alink']
			else:
				scrapedArticle['article_link'] = article['link']
			
			#save the current time article was scraped
			scrapedArticle['accessed_time'] = dt.now().strftime("%Y-%m-%d %H:%M:%S")
			
			try: 
				article_html = urllib.request.urlopen(scrapedArticle['article_link'])

			#there are many exceptions we might want to deal with
			# except urllib.error.HTTPError:
			# except urllib.error.URLError:
			# except httplib.HTTPException:
			# except Exception:
			except Exception:
				print("Failed on " + site + " " + category + " " + scrapedArticle['article_link'] + "\n")
				continue			
			
			#read the html
			article_html = article_html.read()
			
			#use newspaper to extract the text from the html
			article_text = newspaper.fulltext(article_html)
			
			#but just gran the main body
			scrapedArticle['body_paragraphs'] = article_text


			#and add this article to the set of articles from this running
			thisScrape.append(scrapedArticle)

#this should typically just work, without exception...
try:
    with open('./data/scraped_articles_{}.json'.format(dt.now().strftime("%Y-%m-%d_%H:%M")), 'w') as outfile:
        json.dump(thisScrape, outfile)
except Exception as e: print(e)

