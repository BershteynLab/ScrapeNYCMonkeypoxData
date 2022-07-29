import scrapy
import re

class MonkeypoxSpider(scrapy.Spider):
    name = 'monkeypoxspider'
    start_urls = ['https://www1.nyc.gov/site/doh/health/health-topics/monkeypox.page']

    def parse(self, response):
        time = self.crawler.stats.get_value("start_time")
        for title  in response.xpath('//h2'):
            if title.xpath("./text()")[0].extract() == "Cases in NYC":
                rawText = title.xpath("../p[2]/text()")[0].extract()
                dateLine = re.search("(?i)(June|July|August|Aug\.|Aug|September|Sept\.|Sept|October|Oct\.|Oct|November|Nov\.|Nov|December|Dec\.|Dec|January|Jan\.|Jan|February|Feb\.|Feb|March|Mar\.|Mar|April|Apr\.|Apr|May) [0-9]{1,2}",
                          rawText)
                date = dateLine[0] if dateLine else dateLine
                countLine = re.search("(\d+|\d{1,3}(,\d{3})*)(\.\d+)? people", rawText)
                count = countLine[0].split(" ")[0] if countLine else None
                yield {"raw" : title.xpath("../p[1]/text()")[0].extract(), 
                        "scrape_time_UTC": time,
                        "count" : count,
                        "date" : date}
