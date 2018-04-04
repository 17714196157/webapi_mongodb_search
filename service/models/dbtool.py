# from mongoengine import Document, IntField, StringField, connect, DateTimeField
from datetime import datetime
from flask_mongoengine import MongoEngine
import time
db = MongoEngine()


class Company(db.Document):
    name = db.StringField(max_length=255, required=True)
    lagel_person = db.StringField(max_length=20, null=True)
    register_capital = db.StringField(null=True)
    # register_time = db.DateTimeField(null=True)
    register_time = db.StringField(null=True)
    tel = db.StringField(null=True)
    area = db.StringField(required=True, default="中国")
    update_time = db.DateTimeField(default=datetime.now)
    company_id = db.SequenceField(required=True)
    # 定义为索引
    meta = {
         'indexes': ["name", "lagel_person", "area"]
    }


def query_set_to_dict(querySet):
    row_list = []
    for item in querySet:
        row = eval(item.to_json())
        row.pop('_id')
        if row.get('update_time', None) != "" and  row.get('update_time',None) != None:
            row['update_time'] = time.strftime('%Y-%m-%d', time.localtime(int(row['update_time']['$date']/1000)))
        # print(row)
        row_list.append(row)
    return row_list
    pass


def paginate_test(res_db, page, per_page, logger=None):
    """
    分页查询mongodb的 功能
    :param res_db: 查询结果对象
    :param page: 第几页
    :param per_page: 每页元素个数
    :param logger: 日志对象
    :return:
    """
    if True:
        all_n = res_db.count()
        t1 = time.time()
        skip_n = (page - 1) * per_page
        result_search = res_db.skip(skip_n).limit(per_page)
        t2 = time.time()
        logger.info(str(type(result_search))+"paginate_test 查询匹配到的总个数 耗时" + str(all_n) + " " + str(t2 - t1))
    else:
        t1 = time.time()
        result_search = res_db.paginate(page=page, per_page=per_page)
        all_n = result_search.total
        result_search = result_search.items
        t2 = time.time()
        logger.info(str(type(result_search))+"paginate_test 查询匹配到的总个数 耗时" + str(all_n) + " " + str(t2 - t1))

    return result_search, all_n


def db_search(search_dict, page=1, per_page=10, logger=None):
    """
    :param search_dict: 交集条件 同时满足字段值包含 给定字符串
    :return:
    """
    logger.info("begin db_search")
    all_n = 0
    search_condition = {}
    for field_name in search_dict:
        field_value = search_dict.get(field_name, "")
        if field_value != "" and field_value != None:
            search_condition.update({str(field_name).strip()+"__contains": search_dict[field_name].strip()})

    if len(search_condition) != 0:
        logger.info("db_search search_condition" + str(search_condition)+" len="+str(len(search_condition)))

        try:
            res_db = Company.objects(db.Q(**search_condition))
            result_search, all_n = paginate_test(res_db, page, per_page, logger)
            result_search_list = query_set_to_dict(result_search)
            del result_search
        except Exception as e:
            logger.error("ERROR 查询" + str(e))
            result_search_list = []
    else:
        result_search_list = []
    return result_search_list, all_n


def db_area():
    result_search_list = Company.objects().distinct('area')
    return result_search_list

def db_company_detail(company_id, logger=None):
    logger.info("begin db_company_detail id="+str(company_id))
    try:
        company_id = int(company_id)
        result_search = Company.objects(company_id=company_id)
        if len(result_search) != 0:
            result_search_list = query_set_to_dict(result_search)
            result_search = result_search_list[0]
        else:
            result_search = ""
    except Exception as e:
        logger.error("ERROR  db_company_detail id=" + str( e))
        result_search = ""
    return result_search


if __name__ == "__main__":
    # init_data_db()
    pass