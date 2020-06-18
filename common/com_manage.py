"""   
@Author:LZL  
@Time:2020/6/3 15:17       
"""

import logging

from common.com_log import ComLog
from common.com_request import ComRequest
from common.com_assert import ComAssert
from common.com_config import ComConfig
from common.com_params import ComParams


"""
对请求数据进行判断，并调用ComParams进行数据的处理
"""


class ComManage:
    ComLog().use_log()

    def __init__(self):
        self.com_assert = ComAssert()
        self.config = ComConfig()
        self.com_params = ComParams()

    def validate_manner(self, validates_dict):
        """
        处理用例数据中的validates数据
        :param validates_dict:
        :return:
        """
        try:
            ex_dict = dict()

            # 类型
            eq_list = []  # 相等
            contains_list = []  # 包含
            not_contains_list = []  # 不包含
            lt_list = []  # 小于
            le_list = []  # 小于等于
            gt_list = []  # 大于
            ge_list = []  # 大于等于
            sw_list = []  # 以xx开头
            ew_list = []  # 以xx结尾

            for validate in eval(validates_dict):
                if "eq" in validate:
                    eq_list.append(validate["eq"])
                elif "contains" in validate:
                    contains_list.append(validate["contains"])
                elif "not_contains" in validate:
                    not_contains_list.append(validate["not_contains"])
                elif "lt" in validate:
                    lt_list.append(validate["lt"])
                elif "le" in validate:
                    le_list.append(validate["le"])
                elif "gt" in validate:
                    gt_list.append(validate["gt"])
                elif "ge" in validate:
                    ge_list.append(validate["ge"])
                elif "sw" in validate:
                    sw_list.append(validate["sw"])
                elif "ew" in validate:
                    ew_list.append(validate["ew"])

            ex_dict["eq"] = eq_list
            ex_dict["contains"] = contains_list
            ex_dict["not_contains"] = not_contains_list
            ex_dict["lt"] = lt_list
            ex_dict["le"] = le_list
            ex_dict["gt"] = gt_list
            ex_dict["ge"] = ge_list
            ex_dict["sw"] = sw_list
            ex_dict["ew"] = ew_list

            return ex_dict

        except Exception as es:
            logging.error(F"解析validate数据失败，数据为：{validates_dict}")
            raise es

    def request_manner(self, request_dict):
        """
        发送请求，同时处理依赖数据：

        处理variables、variables_data、relevance
        执行variables对应的用例，返回响应中relevance对应的值，并赋值给variables_data
        替换测试用例parameters中对应的variables_data。然后返回处理过后的parameters

        1：先确定需要执行的用例yml中的请求（因为一个yml会存在多个请求内容）
        2：判断variables_data的值，在对应用例的param中的relevance的value，
        3：再从该用例响应中提取出来
        4：接着替换掉之前的测试用例parameters中对应的variables_data。然后返回处理过后的parameters

        :param request_dict:
        :return:
        """
        # variables: [{'login': ['basic_id', 'audid']}, {'Basic': ['test_id']}]
        # variables_data: ['audid', 'basic_id']
        # relevance: {'id': 'content.data'}

        try:
            if "variables" in request_dict and "variables_data" in request_dict:

                # 处理variables的内容，去掉$，方便处理
                variables_data = request_dict["variables_data"]
                variables = request_dict["variables"]
                yaml_path = self.config.test_params_path()

                for variable in eval(variables):
                    # 获取依赖数据的值
                    for test_name in variable:
                        # print(F"variablesss:{variable}")
                        yaml_name = str(test_name) + ".yml"
                        variables_value = self.variables_value(yaml_path, yaml_name, variables_data)
                # 把依赖数据变量替换依赖数据的值
                request_dict = self.com_params.replace_request(request_dict, variables_value)
                # print(F"request_dict:{request_dict}")
            response = ComRequest().send_request(request_dict)
            return response
        except Exception as e:
            logging.error(F"请求发送失败，请求信息是：{request_dict}")
            raise (F"请求发送失败，请求信息是：{request_dict}")

    # 因为调用了Mannage类的的方法，两个类之间不能互相调用，所以移来这里
    def variables_value(self, yaml_path, yaml_name, variables_data):
        """
        获取依赖数据的值。比如
        variables: [{'login': ['data_value', 'code_value']}, {'Basic': ['test_id']}]
        variables_data: ['data_value', 'code_value']
        relevance: {'data_value': 'content.data', 'code_value': 'content.code'}
        根据variables，到对应的测试用例yaml（key）中，获取到其中拥有
        和variables的value全部一致的relevance的key的测试用例信息
        然后执行该测试用例，根据relevance的value，到respon中获取对应的值（依赖测试数据的值）
        :param yaml_path:
        :param yaml_name:
        :param variables_data:
        :return:
        """
        try:
            tests_params = ComParams().test_params(yaml_path, yaml_name)[0]  # 获取到想要执行用例yml的所有内容
            num = 0  # 记录依赖测试用例的请求执行次数，只需要执行一次即可
            for test_params in tests_params:
                if "relevance" in test_params:  # 判断存在relevance的请求信息内容
                    relevance_data = test_params["relevance"]
                    variables_value = []

                    if self.com_params.list_in_dict(variables_data, eval(relevance_data)):  # 获取有全部variables_data的请求信息内容
                        response = ComManage().request_manner(test_params)
                        num += 1
                        for variable_key in variables_data:
                            # 在relevance_data中，获取variables_data的key对应的value
                            variable_dict = self.com_params.relevance_value(variable_key,
                                                                            eval(relevance_data)[variable_key],
                                                                            response)
                            variables_value.append(variable_dict)
                    if num >= 1:
                        return variables_value
        except Exception as es:
            logging.error(F"被依赖用例{yaml_name}不存在依赖用例所需的依赖数据：{variables_data}")
            raise (F"被依赖用例{yaml_name}不存在依赖用例所需的依赖数据：{variables_data}")

    def assert_manner(self, request_dict):
        """
        根据测试用例的validate部分的判断类型（content/headers/status_code），调用不同的判断方法
        :param request_dict:
        :return: 全通过则返回True
        """
        try:
            # params = request_dict[0][0]
            # ex_validates = self.validate_manner(params["validate"])
            # response = self.request_manner(params)

            ex_validates = self.validate_manner(request_dict["validate"])
            response = self.request_manner(request_dict)

            for key in ex_validates:
                values = ex_validates[key]

                if len(values) >= 1:
                    asssert_type = key
                    for value in values:
                        value_start = value[0].split(".")[0]
                        if value_start.startswith("status_code"):
                            assert self.com_assert.assert_code(asssert_type, value, response)
                        elif value_start.startswith("headers"):
                            assert self.com_assert.assert_headers(asssert_type, value, response)
                        elif value_start.startswith("content"):
                            assert self.com_assert.assert_content(asssert_type, value, response)
            return True

        except Exception as es:
            logging.error(F"异常判断类型：{key}，判断值是{value}，响应数据是{response.content}")
            raise (F"异常判断类型：{key}，判断值是{value}，响应数据是{response.content}")

if __name__ == '__main__':

    yaml_path = ComConfig().test_params_path()
    data = ComParams().test_params(yaml_path, yaml_name="test.yml")[0][0]
    value = ComManage().assert_manner(data[0])
#     value = ComManage().assert_manner(data)
#     # value = ComManage().relevance_request_manner(data)
#     print(value)


