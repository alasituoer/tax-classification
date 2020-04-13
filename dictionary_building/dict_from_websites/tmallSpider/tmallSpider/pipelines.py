# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from openpyxl import Workbook, load_workbook

class TmallspiderPipeline(object):
    # pass
    def __init__(self):
        self.file = open('tamllCrawlData-LoadPage.txt','w',encoding='utf-8')

    def process_item(self, item, spider):
        for i in item['segList']:
            self.file.write(item['title'] + "," + str(item['cateTitle']) + "," + str(item['segName']) + "," + i + "\n")
        return item

    def close_spider(self,spider):
        self.file.close()
#
#