
# 登陆用户配置
USER_INFO = {
    r"ne40_noc": r"+9*fAD-\7djnJGjH",
    r"noc": r"xc(%v+1@&&ASDF+",
    r"ikglobal_ops": r"kE+xax-ud7kQ6BG",
    r"zhihui": r"+9*fAD-\7djnJGjH",
}

# 打开的xlxs文件
FILE_NAME = 'huawei.xlsx'

# juniper配置
JUNIPER_FILE = 'juniper.xlsx'

# 验证模式
CHECK_STATUS = {
    1:'include',   # 存在
    2:'greater',  # 大于
    3:'lower',     # 小于
    4:'match',    # 匹配
    5:'between',   # 区间
    6:'uninclude',  # 不存在
    7:'equal',  # 相等
    8:'unbetween',  # 不再区间中
    9:'include_ti' # 替换后是否存在
}