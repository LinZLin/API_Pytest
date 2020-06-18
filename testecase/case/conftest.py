"""   
@Author:LZL  
@Time:2020/6/2 17:26       
"""

import pytest
import allure
from common.com_request import ComRequest

"""
pytest的conftest文件
"""


@pytest.fixture()
def ww_login(request):
    """
    中行外网登录
    """
    url = "https://h5no1.com/cbsp-zp/user/login/"
    header = {
        "Content-Type": "application/json;charset=UTF-8",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36        (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36"
    }
    # data = '{"params": "jWQY62JpDO8oVmOd6fAZPlfzmeYm0nma8Iyn7U8FyDvLlPzex1/djzShnzRFbxg+kjDBOUDfPi0JNzUNZzX0/AVRLNQGsxyACSHFPHFInUYFQXR3MgxTWW1FTlDgn+SqPxpzzgYa6celAYW4BL9UlRiqz+rCjOqTDO3RlngAMSE="}'
    data = '{"params":"g9kMQ1VlXqGlpNE893VJx8PhLLhxsylpe8hNq19SVwb4CwtpXYk64Hd4vWVwtDpbF3pZmb9HkOsM2/O7tWUuUQPrnhAypGgFmxwvHJeLD0qNkK2V01wY3L0dLo7HgNXvhwevhbZed4CUueTLeuG2uC2ujhD4zP2cCIh1A0fs10o="}'
    method = "post"
    datas = {
        "url": url,
        "data": data,
        "method": method,
        "header": header
    }
    ComRequest().send_request(datas)
