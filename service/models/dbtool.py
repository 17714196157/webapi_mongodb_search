# from mongoengine import Document, IntField, StringField, connect, DateTimeField
from datetime import datetime
from flask_mongoengine import MongoEngine
import time
import redis
import json
import os
import pandas as pd
from functools import wraps  # 装饰器的作用是将func函数的相关属性复制到clock中

db = MongoEngine()
pool = redis.ConnectionPool(host='127.0.0.1', port=6379, db='0')

servie_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
df = pd.read_excel(os.path.join(servie_path, os.path.join('config', 'file_map.xlsx')), encoding='utf-8',
                   eindex_col=False)

def init_map_field(df):
    """
    字段名映射成对应那个列族的那个字段
    file_map.xlsx 是需要输入的字段映射关系
    :return:
    """
    map_field={}
    for n in df.index:
        map_field.update({df.at[n, 'hbase字段名']: df.at[n, 'hbase字段名']})
    return map_field

map_field = init_map_field(df)
map_field.update({"ID": "ID"})
map_field.update({"WEB_SOURCE": "WEB_SOURCE"})
map_field.update({"AREA": "PROVINCE"})      # area也当成省份字段
print("map_field:", map_field)
column_name_list = df['hbase字段名'].values.tolist()
column_name_list.insert(0, "ID")
column_name_list.append("WEB_SOURCE")
print("column_name_list:", column_name_list)

def cache_func_redis(timeout=100):
    """
    缓存函数
    :param timeout:
    :return:
    """
    # pool = redis.ConnectionPool(host='127.0.0.1', port=6379, db='0')
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # print("args:", args)
            logger = args[-1]
            # lst_dct = sorted([{k: kwargs[k]} for k in kwargs], key=lambda d:d.keys()[0])
            # lst = [str(d.values()[0]) for d in lst_dct]
            k = '_'.join([func.__name__, str(args[0])])
            # print("cache k",k)
            r = redis.StrictRedis(connection_pool=pool)
            d = r.get(k)
            if d:
                logger.info("命中缓存   k=" + str(k))
                d = d.decode()
                # print(d,type(d))
                res = json.loads(d)['res']
                return res
            else:
                # print("未命中缓存   k=" + str(k))
                logger.info("未命中缓存   k=" + str(k))
                res = func(*args, **kwargs)
                # print("cache res:", res)
                d = json.dumps({
                    'res': res
                })
                r.set(k, d)
                r.expire(k, timeout)

                return res
        return wrapper
    return decorator

def cache_flag(key):
    r = redis.StrictRedis(connection_pool=pool)
    d = r.get(key)
    if d:
        return True
    else:
        return False

class Company(db.Document):
    ID = db.StringField(max_length=255, required=True)
    PROVINCE = db.StringField(max_length=255, null=True)
    CITY = db.StringField(max_length=255, null=True)
    REG_CAPITAL = db.StringField(max_length=255, required=True, default="0")
    REG_TIME = db.StringField(max_length=255, required=True, default="0")
    URBAN_AREA = db.StringField(max_length=255, null=True)
    NAME = db.StringField(max_length=255, required=True)
    TEL = db.StringField(max_length=255, required=True)
    INDUSTRY = db.StringField(max_length=255, null=True)
    LAGEL_PERSON = db.StringField(max_length=255, null=True)
    REGISTER_CAPITAL = db.StringField(max_length=255, null=True)
    REGISTER_TIME = db.StringField(max_length=255, null=True)
    ADDRESS = db.StringField(max_length=255, null=True)
    EMAIL = db.StringField(max_length=255, null=True)
    BUSINESS_LICENSE = db.StringField(max_length=255, null=True)
    STATUS = db.StringField(max_length=255, null=True)
    WEB_SOURCE = db.StringField(max_length=255, null=True)

    # # 定义为索引
    # meta = {
    #      'indexes': ["ID", "PROVINCE", "CITY"]
    # }


@cache_func_redis(timeout=36000)
def count_all(search_condition_str, search_condition, logger=None):
    """
    统计总数
    :param search_condition_str:
    :param search_condition:
    :param logger:
    :return:
    """
    t1 = time.time()
    logger.info("begin count all" + str(search_condition_str))
    try:
        res_db = Company.objects(db.Q(**search_condition))
        all_n = res_db.count()
    except Exception as e:
        logger.error("count 总数异常")
        all_n = 0
    t2 = time.time()
    logger.info("end count all all_n=" + str(all_n))
    logger.info("count_all 消耗时间=" + str(t2-t1))
    return all_n


