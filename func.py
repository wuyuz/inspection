
import re


def equal(data,msg):
    """
    相等状态函数
    """
    re_list = re.findall(data[4],msg)
    # 匹配到的数小于xlsx，就会被过滤掉
    s = set(re_list)
    if len(s)!=1:return list(s)  
    else:return False

def lower(data,msg):
    """
    小于状态函数
    :return: result 拿到的数据结果
    """
    re_list = re.findall(data[4],msg)
    # 匹配到的数小于xlsx，就会被过滤掉
    ret = list(filter(lambda x:int(x)>int(data[5]),re_list))
    if ret:return ret  
    else:return False

def between(data,msg):
    """
    区间状态状态函数
    :return: result 拿到的数据结果
    """
    re_list = re.findall(data[4],msg)
    # 匹配到区间的数xlsx，为正常
    less, more = data[5].split('-')
    ret = list(filter(lambda x:int(x)<int(less) and int(x)>int(more),re_list))
    if ret:return ret  
    else:return False

def greater(data,msg):
    """
    大于状态函数
    :return: result 拿到的数据结果
    """
    re_list = re.findall(data[4],msg)
    # 匹配到的数大于xlsx，就会被过滤掉
    ret = list(filter(lambda x:int(x)<int(data[5]),re_list))
    if ret:return ret  
    else:return False

def uninclude(data,msg):
    """
    不存在状态函数
    :return: result 拿到的数据结果
    """
    # 匹配到区间的数xlsx，为正常
    if data[4] in msg:return [f'存在异常值：{data[4]}',]
    else:return False

def unbetween(data, msg):
    """
    不存在区间内
    """
    re_list = re.findall(data[4],msg)
    # 匹配到区间的数xlsx，为正常
    less, more = data[5].split('-')
    ret = list(filter(lambda x:int(x)>int(less) and int(x)<int(more),re_list))
    if ret:return ret 
    else:return False

def include(data,msg):
    """存在关键字"""
    if data[4] in msg:return False  
    else:return [f'存在Alarm',]

def include_ti(data,msg):
    """替换一个后是否存在"""
    msg = msg.replace("Down","",1)
    if data[4] in msg:return False  
    else:return [f'存在Alarm',]
