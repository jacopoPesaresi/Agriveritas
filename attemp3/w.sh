#!/bin/bash
# pwd
# # Change to the project directory
# cd /home/jp/JPScraping/attemp3
# pwd

# echo "CIAO"

echo "" > myLogSpider.txt
# scrapy crawl try --logfile JPSLog.txt
#scrapy crawl try | tee JPLog.txt
if [[ ($# > 0) && ($1 == "C") ]]; then
    rm -r downloadR
    rm *Log*.txt
fi