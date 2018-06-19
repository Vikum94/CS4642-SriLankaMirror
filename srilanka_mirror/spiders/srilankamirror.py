import scrapy

class NewsItem(scrapy.Item):
    topic = scrapy.Field()
    link = scrapy.Field()
    intro = scrapy.Field()
    full_news = scrapy.Field()

class QuotesSpider(scrapy.Spider):
    name = "sri-lanka-mirror"
    base_url = 'https://srilankamirror.com'
    extension = '/news?start='
    limit_start = 1
    start_urls = ['https://srilankamirror.com/news?limitstart=1']

    def parse(self, response):
        for item in response.xpath('//h3[@class="catItemTitle"]'): 
            news_item = NewsItem()
            news_item['topic'] = item.css('a::text').extract_first().strip()
            news_item['link'] = self.base_url + item.css('a::attr(href)').extract()[0]
            detailed_news = scrapy.Request(news_item['link'], callback=self.get_full_news)
            detailed_news.meta['news_item'] = news_item
            yield detailed_news
        self.limit_start += 20
        next_page = self.base_url + self.extension + str(self.limit_start)
        yield scrapy.Request(url=next_page, callback=self.parse)


    def get_full_news(self, response):
        news_item = response.meta['news_item']
        news_item['intro'] = " ".join(response.xpath('//div[@class="itemIntroText"]/p/text()').extract())
        news_item['full_news'] = " ".join(response.xpath('//div[@class="itemFullText"]/p/text()').extract())
        yield news_item    