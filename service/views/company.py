from flask import Blueprint
from flask import request
from flask import jsonify
from flask_restful import Resource
from flask import current_app
from service.models import dbtool

company_entry = Blueprint('company', __name__)


# 接口
class CompanyApi(Resource):
    def post(self):
        logger = current_app.app_logger
        logger.info("test")
        logger.info("in post company_api")
        content = request.get_json()
        try:
            page = int(content['page'])
            per_page = int(content['per_page'])
            content.pop('page')
            content.pop('per_page')
        except Exception:
            page = 1
            per_page = 10

        logger.info("request content", content)
        result, all_n = dbtool.db_search(content, page, per_page, logger=logger)
        if len(result) != 0:
            res_result = {**{"result": result}, **{"total_num": all_n}}
        else:
            res_result = {**{"result": None}, **{"total_num": all_n}}
        return jsonify(res_result)

