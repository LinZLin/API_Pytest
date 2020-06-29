"""   
@Author:LZL  
@Time:2020/6/2 9:36       
"""

import requests
import json
import logging
from common.com_log import ComLog
import urllib3
import allure

"""
requests常用方法
只支持http/https，以及get、post请求
"""

# 忽略InsecureRequestWarning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
ComLog().use_log()


class ComRequest:
    req_session = requests.session()

    def send_request(self, request_data):
        global response
        try:
            self.url = request_data["url"].strip()
        except Exception as es:
            logging.error(F"请求数据的url获取失败，请求数据是：{request_data}，错误是{es}")
            raise (F"请求数据的url获取失败，请求数据是：{request_data}，错误是{es}")

        try:
            method = request_data["method"]
            header = request_data["header"]
            # yaml读取过来的json数据是[{}}]中字符串被'括起，需要替换成"
            data = self.is_json(request_data["data"])
            # data = eval(request_data['data'].replace("'", '"'))
            # data = json.loads(request_data['data'].replace("'", '"'))
            # if "json" in data.keys():  # 判断是否是json格式（测试用例中指定json）
            #     data = json.dumps(data["json"])
            # else:
            #     data = json.dumps(data)  # 非json格式则转回str
            if method == 'get':
                if not data.startswith("?"):
                    url = self.url + "?" + data

                allure.attach(name="请求地址：", body=F"{url}")
                allure.attach(name="请求方法", body=F"{method}")
                allure.attach(name="请求头：", body=F"{header}")
                allure.attach(name="请求data：", body=F"{data}")
                response = self.req_session.get(url=url, headers=header, params=data,
                                                verify=False)
            elif method == 'post':
                allure.attach(name="请求地址：", body=F"{self.url}")
                allure.attach(name="请求方法", body=F"{method}")
                allure.attach(name="请求头：", body=F"{header}")
                allure.attach(name="请求data：", body=F"{data}")
                response = self.req_session.post(url=self.url, data=data, headers=header,
                                                 verify=False)

        except Exception as e:
            logging.error(F'发送请求失败，请求url是：{self.url}，发生的错误是：{e}')
            raise (F'发送请求失败，请求url是：{self.url}，发生的错误是：{e}')

        return response

    def is_json(self, str):
        """
        判断data是否需要以json格式进行请求
        :param str:
        :return:
        """
        try:
            # yaml读取过来的json数据是[{}}]中字符串被'括起，需要替换成"
            # 同时转成json
            json_data = json.loads(str.replace("'", '"'))
            if "json" in json_data.keys():  # 判断是否是json格式（测试用例中指定json）
                data = json.dumps(json_data["json"])
            else:
                data = json.dumps(json_data)  # 非json格式则转回str
            return data
        except:
            # 如果非json格式，则返回值
            return str