@cache_func_redis(timeout=36000)
def result_return(search_condition_str_skip, search_condition, skip_n, per_page, logger):
    """
    分页返回满足条件的数据
    :param search_condition_str_skip:
    :param search_condition:
    :param skip_n:
    :param per_page:
    :param logger:
    :return:
    """
    t1 = time.time()
    res_db = Company.objects(db.Q(**search_condition))
    result_search = res_db.skip(skip_n).limit(per_page)
    result_search_list = []
    for item in result_search.as_pymongo():
        item.pop("_id")
        # print(type(item), item)
        result_search_list.append(item)
    t2 = time.time()
    logger.info("result_return 查询匹配 消耗时间：" + str(t2-t1))
    return result_search_list


def db_search(search_dict, page=1, per_page=10,startn=0, quick=None, logger=None):
    """
    搜索接口 后台函数
    :param search_dict: 交集条件 同时满足字段值包含 给定字符串
    :return:
    """
    logger.info("begin db_search")
    search_condition = {}
    search_condition_str = ""
    for field_name in search_dict:
        field_value = search_dict.get(field_name, "").strip()
        db_field_name = map_field.get(field_name.upper().strip(), None)

        if db_field_name is not None and field_value != "":
            search_condition_str = search_condition_str + "%s-%s" % (db_field_name, field_value)
            search_condition.update({str(db_field_name) +  "__contains": field_value})
            # search_condition.update({str(field_name).strip().upper() + "__exists": field_value})
    if len(search_condition) != 0:
        logger.info("db_search search_condition:" + ",".join([str(search_condition), str(len(search_condition))]))

        try:
        # if True:
            print("quick:", quick)
            if quick is None:
                all_n = count_all(search_condition_str, search_condition, logger)
            else:
                all_n = 0
            skip_n = startn + (page - 1) * per_page
            logger.info("page,per_page,skip_n=" + ",".join([str(page), str(per_page), str(skip_n)]))
            search_condition_str_skip = search_condition_str + "-{skip_n}-{per_page}".format(per_page=per_page,
                                                                                             skip_n=skip_n)
            result_search_list = result_return(search_condition_str_skip, search_condition, skip_n, per_page, logger)
        except Exception as e:
            logger.error("ERROR 查询"+str(e))
            result_search_list = []
    else:
        result_search_list = []
        all_n = 0
    return result_search_list, all_n



@cache_func_redis(timeout=36000)
def db_area(logger):
    result_search_list = Company.objects().distinct('PROVINCE')
    return result_search_list


def db_company_detail(company_id, logger=None):
    logger.info("begin db_company_detail id="+str(company_id))
    try:
        company_id = int(company_id)
        result_search = Company.objects(company_id=company_id)
        if len(result_search) != 0:
            result_search_list = result_search.as_pymongo()
            result_search = result_search_list[0]
        else:
            result_search = ""
    except Exception as e:
        logger.error("ERROR  db_company_detail id=" + str(e))
        result_search = ""
    return result_search


@cache_func_redis(timeout=36000)
def db_CITY(PROVINCE, logger=None):
    logger.info("begin  CITY list  for PROVINCE:"+str(PROVINCE))
    t1 = time.time()
    if PROVINCE is None:
        return []
    result_search_list = Company.objects(PROVINCE=PROVINCE).distinct('CITY')
    t2 = time.time()
    logger.info("return CITY list cost time="+str(t2-t1))
    return result_search_list


@cache_func_redis(timeout=36000)
def db_URBAN_AREA(PROVINCE, CITY, logger=None):
    logger.info("begin  URBAN_AREA list  for CITY:"+str(CITY))
    if PROVINCE is None or CITY is None:
        return []
    t1 = time.time()
    result_search_list = Company.objects(PROVINCE=PROVINCE, CITY=CITY).distinct('URBAN_AREA')
    t2 = time.time()
    logger.info("return URBAN_AREA list cost time="+str(t2-t1))
    return result_search_list


@cache_func_redis(timeout=36000)
def db_source(logger=None):
    logger.info("begin  source list ")
    t1 = time.time()
    result_search_list = Company.objects().distinct('WEB_SOURCE')
    t2 = time.time()
    logger.info("return source list cost time="+str(t2-t1))
    return result_search_list

@cache_func_redis(timeout=36000)
def db_industry(logger=None):
    logger.info("begin  industry list ")
    t1 = time.time()
    # result_search_list = Company.objects().distinct('INDUSTRY')
    result_search_list = ["IT/通信/电子/互联网","交通/运输/物流/仓储","体育/休闲/旅游/娱乐","其他","农/林/牧/渔","医疗/健康","商业服务","媒体","房地产/建筑业","政府/非盈利机构","教育","服务业","法律","生产/加工/制造","能源/矿产/环保","贸易/批发/零售/租赁业","跨领域经营","金融业"]
    t2 = time.time()
    logger.info("return industry list cost time="+str(t2-t1))
    return result_search_list

if __name__ == "__main__":
    # init_data_db()
    pass