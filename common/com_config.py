"""   
@Author:LZL  
@Time:2020/6/2 17:32       
"""
import time
from configparser import ConfigParser
import os

"""
封装config配置文件的方法
"""


class ComConfig:
    # section
    TEST_PATH = "test_path"

    # test_path
    PARAMS_FOLDER_PATH = "params_folder_path"

    def __init__(self):
        self.cp = ConfigParser()
        self.base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        config_path = os.path.join(self.base_path, "config", "config.ini")
        self.cp.read(config_path, encoding='utf-8')

    def __get_value(self, section, option):
        return self.cp.get(section, option)

    def test_params_path(self):
        # print(F"path:{os.path.join(self.base_path, self.__get_value(self.TEST_PATH, self.PARAMS_FOLDER_PATH))}")

        return os.path.join(self.base_path, self.__get_value(self.TEST_PATH, self.PARAMS_FOLDER_PATH))

    def get_report_path(self):
        xml_dir_path = os.path.join("report", time.strftime("%m-%d-%H") + "\\xml")
        html_dir_path = os.path.join("report", time.strftime("%m-%d-%H") + "\\html")

        xml_report_path = os.path.join(self.base_path, xml_dir_path)
        html_report_path = os.path.join(self.base_path, html_dir_path)
        return xml_report_path, html_report_path
