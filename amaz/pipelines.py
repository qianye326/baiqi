# Define your item pipelines here
#encoding='utf-8'
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

class AmazPipeline:

    def process_item(self, item, spider):
        return item
