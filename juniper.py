import sys
import os.path   
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)   # 设置系统路径

import time
import re
from sys import modules
import paramiko
from config import USER_INFO,JUNIPER_FILE,CHECK_STATUS
import xlrd
import xlwt
from func import equal,lower,between,greater,uninclude,unbetween,include
result_data = []


def read_xls():
    """
    读取行数据
    :return: ssh对象
    """
    data = xlrd.open_workbook(filename=JUNIPER_FILE)
    table = data.sheets()[0]          #通过索引顺序获取 
    nrows = table.nrows               # 获取多少行
    ret = []
    for n in range(nrows):
        ret.append(list(map(lambda x:x.value,list(filter(lambda x:x.value, table.row(n)))))) 
    return ret


def read_col(args):
    """
    读列数据
    n：列数
    :return: ssh对象
    """
    data = xlrd.open_workbook(filename=JUNIPER_FILE)
    table = data.sheets()[0]          #通过索引顺序获取 
    ret = []
    for n in args:
        ret.append(list(map(lambda x:x.value,list(filter(lambda x:x.value, table.col(n))))))
    return ret
    

def login_fun(ip):
    """
    登陆函数
    :return: ssh对象
    """
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        for user, pwd in USER_INFO.items():
            try:
                ssh.connect(hostname=ip, username=user, password=pwd, allow_agent=False,
                            look_for_keys=False, timeout=60, compress=True)
                return ssh
            except Exception as e:
                print(e,'login Error')
                pass
        else:
            print("所有密码无法登陆")
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
            if line and line.endswith(b'> '):
                break

        # send command
        ssh_shell.sendall(msg + '\n')
        lines = []
        while True:
            line = ssh_shell.recv(1024)
            if line and line.endswith(b'> '):
                break
            lines.append(line.decode('utf-8'))
        result = ''.join(lines)
        ssh.close()
        return result
    except Exception as e:
        print('异常：', e)

    finally:
        ssh.close()


def main():
    result_data = []
    all_data = read_xls()  # 获取表格数据
    for one in all_data:
        print(one)
        try:
            statusID = one[3]  # 获取检查动作
            # 获取验证函数
            func_flex = CHECK_STATUS[int(statusID)]
            for ip in all_data:  # 循环ip
                if hasattr(modules[__name__],func_flex): # 反射
                    # 获取登陆对象
                    ssh = login_fun(ip[1].strip())
                    # ssh = login_fun(one[1].strip()) # 测试
                    if ssh:
                        # 动作后获取结果
                        ret_msg = takeAction(one[2],ssh)
                    else:
                        print('未返回ssh对象！')
                        with open('check_juniper.txt','w+',encoding='utf-8') as f:
                            for obj in result_data:
                                f.write(obj)
                        return
                    # 调用验证动作
                    rets = getattr(modules[__name__],func_flex)(one, ret_msg)
                    print(rets)
                    if rets:
                        result_data.append(f'{ip[1]},{one[2]}输出异常值：{" ".join(rets)} \n')

        except (ValueError,IndexError) as e:
            print('结束动作循环')
            break

    with open('check_juniper.txt','w+',encoding='utf-8') as f:
        for obj in result_data:
            # obj = list(map(lambda x:str(x),obj))
            # f.write(' '.join(obj))
            f.write(obj)



if __name__ == '__main__':
    main()
    