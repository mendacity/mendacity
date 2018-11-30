Some dependencies that may need to be installed:

pip install feedparser
pip install newspaper3k

using urllib


Some helpful links
https://www.pythonforbeginners.com/feedparser/using-feedparser-in-python
https://stackoverflow.com/questions/14694482/converting-html-to-text-with-python
https://www.dataquest.io/blog/web-scraping-tutorial-python/

For viewing json:
http://jsonviewer.stack.hu/

Check out the sampleScrape.json



On AWS:
(the version we use doesn't have git preloaded?  should check into that...)
sudo yum install git

git clone https://github.com/hussainzaidi/mendacity

sudo yum install python36

sudo pip-3.6 install feedparser
sudo pip-3.6 install newspaper3k

copy dailyScripts.sh to /etc/cron.daily
crontab AWS_crontab
