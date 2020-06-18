"""   
@Author:LZL  
@Time:2020/6/10 15:08       
"""  

import logging
import time
import pytest
import os

from common.com_log import ComLog
from common.com_config import ComConfig
from common.com_shell import ComShell


class Run:

    def __init__(self):
        ComLog().use_log()
        # 报告文件文件夹，防止生成的报告内容叠加
        self.time = time.strftime('%m-%d-%H-%M', time.localtime())
        self.report_path = ComConfig().get_report_path()

    def run_case(self):
        # 执行测试
        args = ["-s", "-n", "4", "--alluredir", F"{self.report_path[0]}"]
        pytest.main(args)
        # 生成测试报告
        cmd = F"allure generate --clean {self.report_path[0]} -o {self.report_path[1]}"
        ComShell().invoke(cmd)


if __name__ == '__main__':
    Run().run_case()

