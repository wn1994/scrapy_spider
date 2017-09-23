# -*- coding: utf-8 -*-
import re
import urlparse
import datetime

import scrapy
from scrapy.http import Request
import scrapy.loader.processors
from ArticleSpider.items import MyArticlespiderTitem
from ArticleSpider.spiders.utils.common import get_md5
from ArticleSpider.items import ArticleItemLoader

class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts/']

    def parse(self, response):
        post_nodes = response.css("div.post.floated-thumb")
        for post_node in post_nodes:
            pic_url = post_node.css("div.post-thumb a img::attr(src)").extract_first("")
            pic_url = urlparse.urljoin(response.url,pic_url)
            url_post = post_node.css("div.post-meta p a.archive-title::attr(href)").extract_first("")
            url_post = urlparse.urljoin(response.url,url_post)             #学会urlparse.urlopen()方法
            yield Request(url=url_post,meta={'front_image_url':pic_url},callback=self.parse_detail)

        next_page = response.xpath("//a[@class='next page-numbers']/@href").extract_first("")
        if next_page:
            yield Request(url=urlparse.urljoin(response.url,next_page),callback=self.parse)


    def parse_detail(self, response):
        # title = response.xpath("//div[@class='entry-header']/h1/text()").extract_first("")
        # praise_num = response.xpath("//span[contains(@class,'vote-post-up')]/h10/text()").extract_first("")
        # if not praise_num:
        #     praise_num = 0
        # #如果要匹配多个class值，可以这样写//span[contains(@class,'bookmark-btn') and contains(@class,'href-style')]/text()
        # book_num = response.xpath("//span[contains(@class,'bookmark-btn')]/text()").extract_first("")
        # ma = re.match(r'.*?(\d+).*', book_num)
        # if ma:
        #     book_num = int(ma.group(1))
        # else:
        #     book_num = 0
        # comment_num = response.xpath("//div[@class='post-adds']/a[@href='#article-comment']/span/text()").extract_first("")
        # ma = re.match(r'.*?(\d+).*', comment_num)
        # if ma:
        #     comment_num = int(ma.group(1))
        # else:
        #     comment_num = 0
        # content = response.xpath("//div[@class='entry']").extract_first()
        # create_date = response.xpath("//p[@class='entry-meta-hide-on-mobile']/text()").extract_first("")
        # ma = re.match(r'[\s\S]*?(\d+/\d+/\d+).*',create_date)    #这里的正则不能用.*?的原因是.不能代表\n
        # if ma:
        #     create_date = ma.group(1)
        # tags_list = response.xpath("//p[@class='entry-meta-hide-on-mobile']/a/text()").extract() #extract()返回一个list
        # tags_list = [element for element in tags_list if not element.strip().endswith(u"评论")]
        # tag = ','.join(tags_list)       #学会这个方法


        #itemloader添加值默认返回一个list，原来是list的不变，是值的变为list
        article_itemloader = ArticleItemLoader(MyArticlespiderTitem(),response=response)
        article_itemloader.add_xpath('title',"//div[@class='entry-header']/h1/text()")
        article_itemloader.add_xpath('praise_num',"//span[contains(@class,'vote-post-up')]/h10/text()")
        article_itemloader.add_xpath('book_num',"//span[contains(@class,'bookmark-btn')]/text()")
        article_itemloader.add_xpath('comment_num',"//div[@class='post-adds']/a[@href='#article-comment']/span/text()")
        article_itemloader.add_xpath('content',"//div[@class='entry']")
        article_itemloader.add_xpath('create_date',"//p[@class='entry-meta-hide-on-mobile']/text()")
        article_itemloader.add_xpath('tag',"//p[@class='entry-meta-hide-on-mobile']/a/text()")
        article_itemloader.add_value('url',response.url)
        #pipeline--ArticlespiderImages的调用需要传入一个list
        article_itemloader.add_value('front_image_url',response.meta.get('front_image_url',''))
        article_itemloader.add_value('url_md5',get_md5(response.url))
        article_itemloader.add_value('front_image_path',u"can't get the path")

        article_item = article_itemloader.load_item()
        yield article_item

        # article_item = MyArticlespiderTitem()
        # article_item['title'] = title
        # article_item['praise_num'] = praise_num
        # article_item['book_num'] = book_num
        # article_item['comment_num'] = comment_num
        # article_item['content'] = content
        # try:
        #     create_date = datetime.datetime.strptime(create_date,'%Y/%m/%d').date()
        # except Exception:
        #     create_date = datetime.datetime.now().date()
        # article_item['create_date'] = create_date
        # article_item['tag'] = tag
        # article_item['url'] = response.url
        # article_item['front_image_url'] = [response.meta.get('front_image_url','')]
        # article_item['url_md5'] = get_md5(response.url)
        # yield article_item
