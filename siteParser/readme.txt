pip install scrapy
scrapy startproject nameProj .
scrapy genspider catalog domen.com

scrapy crawl catalog -o name.json