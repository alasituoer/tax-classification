#coding:utf-8
import pandas as pd
import numpy as np
from pymongo import MongoClient


def updateManualTest(dict_tobe_updated):
    """指定待更新(或添加)的code和list of keywords
        查看该品类数据库已有的关键字列表
	将预添加的关键字列表合并进已存在列表中
    """

    for c in dict_tobe_updated.keys():
        list_kws = dict_tobe_updated[c]
	print u"预添加关键字列表:", c, repr(list_kws).decode('unicode-escape')

        # 对拟添加的关键字列表去重
        func = lambda x,y: x if y in x else x+[y]
        list_kws = reduce(func, [[], ] + list_kws)
        print "去重后的预添加关键字列表:", c, repr(list_kws).decode('unicode_escape')

        # 检测拟添加的关键字是否已存在现有数据库
        for doc in db['tax_base'].find({'code': c}):
            print "该品类现有的关键字列表:", repr(doc['keywords']).decode('unicode-escape')
            # 只取数据库中现有关键字列表内没有的那些
            list_kws = [kw for kw in list_kws if kw not in doc['keywords']]
            print '最终预添加的关键字列表 ', repr(list_kws).decode('unicode-escape')
            # 如果去重检测后的待添加关键字列表不为空, 则进行更新操作
            if len(list_kws) != 0:
                db['tax_base'].update({'code': c},
                        {'$set': {'keywords': doc['keywords'] + list_kws}})
        # 输出该品类更新后的关键字列表
        for doc in db['tax_base'].find({'code': c}):
            print "更新后的现有关键字列表: ", repr(doc['keywords']).decode('unicode-escape')


def returnDataFrameOfTobeUpdatedFile(df):
    """"""

    df_kws_final = pd.DataFrame(columns=['code', 'cate', 't1', 't2', 'list_kws'])

    # 第一部分59wujin
    df_59wujin_p1 = df['59wujin_p1']
    df_59wujin_p2 = df['59wujin_p2']

    #print df_59wujin_p1.head()
    for i in df_59wujin_p1.index:
        t1 = df_59wujin_p1.ix[i]['t1']
        t2 = df_59wujin_p1.ix[i]['t2']
        #print t1, t2
	df_kws = df_59wujin_p2[(df_59wujin_p2['t1']==t1) & (df_59wujin_p2['t2']==t2)]
        #print df_kws
	df_kws = df_kws.reindex(columns=['code', 'cate', 't1' , 't2', 'list_kws'])
	df_kws.loc[:, 'code'] = str(df_59wujin_p1.ix[i]['code'])
	df_kws.loc[:, 'cate'] = df_59wujin_p1.ix[i]['cate']
        #print df_kws

	df_kws_final = pd.concat([df_kws_final, df_kws])
    df_kws_final.index = range(len(df_kws_final))
#    print df_kws_final.index.size
#    print df_kws_final.head()

    # 第二、三部分 taobao、1688
    df_taobao = df['taobao'].reindex(columns=['code', 'cate', 't1', 't2', 'list_kws'])
    df_taobao['code'] = df_taobao['code'].apply(lambda x: str(x))
    df_1688 =  df['1688'].reindex(columns=['code', 'cate', 't1', 't2', 'list_kws'])
    df_1688['code'] = df_1688['code'].apply(lambda x: str(x))
#    print df_taobao.index.size
#    print df_taobao.head()
#    print df_1688.index.size
#    print df_1688.head()

    df_kws_final = pd.concat([df_kws_final, df_taobao, df_1688])
#    print df_kws_final.index.size
#    print df_kws_final

#    df_kws_final.to_excel("/mnt/hgfs/windows_desktop/classification_and_coding/classification_and_coding/data/dictionary_building/机械五金合并文件.xlsx", index=False)
    
    return df_kws_final



