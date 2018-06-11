数据库 字段 Company表
name  企业名称
lagel_person 企业法人
register_capital 企业注册钱数
register_time 企业注册时间
tel 电话
area 区域（省份）
update_time 更新数据时间

#接口说明文档
## 依赖库
json
pandas
flask
redis
flask_mongoengine

## 数据库字段说明
hbase字段名	hbase列族	index_table
ID    rowkey    FALSE
PROVINCE	rowkey	FALSE
CITY	rowkey	FALSE
REG_CAPITAL	rowkey	FALSE
REG_TIME	A	TRUE
URBAN_AREA	A	FALSE
NAME	A	TRUE
TEL	A	TRUE
INDUSTRY	A	TRUE
LAGEL_PERSON	A	FALSE
REGISTER_CAPITAL	A	FALSE
REGISTER_TIME	A	FALSE
ADDRESS	A	FALSE
EMAIL	A	FALSE
BUSINESS_LICENSE	A	FALSE
STATUS	A	FALSE
WEB_SOURCE  A FALSE

## company接口
请求url   http://47.98.36.72:10000/search/company
请求消息体
```python
  {
    "PROVINCE":"江苏",
    "page":"1",
    "per_page":"10000",
    "startn":"100"
}
```
以下字段都可以作为搜索条件；
接口开发字段如下，大小写不区分：
    page页面号不太，默认为1；
    per_page每页展示数据量，默认为10；
    startn数据返回时的起始偏移量，默认为0；
    quick字段： 判断前端是否需要返回数据总数，统计总数需要几秒时间
        1.不太字段默认需要count
        2.携带字段无论值都不返回总数；
    city 城市；
    PROVINCE 省份 或者 area；
    REG_CAPITAL 企业规模 0表示未知（其他），1~5是枚举值
    REG_TIME  企业成立时间  0表示未知（其他），1~5是枚举值
    name  企业名
    INDUSTRY 行业类型
    URBAN_AREA 街道

    枚举值对应说明：
    REG_TIME  = {'1': [-1, 2018],
                          '2': [2017, 2013],
                          '3': [2012, 2008],
                          '4': [2007, 2003],
                          '5': [2002, -1],
                          }

    REG_CAPITAL= {'1': [100, 0],
                          '2': [200, 100],
                          '3': [500, 200],
                          '4': [1000, 500],
                          '5': [-1,1000],
                          }

响应消息体
```python
{
  "result": [
    {
      "ADDRESS": "中国江苏苏州市苏州市沧浪区乌鹊桥路",
      "BUSINESS_LICENSE": "未知",
      "CITY": "苏州",
      "EMAIL": "215000",
      "ID": "360994",
      "INDUSTRY": "一次性医用耗材公司",
      "NAME": "山东威高集团南京分公司",
      "PROVINCE": "江苏",
      "REGISTER_CAPITAL": "未知",
      "REGISTER_TIME": "未知",
      "REG_CAPITAL": "0",
      "REG_TIME": "0",
      "STATUS": "在业",
      "TEL": "13914037037",
      "URBAN_AREA": "沧浪区",
      "WEB_SOURCE": "shunqi"
    },
    {
      "ADDRESS": "中国江苏苏州市苏州市沧浪区盘胥路68号",
      "BUSINESS_LICENSE": "320503000028643",
      "CITY": "苏州",
      "EMAIL": "215000",
      "ID": "360995",
      "INDUSTRY": "汽车通讯公司",
      "NAME": "苏州智鼎电子科技有限公司",
      "PROVINCE": "江苏",
      "REGISTER_CAPITAL": "100万人民币",
      "REGISTER_TIME": "2014年",
      "REG_CAPITAL": "1",
      "REG_TIME": "2",
      "STATUS": "在业",
      "TEL": "13812779660",
      "URBAN_AREA": "沧浪区",
      "WEB_SOURCE": "shunqi"
    }
  ],
  "total_num": 123685
}
```

## 请求城市列表接口
请求url  http://47.98.36.72:10000/search/company_city
请求消息体
```python
  {
    "PROVINCE":"江苏"
}
```
响应消息体
```python
{
  "result": [
    "苏州",
    "无锡",
    "南京",
    "常州",
    "南通",
    "扬州",
    "徐州",
    "盐城",
    "镇江",
    "泰州",
    "淮安",
    "宿迁",
    "连云港"
  ]
}
```

## 请求街道区域列表接口
请求url  http://47.98.36.72:10000/search/company_urban_area
请求消息体
```python
  {
    "PROVINCE":"江苏","CITY":"南京"
}
```
响应消息体
```python
{
  "result": [
    "玄武区",
    "白下区",
    "秦淮区",
    "建邺区",
    "鼓楼区",
    "下关区",
    "浦口区",
    "栖霞区",
    "雨花台区",
    "江宁区",
    "六合区",
    "溧水县",
    "高淳县",
    "其他区"
  ]
}
```

## 请求来源列表接口
请求url  http://47.98.36.72:10000/search/company_source
请求消息体
```python
{
}
```
响应消息体
```python
{
  "result": [
    "shunqi",
    "tianyan"
  ]
}
```
## 请求行业类型列表接口
请求url  http://47.98.36.72:10000/search/company_industry
请求消息体
```python
{
}
```
响应消息体
```python
{
  "result": [
    "IT/通信/电子/互联网",
    "交通/运输/物流/仓储",
    "体育/休闲/旅游/娱乐",
    "其他",
    "农/林/牧/渔",
    "医疗/健康",
    "商业服务",
    "媒体",
    "房地产/建筑业",
    "政府/非盈利机构",
    "教育",
    "服务业",
    "法律",
    "生产/加工/制造",
    "能源/矿产/环保",
    "贸易/批发/零售/租赁业",
    "跨领域经营",
    "金融业"
  ]
}
```
