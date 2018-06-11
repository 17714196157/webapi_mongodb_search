import unittest
import requests
import json
import unittest.mock as mock


def client_post(url, data):
    headers_str = '''
    Accept:application/json
    Content-Type:application/json;charset=UTF-8'''.strip()
    headers = {}
    for item in headers_str.split("\n"):
        name = item.strip().split(":")[0].strip()
        value = item.strip().split(":")[1].strip()
        headers.update({name: value})
    print(type(data), data)

    response = requests.post(url=url, headers=headers, json=data)

    response.encoding = "utf-8"
    status_code = response.status_code
    result_json = eval(response.text)
    print(status_code)
    print(result_json)
    return status_code

class TestClient(unittest.TestCase):
    def test_success_request(self):
        data = {
                    "area":"江苏",
                    "page":"1",
                    "per_page":"10000",
                    "startn":"100",
        }
        url = r"http://localhost:10000/search/company/"
        self.assertEqual(client_post(url,data),'200')


data = {
                    "area":"江苏",
                    "page":"1",
                    "per_page":"10000",
                    "startn":"100",
        }
url = r"http://localhost:10000/search/company/"
client_post(url, data)


# from unittest import TestCase
# import unittest
# from service import app
# import os
# class Test(TestCase):
#     URL = "/search/company/"
#     def setUp(self):
#         self.app = app
#         self.client = self.app.test_client()
#     def test_post(self):
#         payload = {
#                 "area":"江苏",
#                 "page":"1",
#                 "per_page":"10000",
#                 "startn":"100",
#         }
#         resp = self.client.post(self.URL, json=payload).json
#         self.assertEqual(resp['code'], '0000')
#


# if __name__ == '__main__':
#     unittest.main()
#


# from service import app
# with app.test_client() as c:
#     rv = c.post('/search/company', json={
#     "area":"江苏",
#     "page":"1",
#     "per_page":"10000",
#     "startn":"100",
# })
#     json_data = rv.get_json()
#     print(json_data)
#     # assert verify_token(email, json_data['token'])
