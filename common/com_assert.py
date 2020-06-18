"""   
@Author:LZL  
@Time:2020/6/4 9:29       
"""
import json
from jsonpath_rw import parse
import logging
import allure

from common.com_log import ComLog

"""
自定义assert
    # 类型
    # eq_list = []  # 相等
    # contains_list = []  # 包含
    # not_contains_list = []  # 不包含
    # lt_list = []  # 小于
    # le_list = []  # 小于等于
    # gt_list = []  # 大于
    # ge_list = []  # 大于等于
    # sw_list = []  # 以xx开头
    # ew_list = []  # 以xx结尾
"""


class ComAssert:
    ComLog().use_log()

    def eq(self, ex, re):
        try:
            assert str(ex) == str(re)
            return True
        except Exception as es:
            logging.error(F"eq判断失败，预期结果：{ex}，实际结果：{re}")
            raise (F"eq相等判断失败，预期结果：{ex}，实际结果：{re}")

    def contains(self, ex, re):
        try:
            assert str(ex) in str(re)
            return True
        except Exception as es:
            logging.error(F"contains判断失败，预期结果：{ex}，实际结果：{re}")
            raise (F"contains判断失败，预期结果：{ex}，实际结果：{re}")

    def not_contains(self, ex, re):
        try:
            assert str(ex) not in str(re)
            return True
        except Exception as es:
            logging.error(F"not_contains判断失败，预期结果：{ex}，实际结果：{re}")
            raise (F"not_contains判断失败，预期结果：{ex}，实际结果：{re}")

    def lt(self, ex, re):
        try:
            if isinstance(re, int) or isinstance(re, float):
                assert float(ex) < float(re)
            else:
                assert float(ex) < float(len(re))
            return True
        except Exception as es:
            logging.error(F"lt判断失败，预期结果：{ex}，实际结果：{re}")
            raise (F"lt判断失败，预期结果：{ex}，实际结果：{re}")

    def le(self, ex, re):
        try:
            # assert float(ex) <= float(re)
            if isinstance(re, int) or isinstance(re, float):
                assert float(ex) <= float(re)
            else:
                assert float(ex) <= float(len(re))
            return True
        except Exception as es:
            logging.error(F"le判断失败，预期结果：{ex}，实际结果：{re}")
            raise (F"le判断失败，预期结果：{ex}，实际结果：{re}")

    def gt(self, ex, re):
        try:
            # assert float(ex) > float(re)
            if isinstance(re, int) or isinstance(re, float):
                assert float(ex) > float(re)
            else:
                assert float(ex) > float(len(re))
            return True
        except Exception as es:
            logging.error(F"gt判断失败，预期结果：{ex}，实际结果：{re}")
            raise (F"gt判断失败，预期结果：{ex}，实际结果：{re}")

    def ge(self, ex, re):
        try:
            # assert float(ex) >= float(re)
            if isinstance(re, int) or isinstance(re, float):
                assert float(ex) >= float(re)
            else:
                assert float(ex) >= float(len(re))
            return True
        except Exception as es:
            logging.error(F"ge判断失败，预期结果：{ex}，实际结果：{re}")
            raise (F"ge判断失败，预期结果：{ex}，实际结果：{re}")

    def sw(self, ex, re):
        try:
            assert str(ex).startswith(str(re))
            return True
        except Exception as es:
            logging.error(F"sw判断失败，预期结果：{ex}，不以{re}开头")
            raise (F"sw判断失败，预期结果：{ex}，不以{re}开头")

    def ew(self, ex, re):
        try:
            assert str(ex).endswith(str(re))
            return True
        except Exception as es:
            logging.error(F"ew判断失败，预期结果：{ex}，不以{re}结尾")
            raise (F"ew判断失败，预期结果：{ex}，不以{re}结尾")

    def assert_result(self, assert_type, ex, re):
        """
        根据判断类型调用对应的判断方法
        :param assert_type:
        :param ex:
        :param re:
        :return:
        """
        try:
            if assert_type == "eq":
                return self.eq(ex, re)
            elif assert_type == "contains":
                return self.contains(ex, re)
            elif assert_type == "not_contains":
                return self.not_contains(ex, re)
            elif assert_type == "lt":
                return self.lt(ex, re)
            elif assert_type == "not_contains":
                return self.not_contains(ex, re)
            elif assert_type == "le":
                return self.le(ex, re)
            elif assert_type == "gt":
                return self.gt(ex, re)
            elif assert_type == "ge":
                return self.ge(ex, re)
            elif assert_type == "sw":
                return self.sw(ex, re)
            elif assert_type == "ew":
                return self.ew(ex, re)
        except Exception as es:
            logging.error(F"出现了非法的比较类型或者比较结果False：{assert_type}")
            raise (F"出现了非法的比较类型或者比较结果False：{assert_type}")

    def assert_code(self, assert_type, ex, response):
        """
        判断response.status_code是否如预期
        :param assert_type:
        :param ex:
        :param response:
        :return:
        """
        try:
            ex_code = ex[1]
            re_code = response.status_code
            return self.assert_result(assert_type, ex_code, re_code)
        except Exception as es:
            logging.error(F"code判断失败，判断类型是{assert_type}, 预期值：{ex_code}, 实际值：{re_code}")
            raise (F"code判断失败，判断类型是{assert_type}, 预期值：{ex_code}, 实际值：{re_code}")

    def assert_headers(self, assert_type, ex_value, response):
        """
        判断headers的内容是否如预期
        :param assert_type:
        :param ex_value:
        :param response:
        :return:
        """
        try:
            ex_headers = ex_value[1]
            headers_key = str(ex_value[0]).split(".")[1]
            re_headers = response.headers[headers_key]
            return self.assert_result(assert_type, ex_headers, re_headers)
        except Exception as es:
            logging.error(
                F"headers判断失败，判断类型是{assert_type}, 预期值：{ex_headers}, headers的key是：{headers_key},实际值：{re_headers}")
            raise (F"headers判断失败，判断类型是{assert_type}, 预期值：{ex_headers}, headers的key是：{headers_key},实际值：{re_headers}")

    @staticmethod
    def dict_value(key, data):
        """
        根据key层级获取data对应的value；jsonpath_rw的方法也可以实现（jsonpath-rw无法安装时用）
        :param key: str："one.two.three..."
        :param data: dict
        :return:
        """

        key_list = str(key).split(".")
        for now_key in key_list:
            if len(key_list) == 1:
                value = data[now_key]
                return value
            else:
                new_data = data[now_key]
                key = str.join(".", key_list[1:])
                return ComAssert.dict_value(key, new_data)  # 递归别忘了返回

    def assert_content(self, assert_type, ex_value, response):
        """
        判断content的内容是否如预期
        :param assert_type:
        :param ex_value:
        :param response:
        :return:
        """
        try:
            # 把"content.xx.yy"转成["xx.yy"]再转成"xx.yy"
            keys = str(ex_value[0].split("content.")[1:][0])
            ex_content = ex_value[1]

            json_content = json.loads(response.content)  # byte转dict
            # jsonpath_rw，根据key（"xx.yy.zz"），返回dict中该key的值
            re_content = [match.value for match in parse(str(keys)).find(json_content)][0]
            return self.assert_result(assert_type, ex_content, re_content)
        except Exception as es:
            logging.error(
                F"content判断失败或者响应文本不是json格式，判断类型是{assert_type}, 预期值：{ex_content}, content的key是：{keys},实际值：{re_content}")
            raise (
                F"content判断失败或者响应文本不是json格式，判断类型是{assert_type}, 预期值：{ex_content}, content的key是：{keys},实际值：{re_content}")
