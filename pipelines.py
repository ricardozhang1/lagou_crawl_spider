# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import MySQLdb

class PicturespiderPipeline(object):
    def process_item(self, item, spider):
        return item


class LagouPipline(object):
    def __init__(self):
        self.conn = MySQLdb.connect(
            host='127.0.0.1',
            user='root',
            passwd='1234',
            db='mysql_test_01',
            port=3306,
            charset='utf8',
            use_unicode=True
        )
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        insert_sql = """
               insert into text_04(title,url,url_object_id,salary,job_city,work_years,degree_need,job_type,publish_time,job_advantage,company_name,company_url,tags )
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
           """
        self.cursor.execute(insert_sql, (item["title"], item["url"],item["url_object_id"], item["salary"],item["job_city"].strip('/'), item["work_years"].strip('/'),item["degree_need"].strip('/'), item["job_type"],item["publish_time"], item["job_advantage"],item["company_name"],item["company_url"], item["tags"]))
        self.conn.commit()
