"""   
@Author:LZL  
@Time:2020/6/2 09:27
"""
import logging

import yaml
from common.com_log import ComLog
from pathlib import Path


"""
封装操作yaml的read
"""

class ComYaml:

    ComLog().use_log()

    @staticmethod
    def __read_yaml(yaml_path):
        """
        读取yaml文件
        :param yaml_path: yaml文件路径
        :return: {}
        """
        try:
            dict_data = yaml.load(open(yaml_path, 'r', encoding="utf-8"), Loader=yaml.FullLoader)
            return dict_data
        except Exception as es:
            logging.error(F'读取{yaml_path}文件出错，错误是{es}')
            raise (F'读取{yaml_path}文件出错，错误是{es}')

    def read_yaml(self, yml_path):
        """
        遍历文件夹下的所有yaml文件，拆分其中的dec和parameters，并设置为字典的键值对，返回字典
        :param yml_path: yaml文件路径 或 yaml文件路径
        :return: {dec1:parameters1, dec2:parameters2}
        """
        values_dict = {}
        # 判断路径是否是文件夹、获取该文件夹下所有的yml文件、并遍历
        try:
            if Path(yml_path).is_dir():
                for file in [x for x in list(Path(yml_path).glob("**/*.yml"))]:
                    data_dict = self.__read_yaml(file)
                    for test_name, parameters in data_dict.items():
                        values_dict[test_name] = parameters
            elif str(yml_path).endswith(".yml"):
                file = yml_path  # 为了log服务才这样赋值的
                data_dict = self.__read_yaml(file)
                for test_name, parameters in data_dict.items():
                    values_dict[test_name] = parameters
        except Exception as es:
            logging.error(F"解析{file}文件内容出错，错误是{es}")
            raise Exception
        return values_dict


