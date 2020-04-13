#coding:utf-8

import numpy as np
import pandas as pd
from pymongo import MongoClient

def createDetailArrayCategoryArray(df):
    """传入基础数据库, 简单划分(即只是归类, 关键字还是列表形式存储)为细分类和大分类"""

    # 条及以下的记录为细分类编码, 节及以上为大分类编码
    df_detail = df[df[u'条']!="None"][['code', 'cate']]
    df_category = df[df[u'条']=="None"][['code', 'cate']]
    print "细分类: ", df_detail.head()
    print "大分类: ", df_category.head()

    # 删除已有的2个集合collections
    db['detail_array'].remove()
    db['category_array'].remove()

    # 按照此划分依据将基础数据库划分为2个, 顺便保留每个文档的_id
    for c in df_detail['code']:
        for doc in db['tax_base'].find({'code': c}):
	    #print repr(doc).decode('unicode-escape')
            db['detail_array'].insert(doc)

    for c in df_category['code']:
        for doc in db['tax_base'].find({'code': c}):
	    #print repr(doc).decode('unicode-escape')
            db['category_array'].insert(doc)

def createDetailStringCategoryString():
    """将数据库中已有的detail_array集合中的各文档中的keywords列表拼接成字符串
        归为新集合detail_string中"""

    # 删除已有的2个集合collections
    db['detail_string'].remove()
    db['category_string'].remove()

    for doc in db['detail_array'].find({}):
	doc['keywords'] = u'、'.join(doc['keywords'])
        #print repr(doc).decode('unicode-escape')
	db['detail_string'].insert(doc)

    for doc in db['category_array'].find({}):
	doc['keywords'] = u'、'.join(doc['keywords'])
        #print repr(doc).decode('unicode-escape')
	db['category_string'].insert(doc)

if __name__ == "__main__":

    client = MongoClient(***
            username = '***',
            password = '***',
            authSource = '***',
            authMechanism = 'DEFAULT')
    db = client.test

    working_space = "/mnt/hgfs/windows_desktop/classification_and_coding/classification_and_coding/"
    path_file = working_space + "data/dictionary_building/国标商品与服务编码层级结构.xlsx"
    df_level_nation_std = pd.read_excel(path_file, dtype={'code': np.str})
    df_level_nation_std.fillna("None", inplace=True)
    #print df_level_nation_std.head()

    # 传入基础数据库划分依据, (划分tax_base)生成2个互补的编码集(detail_array,category_array)
#    createDetailArrayCategoryArray(df_level_nation_std)

    # 将detail_array/category_array关键字列表拼接成字符串，归到新集合中
    createDetailStringCategoryString()



