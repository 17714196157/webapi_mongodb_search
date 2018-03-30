# mongodb_-
mongodb作为数据库，flask启动一个web服务端口
数据库 字段 Company表
name  企业名称
lagel_person 企业法人
register_capital 企业注册钱数
register_time 企业注册时间
tel 电话
area 区域（省份）
update_time 更新数据时间

POST  http://192.168.1.92:10000/company
{ "name": "义乌",
   "page":"1",
   "per_page":"10"
}

响应
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
