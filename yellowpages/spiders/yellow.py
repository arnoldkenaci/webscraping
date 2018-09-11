# -*- coding: utf-8 -*-
import scrapy
import os
import csv
import glob
from yellowpages import items
from scrapy.http import Request
from scrapy.loader import ItemLoader
from yellowpages.items import YellowItem
import string
class InfoSpider(scrapy.Spider):
    name = 'yellowpages'
    allowed_domains = ['yellowpagesalbania.com']
    start_urls = ['http://www.yellowpagesalbania.com/attivitas.html?cerca=&dove=']
    next_xpath = '//*[@id="paginatore_next"]/a/@href'

    def parse(self, response):
        
        print(response.url)

        urls = response.xpath('//*[@id="attivita_link"]/@href').extract()
        for url in urls:
            if '#' == url:
                pass
            else:
                url = response.urljoin(url)
                yield Request(url, callback=self.parse_info)
        relative_next_url = response.xpath('//*[@id="paginatore_next"]/a/@href').extract_first()
        absolute_next_url = 'http://www.yellowpagesalbania.com/attivitas.html?cerca=&dove=' + relative_next_url
        yield Request(absolute_next_url, callback=self.parse)
    def parse_info(self, response):
        cat = response.xpath('//*[@id="kat"]/text()').extract_first().strip()

        title = response.xpath('//*[@id="nome"]/text()').extract_first().strip()

        tel = response.xpath('//*[@id="tel"]/text()').extract_first()
        if tel:
            tel = tel.strip(" ")
        else:
            pass

        cel = response.xpath('//*[@id="cell"]/text()').extract_first()
        if cel:
            cel = cel.strip(" ")
        else:
            pass

        email = response.xpath('//*[@id="email"]/a/text()').extract_first()
        
        web = response.xpath('//*[@id="web"]/a/@href').extract_first()

        description = response.xpath('//*[@id="descr"]/text()').extract_first()
        if description:
            description = description.strip()
        else:
            pass

        geo = response.xpath('.//script[contains(., "lat")]/text()').extract_first()
        if geo:
            geo = geo.split()
            lat = geo[17].strip(',').strip('\'')
            lon = geo[19].strip(',').strip('\'')
        else:
            pass

        image_urls = response.xpath('//*[@id="logo"]/@src').extract_first()
        if image_urls:
            image_urls = 'http://www.yellowpagesalbania.com' + image_urls
        else:
            image_urls = None

        city = response.xpath('//*[@id="recapito"]/text()').extract_first().split()[0].strip(",")

        address = response.xpath('//*[@id="recapito"]/text()').extract_first()

        yield{
            
            'phone': cel,
            'city': city,
            'marker_image': image_urls,
            'location': address,
            'latitude': lat,
            'website': web,
            'title': title,
            'longitude': lon,
            'sub_kategori': cat,
        }
     
    