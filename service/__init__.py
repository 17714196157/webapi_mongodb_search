# -*- coding:utf-8 -*-

"""
File Name : '__init__'.py
Description:
Author: 'weicheng'
Date: '2018/4/2' '下午2:49'
"""

from flask import Flask
from service.actions.creat_log import creat_app_log
import os
from flask_mongoengine import MongoEngine
from service.views.company import company_entry, CompanyApi
from service.views.company_area import company_area_entry, CompanyArea
from service.views.company_detail import company_detail_entry, CompanyDetail

from flask_restful import Api


def creat_app():
    app = Flask(__name__)
    # 注册接口
    app.register_blueprint(company_entry)
    app.register_blueprint(company_area_entry)
    BasePath = os.path.dirname(os.path.abspath(__file__))
    ConfigPath = os.path.join(BasePath, "config")
    view = Api(app)
    view.add_resource(CompanyApi, '/search/company')
    view.add_resource(CompanyArea, '/search/company_area')
    view.add_resource(CompanyDetail, '/search/company_detail')
    app.config.from_json(os.path.join(ConfigPath, "app.json"))

    db = MongoEngine()
    db.init_app(app)
    return app


app = creat_app()
with app.app_context():
    app.app_logger = creat_app_log()
