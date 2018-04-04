from flask import Blueprint
from flask import request
from flask import jsonify
from flask_restful import Resource
from flask import current_app
from service.models import dbtool

company_detail_entry = Blueprint('company_detail', __name__)


# 接口
class CompanyDetail(Resource):
    def post(self):
        logger = current_app.app_logger
        res_result = {}
        logger.info("begin Post CompanyDetail")
        content = request.get_json()
        print(content)
        try:
            company_id_list = content['company_id']
            logger.info("request id_list=" + str(company_id_list))
            for company_id in company_id_list:
                result = dbtool.db_company_detail(company_id, logger=logger)
                res_result.update({company_id: result})
        except Exception as e:
            logger.error("ERROR Post CompanyDetail e=" + str(e))
            res_result = {}
        return jsonify(res_result)
