Flask + Gunicorn + Nginx 部署

数据库 字段 Company表
name  企业名称
lagel_person 企业法人
register_capital 企业注册钱数
register_time 企业注册时间
tel 电话
area 区域（省份）
update_time 更新数据时间
company_id 详情返回的公司ID

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
请求company接口：
请求：http://47.98.36.72:10000/search/company_detail
POST
{ "name": "义乌",
   "page":"1",
   "per_page":"10"
}

响应：
{
  "result": [
    {
      "area": "江苏",
      "lagel_person": "周盈富",
      "name": "东台市安丰义乌小商品城有限公司",
      "register_capital": "2000万人民币",
      "register_time": "2008-05-22",
      "tel": "0515-85100688",
      "update_time": "2018-03-30"
    },
    {
      "area": "安徽",
      "lagel_person": "吴小平",
      "name": "临泉义乌国际商城市场管理有限公司",
      "register_capital": "200万人民币",
      "register_time": "2016-04-26",
      "tel": "6110009",
      "update_time": "2018-03-30"
    },
  ],
  "total_num": 710
}


'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
请求company_detail接口：
请求
post http://192.168.1.92:10000/search/company_detail
{ "company_id": ["827932","483135","1595405"]}
响应
{
  "483135": {
    "area": "浙江",
    "company_id": 483135,
    "lagel_person": "刘兵",
    "name": "义乌华邮科技园投资开发有限公司",
    "register_capital": "10000.000000万人民币",
    "register_time": "2016-10-13",
    "tel": "0579-85603777",
    "update_time": "2018-04-03"
  },
  "827932": {
    "area": "浙江",
    "company_id": 827932,
    "lagel_person": "明安龙",
    "name": "义乌华邮信息文化研究院有限公司",
    "register_capital": "1000.000000万人民币",
    "register_time": "2015-11-23",
    "tel": "0579-85603777",
    "update_time": "2018-04-03"
  },
  "1595405": {
    "area": "浙江",
    "company_id": 1595405,
    "lagel_person": "殷志远",
    "name": "义乌华邮资产运营管理有限公司",
    "register_capital": "1000.000000万人民币",
    "register_time": "2016-10-14",
    "tel": "18678808058",
    "update_time": "2018-04-03"
  }
}
'''''''''''''''''''''''''''''''''''''''

请求company_area接口：
http://47.98.36.72:10000/search/company_area
