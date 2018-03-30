from flask import Flask
from flask_restful import Api
from company import company_entry
from company import company_api
from creat_log import creat_app_log
import argparse
import os
from flask_mongoengine import MongoEngine



def creat_app():
    app = Flask(__name__)
    # 注册接口
    app.register_blueprint(company_entry)

    view = Api(app)
    view.add_resource(company_api, '/company')

    app.config['MONGODB_SETTINGS'] = {
        'db': 'admin',
        'username': 'qinyuchen',
        'password': 'qq3@django',
        'port': 27017,
        'host': '192.168.1.192',
    }
    # app.config['MONGODB_SETTINGS'] = {
    #     'db': 'BusinessCircles',
    #     'username': 'guiji',
    #     'password': 'guiji@123qwe',
    #     'port': 27017,
    #     'host': '127.0.0.1',
    # }

    db = MongoEngine()
    db.init_app(app)

    return app



if __name__ == "__main__":
    # 命令行解析,默认服务启动端口10000
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', default=10000, help='main service port', type=int)
    parser.add_argument('-d', '--debug_mode', action="store_true")
    args = parser.parse_args()

    app = creat_app()
    with app.app_context():
        app.app_logger = creat_app_log()

    if args.debug_mode:
        print('app starting on debug mode')
        app.run('0.0.0.0', port=args.port, debug=True, threaded=True)
    else:
        print('app running, work dir is:', os.getcwd())
        app.run('0.0.0.0', port=args.port, threaded=True, debug=True)