def updateBulkOperation(df):
    """导入有预更新类别及其关键字列表的DataFrame格式数据, 进行批量更新
        df.head() : code, cate, keyword"""

    for code in df['code'].unique():
        cate = df[df['code']==code].iloc[0]['cate']
        list_kws = df[df['code']==code]['keyword'].tolist()
        print "___预更新关键字列表", code, cate, repr(list_kws).decode('unicode-escape')

        # 对拟添加的关键字列表去重
        func = lambda x,y: x if y in x else x+[y]
        list_kws = reduce(func, [[], ] + list_kws)
        print "___去重后的预更新关键字列表:", code, cate, repr(list_kws).decode('unicode-escape')

        # 检测拟添加的关键字是否已存在现有数据库
        for doc in db['tax_base'].find({'code': code}):
            print "___该品类现有的关键字列表: ", repr(doc['keywords']).decode('unicode-escape')
            # 只取数据库中现有关键字列表内没有的那些
            list_kws = [kw for kw in list_kws if kw not in doc['keywords']]
            print '___最终确定的预添加关键字列表:', repr(list_kws).decode('unicode-escape')

            # 如果去重检测后的待添加关键字列表不为空, 则进行更新操作
            if len(list_kws) != 0:
                db['tax_base'].update({'code': code},\
                        {'$set': {'keywords': doc['keywords'] + list_kws}})
        # 输出该品类更新后的关键字列表
        for doc in db['tax_base'].find({'code': code}):
            print "___更新后的关键字列表: ", repr(doc['keywords']).decode('unicode-escape')
        print '\n'


def updateSelf():
    """数据库自更新, 处理部分类别中的关键字仍是是由顿号分隔(系导入错误)的多个关键字"""

    func = lambda x,y: x if y in x else x+[y]

#    for doc in db['tax_base'].find({'code': '1040105000000000000'}):
#        if 'li' in 'limingzhi':

    for doc in db['tax_base'].find():
        list_kws = doc['keywords']
        if u'、' in repr(list_kws).decode('unicode-escape'):

            list_kws = doc['keywords']
            print doc['code'], doc['cate'], repr(list_kws).decode('unicode-escape')
	    list_kws_t = []
            for kw in list_kws:
                if u'、' in kw:
                    list_kws_t.extend(kw.split(u'、'))
                else:
                    list_kws_t.append(kw)
            list_kws = reduce(func, [[], ] + list_kws_t)
            print doc['code'], doc['cate'], repr(list_kws).decode('unicode-escape')
            db['tax_base'].update({'code': doc['code']}, {'$set': {'keywords': list_kws}})
	print '\n'




if __name__ in "__main__":

    # 无认证连接和有认证连接数据库
#    client = MongoClient("***", 27017)
    client = MongoClient('***', 
            username = '***',
            password = '***',
            authSource = '***',
            authMechanism = 'DEFAULT',)
    db = client.test

    working_space = "/mnt/hgfs/windows_desktop/classification_and_coding/classification_and_coding/"

    # 指定有限个预更新类别及其关键字列表
#    dict_tobe_updated = {'1030201990000000000': [u'披萨',]}
#    updateManualTest(dict_tobe_updated)

    # 导入有预更新类别及其关键字列表的excel文件
    # 进行批量更新
    """
    path_file = working_space + "data/dictionary_building/from_samples/" +\
            "预更新品类及其关键字.xlsx"
    df_tobe_updated = pd.read_excel(path_file, sheet_name='final', dtype={'code': np.str})
    print df_tobe_updated[:4]
    updateBulkOperation(df_tobe_updated[:4])
    """

    # 数据库自更新, 部分类别中的关键字是由顿号分隔的多个关键字
#    updateSelf()

    # 读入机械及五金待更新excel文件, 返回规范的DataFrame格式数据导入数据库
    """
    path_file = working_space + "data/dictionary_building/" +\
            "机械五金类别及关键字预更新合并文件.xlsx"
    df_tobe_trans = pd.read_excel(path_file, sheet_name=None)
    #print df_tobe_trans['taobao'].head()
    df_kws_final = returnDataFrameOfTobeUpdatedFile(df_tobe_trans)
    df_kws_final = df_kws_final[['code', 'cate', 'list_kws']]
    df_kws_final.columns = ['code', 'cate', 'keyword']
    updateBulkOperation(df_kws_final)
    """
