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
    # 定义为索引
    meta = {
         'indexes': ["name", "lagel_person", "area"]
    }


def QuerySetToDict(querySet):
    row_list = []
    for item in querySet:
        row = eval(item.to_json())
        row.pop('_id')
        if row.get('update_time', None) != "" and  row.get('update_time',None) != None:
            # print( time.strftime('%Y-%m-%d', time.localtime(int(row['register_time']['$date']/1000))) )
            row['update_time'] = time.strftime('%Y-%m-%d', time.localtime(int(row['update_time']['$date']/1000)))
        print(row)
        row_list.append(row)
    return  row_list
    pass




def db_search(search_dict, page=1, per_page=10):
    '''

    :param search_dict: 交集条件 同时满足字段值包含 给定字符串
    :return:
    '''
    all_n = 0
    search_condition = {}
    for field_name in search_dict:
        field_value = search_dict.get(field_name, "")
        if field_value != "" and field_value != None:
            search_condition.update({str(field_name).strip()+"__contains": search_dict[field_name].strip()})

    if len(search_condition) != 0:
        t1 = time.time()
        # all_n = Company.objects(db.Q(**search_condition)).count()
        result_search = Company.objects(db.Q(**search_condition)).paginate(page=page, per_page=per_page)

        all_n = result_search.total
        t2 = time.time()
        print(all_n, "查询匹配到的总个数 耗时:", t2-t1)

        if all_n != 0:
            # t1 = time.time()
            # result_search = Company.objects(db.Q(**search_condition)).paginate(page=page, per_page=per_page)
            # t2 = time.time()
            # print("查询每页数耗时:", t2-t1, dir(result_search))

            result_search = result_search.items   # 转化为
            result_search_list = QuerySetToDict(result_search)
            del result_search
            print("db_search return len=", type(result_search_list), len(result_search_list))
        else:
            result_search_list = []
    else:
        result_search_list = []
    return result_search_list, all_n



if __name__ == "__main__":
    # init_data_db()
    pass