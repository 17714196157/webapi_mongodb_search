from flask import Blueprint
from flask import request
from flask import jsonify
from flask_restful import Resource
from flask import current_app
import dbtool


company_entry = Blueprint('company', __name__)


# 接口
class company_api(Resource):
    def post(self):
        print("in get company_api")
        content = request.get_json()
        page = int(content['page'])
        per_page = int(content['per_page'])
        content.pop('page')
        content.pop('per_page')
        print(content)
        result, all_n = dbtool.db_search(content, page, per_page)

        if len(result) != 0:
            res_result = {**{"result": result}, **{"total_num": all_n}}
        else:
            res_result = {**{"result": None}, **{"total_num": all_n}}
        return jsonify(res_result)
