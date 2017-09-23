# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import re
import datetime
from scrapy.loader.processors import MapCompose,TakeFirst,Join
from scrapy.loader import ItemLoader

class ArticlespiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class ArticleItemLoader(ItemLoader):
    #TakeFirst()：取list中的第一项
    default_output_processor = scrapy.loader.processors.TakeFirst()


def return_praise_num(value):
    if not value:
        return str(0)
    else:
        return value

def return_num(value):
    ma = re.match(r'.*?(\d+).*', value)
    if ma:
        return int(ma.group(1))
    else:
        return str(0)

def return_date(value):
    ma = re.match(r'[\s\S]*?(\d+/\d+/\d+).*', value)  # 这里的正则不能用.*?的原因是.不能代表\n
    if ma:
        value = ma.group(1)
    try:
        value = datetime.datetime.strptime(value,'%Y/%m/%d').date()
    except Exception:
        value = datetime.datetime.now().date()
    return value

def return_tag(value):
    if u'评论' in value:
        return ''
    else:
        return value

def return_value(value):
    return value


class MyArticlespiderTitem(scrapy.Item):
    title = scrapy.Field()
    #MapCompose方法允许我们指定一系列的处理方法，Scrapy会将解析到的list中的值依次传递到每个方法中对值进行处理
    praise_num = scrapy.Field(input_processor = MapCompose(return_praise_num))
    book_num = scrapy.Field(input_processor = MapCompose(return_num))
    comment_num = scrapy.Field(input_processor = MapCompose(return_num))
    content = scrapy.Field()
    create_date = scrapy.Field(input_processor = MapCompose(return_date))
    tag = scrapy.Field(input_processor = MapCompose(return_tag),
                       output_processor = Join(u'  '))
    url = scrapy.Field()
    front_image_url = scrapy.Field(output_processor = MapCompose(return_value))
    front_image_path = scrapy.Field()
    url_md5 = scrapy.Field()
