from pymysql import connect
from pymongo import mongo_client
import  re
from mongoengine import Document, IntField, StringField, DateTimeField
import  mongoengine
from datetime import datetime
import time

class Company(Document):
    name = StringField(max_length=255, required=True)
    lagel_person = StringField(max_length=255, null=True)
    register_capital = StringField(null=True)
    # register_time = db.DateTimeField(null=True)
    register_time = StringField(null=True)
    tel = StringField(null=True)
    area = StringField(required=True, default="中国")
    update_time = DateTimeField(default=datetime.now)
    # 定义为索引
    meta = {
        'indexes': ["name", "lagel_person", "area"]
    }
#



# 读取mysql数据库数据
def get_data_mysql():
    # conn_mongodb = mongoengine.connect('admin', host='192.168.1.192', port=27017, username='qinyuchen', password='qq3@django')
    conn_mongodb = mongoengine.connect('admin', host='47.98.36.72', port=27017, username='guiji', password='guiji@123qwe')

    conn = connect(host='192.168.1.7', port=3306, database='tianyan', user='root', password='mysql', charset='utf8')
    cs = conn.cursor()
    # cs.execute('select * from tianyan_company where company_name = "龙岩新华都购物广场有限公司"')
    cs.execute('select * from tianyan_company')
    res = cs.fetchall()

    with open('tabledb.txt', mode='w', encoding='utf-8') as f:
        for index, item in enumerate(res):
            item = item[1:]
            name = item[0] if item[0] else ""
            lagel_person = item[2] if item[2] else ""
            register_capital = item[3] if item[3] != '-' else ""
            register_time = item[4] if item[4] else ""
            tel = item[5] if item[5] !="未知" else ""
            area = item[6] if item[6] else ""
            print(item)
            company_node = Company(
                name=name,
                lagel_person=lagel_person,
                register_capital=register_capital,
                register_time=register_time,
                tel=tel,
                area=area,
            )
            company_node.save()

            f.write(str(item)+"\n")
    cs.close()
    conn.close()


get_data_mysql()
