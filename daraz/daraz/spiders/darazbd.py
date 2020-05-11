# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request


class DarazbdSpider(scrapy.Spider):
    name = 'darazbd'
    allowed_domains = ['daraz.com.bd']
    start_urls = ['https://www.daraz.com.bd/smartphones/',
                'https://www.daraz.com.bd/kids-sanitizers/']

    def parse(self, response):
        links1= response.xpath("//div[@class='sku -gallery -validate-size ']/a[@class='link']/@href").extract()
        links2= response.xpath("//div[@class='sku -gallery ']/a[@class='link']/@href").extract()


        links= links1 + links2
        for link in links:
            print(link)
            yield Request(link, callback=self.parse_article, dont_filter=True)

        nextpageurl = response.xpath('//li/a[@title="Next"]/@href').extract_first()
        # absolute_next_page_url = response.urljoin(nextpageurl)
        yield scrapy.Request(nextpageurl, dont_filter=True)


    def parse_article(self,response):

        title =  response.xpath('//h1[@class="title"]/text()').extract()[0]
        BY = response.xpath('//div[@class="sub-title"]/a/text()').extract_first()
        price=response.xpath('//span[@dir="ltr"]/@data-price').extract_first()
        curr = response.xpath('//span[@data-currency-iso="NPR"]/text()').extract_first()
        price=curr[:2]+price
        seller = response.xpath('//a[@class="-name"]/text()').extract_first()
        rating = response.xpath('//article[@class="avg"]/div/span/text()').extract()[0]
        rating = rating.replace(',', '.')
        comments = response.xpath("//div[@class='content']/div[@class='detail truncate - txt']/text()").extract()
        user_comments = [x for x in comments if x != " "]
        user_comment_title = response.xpath("//div[@class='content']/div[@class='title']/text()").extract()
        user_rating = response.xpath("//div[@class='content']/div[@class='rating-stars']/div[@class='stars-container']/div[@class='stars']/@style").extract()
        user_rating = [x[7:9] for x in user_rating]
        category= response.xpath("//nav[@class='osh-breadcrumb']/ul/li/a/text()").extract()[1]

        yield{
            'Title':title,
            "Category":category,
            'Brand':BY,
            'Price':price,
            'Seller_name':seller,
            'Average_Product_rating':rating,
            'Buyer_comments':user_comments,
            'Buyer_comment_title':user_comment_title,
            'Buyer_product_review':user_rating,
            }
