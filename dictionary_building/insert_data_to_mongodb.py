#coding:utf-8
import numpy as np
import pandas as pd
from pymongo import MongoClient
import uniout

def insertDataToMongoDB(df_datasets):
    """将所有数据先按最大5类划分，分为5个集合, 
        每个最大类别下的任一细分类别是一个文档"""
    # 根据code得到第一大类c1和第二大类c2的类别代码
    df_datasets['c1'] = df_datasets['code'].apply(lambda x: str(x)[0])
    df_datasets['c2'] = df_datasets['code'].apply(lambda x: str(x)[1:3])
    #df_datasets['c3'] = df_datasets['code'].apply(lambda x: str(x)[4:6])
#    print df_datasets.head()
	
    # 第一大类
    for c1 in df_datasets['c1'].unique():
        df_c1 = df_datasets[df_datasets['c1']==c1]
        one_c1_cate = df_c1[:1]['cate'].values[0]
        #print s, one_c1_cate, df_c1.shape
        # 第二大类
        for c2 in df_c1['c2'].unique():
            df_c2 = df_c1[df_c1['c2']==c2]
            # 得到该章的code和cate
            code_c2 = df_c2[:1]['code'].values[0]
            cate_c2 = df_c2[:1]['cate'].values[0]
            print c1, code_c2, cate_c2, df_c2.shape[0]
   
            #print df_c2.head()
            # 向数据库中插入数据(细分到第二大类的路径结构没有体现在数据库中)
            """
            for i in df_c2.index:
                code = df_c2.ix[i]['code']
                cate = df_c2.ix[i]['cate']
                keywords = df_c2.ix[i]['keywords']
                dict_to_write = {'code': code, 'cate': cate, 'keywords': keywords,}
                db[c1].insert(dict_to_write)
            """


def insertDataToOneCollection(df_datasets):
    """不区分大类别，存入所有数据到一个集合, 一个细分类别是一个文档"""
    #print df_datasets.head()
    for i in df_datasets.index[:10]:
        code = df_datasets.ix[i]['code']
        cate = df_datasets.ix[i]['cate']
        keywords = df_datasets.ix[i]['keywords']
        dict_to_write = {'code': code, 'cate': cate, 'keywords': keywords,}
        db['all_documents'].insert(dict_to_write)


def insertDataTest(df_datasets):
    #print df_datasets.head()
    for i in df_datasets.index:
        code = df_datasets.ix[i]['code']
        cate = df_datasets.ix[i]['cate']
        keywords = df_datasets.ix[i]['keywords']
        set_keywords = set(keywords.split(u'、'))
        set_keywords.discard(u'')
        list_keywords = [x.strip().replace(',', '') for x in list(set_keywords)]
        #print code, cate, list_keywords
        dict_to_write = {'code': code, 'cate': cate, 'keywords': list_keywords,}
        #print dict_to_write
        db['docs_first_commit'].insert(dict_to_write)


if __name__ == "__main__":
    working_space = "/mnt/hgfs/windows_desktop/classification_and_coding/"
    path_file = working_space + "data/dictionary_building/nation_std_first_commit.xls"
    df_datasets = pd.read_excel(path_file,
            dtype={'code': np.str_})#, index_col='code')
#    del df_datasets['id']
    print df_datasets.head()

    client = MongoClient("***", 27017)
    # 任一细分类别为一个文档, 划分5个集合, 每个集合下是各最大类别的所有细分文档
    #db = client.tax_classification_and_coding
    #insertDataToMongoDB(df_datasets)

    # 任一细分类别为一个文档, 所有文档存入一个集合all_documents
    #db = client.tax_classification_and_code
    #insertDataToOneCollection(df_datasets)

    # 尝试将keywords字符串(以顿号切分后)改为python集合存入
#    db = client.test
#    insertDataTest(df_datasets)




