import time
from mongoengine import Document, IntField, StringField, connect, DateTimeField ,Q
import mongoengine
from datetime import datetime
import re

conn_mongodb = connect('BusinessCircles', host='localhost', port=27017, username='guiji', password='guiji@123qwe')


print("has connect")

class Company(mongoengine.Document):
    ID = mongoengine.StringField(max_length=255, required=True)
    PROVINCE = mongoengine.StringField(max_length=255, null=True)
    CITY = mongoengine.StringField(max_length=255, null=True)
    REG_CAPITAL = mongoengine.StringField(max_length=255, required=True, default="0")
    REG_TIME = mongoengine.StringField(max_length=255, required=True, default="0")
    URBAN_AREA = mongoengine.StringField(max_length=255, null=True)
    NAME = mongoengine.StringField(max_length=255, required=True)
    TEL = mongoengine.StringField(max_length=255, required=True)
    INDUSTRY = mongoengine.StringField(max_length=255, null=True)
    LEGAL_PERSON = mongoengine.StringField(max_length=255, null=True)
    REGISTER_CAPITAL = mongoengine.StringField(max_length=255, null=True)
    REGISTER_TIME = mongoengine.StringField(max_length=255, null=True)
    ADDRESS = mongoengine.StringField(max_length=255, null=True)
    EMAIL = mongoengine.StringField(max_length=255, null=True)
    BUSINESS_LICENSE = mongoengine.StringField(max_length=255, null=True)
    STATUS = mongoengine.StringField(max_length=255, null=True)
    WEB_SOURCE = mongoengine.StringField(max_length=255, null=True)


res_db = Company.objects(Q(**{'PROVINCE__contains': '江苏', 'CITY__contains': '南京', 'REG_CAPITAL__contains': '0', 'REG_TIME__contains': '2'}))


for item in res_db:
    node_data = eval(item.to_json())
    print(type(node_data), node_data)
