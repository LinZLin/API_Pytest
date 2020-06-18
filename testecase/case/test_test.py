"""
@Author:LZL
@Time:2020/6/10 14:28
"""

import allure
import pytest

from common.com_params import ComParams
from common.com_config import ComConfig
from common.com_log import ComLog
from common.com_manage import ComManage


@allure.epic("xxx")
@allure.feature("test接口")  # 功能点的描述
class Testtest:
    ComLog().use_log()
    yaml_path = ComConfig().test_params_path()
    # 获取指定测试用例的用例信息
    test_params = ComParams().test_params(yaml_path, yaml_name="test.yml")

    @allure.title("{title}")
    @pytest.mark.parametrize("param, title", test_params)
    def test_login(self, param, title):
        result = ComManage().assert_manner(param)
        assert result


if __name__ == '__main__':
    pytest.main(["-s", "test_test.py"])
