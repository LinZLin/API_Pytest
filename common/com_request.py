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

    def send_request(self, kwargs):
        global response
        try:
            self.url = kwargs['url'].strip()
        except Exception as es:
            logging.error(F"请求数据的url获取失败，请求数据是：{kwargs}，错误是{es}")
            raise (F"请求数据的url获取失败，请求数据是：{kwargs}，错误是{es}")

        try:
            method = kwargs['method']
            header = kwargs['header']
            # yaml读取过来的json数据是[{}}]中字符串被'括起，需要替换成"
            data = eval(kwargs['data'].replace("'", '"'))
            if "json" in data.keys():  # 判断是否是json格式
                data = json.dumps(data["json"])
            else:
                data = json.dumps(data)  # 非json格式则转回str
            if method == 'get':
                if not data.startswith("?"):
                    url = self.url + "?" + data

                allure.attach(name="请求地址：", body=F"{url}")
                allure.attach(name="请求方法", body=F"{method}")
                allure.attach(name="请求头：", body=F"{header}")
                allure.attach(name="请求data：", body=F"{data}")
                # allure.attach(F"请求cookies：{cookies}")
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
