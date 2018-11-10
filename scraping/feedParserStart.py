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

with open('sitesToScrape.json') as data_file:
	sites = json.load(data_file)

#can reference this data as so:
# print(sites["cnn"]["top_stories"]['link'])


for site in sites.keys():
#just use one for testing for now
# site = 'NYT'
# for i in range(0, 1):
	
# category = 'top_stories'
# for i in range(0, 1):
	for category in sites[site].keys():
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
			#special stuff.........
			if site == 'xinhua' and (category == 'health' or category == 'tech'):
				scrapedArticle['article_link'] = article['alink']
			else:
				scrapedArticle['article_link'] = article['link']
			
			# this doesn't work for every site...also, what even is it?
			# scrapedArticle['media'] = article['media_content']
			
			# print("Datetime: ", dt.now().strftime("%Y-%m-%d %H:%M:%S"))
			scrapedArticle['accessed_time'] = dt.now().strftime("%Y-%m-%d %H:%M:%S")
			
			# article_link_temp = 'http://rss.cnn.com/~r/rss/cnn_topstories/~3/QYbsqqnKZLo/index.html'
			# article_html = urllib.request.urlopen(article_link_temp)
			
			try: 
				article_html = urllib.request.urlopen(scrapedArticle['article_link'])
			# except urllib.error.HTTPError:
				# checksLogger.error('HTTPError = ' + str(e.code))
			# except urllib.error.URLError:
				# checksLogger.error('URLError = ' + str(e.reason))
			# except httplib.HTTPException:
				# checksLogger.error('HTTPException')
			# except Exception:
				# import traceback
				# checksLogger.error('generic exception: ' + traceback.format_exc())
			except Exception:
				print("Failed on " + site + " " + category + " " + scrapedArticle['article_link'] + "\n")
				continue			
			
			article_html = article_html.read()
			
			# print(newspaper.fulltext(article_html))
			article_text = newspaper.fulltext(article_html)
			
			scrapedArticle['body_paragraphs'] = article_text

			thisScrape.append(scrapedArticle)


try:
    with open('./data/scraped_articles_{}.json'.format(dt.now().strftime("%Y-%m-%d_%H:%M")), 'w') as outfile:
        json.dump(thisScrape, outfile)
except Exception as e: print(e)

