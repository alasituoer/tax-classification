#coding:utf-8
import pandas as pd
import numpy as np

if __name__ == "__main__":
    """对原始分类编码表进行预处理, 导入数据库后, 
	与最新的表做对比可得到历史累计增加的品类关键字"""

    working_space = "/mnt/hgfs/windows_desktop/classification_and_coding/"
    path_to_read = working_space + "data/dictionary_building/"
    filename_to_read = "P020161031602974964899.xlsx"
    filename_to_write = "nation_std_by_mingzhi.xlsx"

    nation_std = pd.read_excel(path_to_read + filename_to_read)
    nation_std.drop([0, 1, 2,], inplace=True)
    nation_std.columns = ['序号', '篇', '类', '章', '节', u'条', u'款',
	u'项', u'目', u'子目', u'细目', u'合并编码','商品和服务名称','说明','关键字']

#    print nation_std.head()

    # 填补关键字缺失值
    nation_std['关键字'][nation_std['关键字'].isnull()] =\
            nation_std['说明'][nation_std['关键字'].isnull()]
    nation_std['关键字'][nation_std['关键字'].isnull()] =\
            nation_std['商品和服务名称'][nation_std['关键字'].isnull()]
    keywd_null = nation_std[nation_std['关键字'].isnull()]

#    print nation_std.head()

    # 删除多余的列
    nation_std.info()
    del nation_std[u'子目']
    del nation_std[u'细目']
    nation_std[u'目'][nation_std[u'目'].notnull()]

#    print nation_std.head()

    # 清洗关键字列
    nation_std['关键字'] = nation_std['关键字'].str.replace(r'不包括.*。$','')
    nation_std['关键字'] = nation_std['关键字'].str.replace(r'（详见.*。$','')
    nation_std['关键字'] = nation_std['关键字'].str.replace(r'（详见.*）$','')
    nation_std['关键字'] = nation_std['关键字'].str.replace(r'(详见.*)$','')
    nation_std['关键字'] = nation_std['关键字'].str.replace(r'^指','')
    nation_std['关键字'] = nation_std['关键字'].str.replace(r'等$','')
#    nation_std['关键字'] = nation_std['关键字'].str.replace(r'包括$','')

    # 输出固化保存
#    nation_std.to_excel(path_to_read + filename_to_write)


