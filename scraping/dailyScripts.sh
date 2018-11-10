#!/bin/bash

cd ~/mendacity/scraping
./feedParserStart.py > ./logs/scrapeLog_`date +%d_%m_%y`.txt
