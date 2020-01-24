import sys
import os.path   
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)   # 设置系统路径


import time
import re
from sys import modules
import paramiko
from config import USER_INFO,FILE_NAME,CHECK_STATUS
import xlrd
import xlwt
 
try:
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname='10.21.0.9', username=r'ne40_noc', password=r'+9*fAD-\7djnJGjH', allow_agent=False,
                look_for_keys=False, timeout=60, compress=True)
except Exception as e:
    print(e,'login func Error')


def takeAction(msg,ssh):
    """
    执行命令函数
    :return: result 拿到的数据结果
    """
    try:
        ssh_shell = ssh.invoke_shell()
        while True:
            line = ssh_shell.recv(1024)
            if line and line.endswith(b'>'):
                break


        ssh_shell.sendall(r'screen-length 0 temporary'+ '\n')
        while True:
            line = ssh_shell.recv(1024)
            if line and line.endswith(b'>'):
                break
        ssh_shell.sendall(msg + '\n')

        # get result lines
        lines = []
        while True:
            line = ssh_shell.recv(1024)
            lines.append(line.decode('utf-8'))
            if line and line.endswith(b'>'):
                break
        result = ''.join(lines)
        ssh.close()
        print(result)
        return result
    except Exception as e:
        print('异常：', e)

    finally:
        ssh.close()

takeAction('display device',ssh)