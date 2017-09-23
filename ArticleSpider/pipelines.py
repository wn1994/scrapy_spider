# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
import json
from scrapy.pipelines.images import ImagesPipeline
import MySQLdb

class ArticlespiderPipeline(object):
    def process_item(self, item, spider):
        return item

class JSONWithPipeline(object):
    def process_item(self,item,spider):
        self.file = codecs.open('article.json','wb',encoding='utf-8')
        content = json.dumps(dict(item),ensure_ascii=False)
        self.file.write(content)
        return item
    def spider_closed(self,spider):
        self.file.close()

class ArticlespiderToMySQL(object):
    def __init__(self):
        self.conn = MySQLdb.Connect('127.0.0.1','root','wn3527825','articlespider',charset='utf8',use_unicode=True)
        self.cursor = self.conn.cursor()
    def process_item(self,item,spider):
        sql = "insert into articlespider(url_md5,url,title,create_date,content,praise_num,book_num,comment_num,tag," \
              "front_image_url,front_image_path) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        self.cursor.execute(sql,(item['url_md5'],item['url'],item['title'],item['create_date'],item['content'],
                                 item['praise_num'],item['book_num'],item['comment_num'],item['tag'],
                                 item['front_image_url'],item['front_image_path']))
        self.conn.commit()
        return item


class ArticlespiderImages(ImagesPipeline):
    def item_completed(self, results, item, info):
        if 'front_image_path' in item:
            for ok,value in results:
               path = value['path']
               item['front_image_path'] = path
        return item
