"""   
@Author:LZL  
@Time:2020/6/9 17:40       
"""
import subprocess

"""
执行shell语句的封装
"""

class ComShell:

    def invoke(self, cmd):
        output, errors = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        o = output.decode("utf-8")
        return o
