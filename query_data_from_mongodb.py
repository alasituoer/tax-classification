#coding:utf-8
import numpy as np
import pandas as pd
from pymongo import MongoClient
from datetime import datetime
import time

def readIrregularAndSplitedName(path_file):
    """得到不规则货物名称的分词结果
        顺便设置字段类型为字符串(针对某些字段值是纯数值做转换)"""

    df = pd.read_excel(path_file, dtype={'irregular_name': np.str, 'splited_name': np.str})
    df_irregular_splited_name = df[[u'货物或应税劳务名称', 'kd']]
    df_irregular_splited_name.columns = ['irregular_name', 'splited_name',]
    #df_splited_name['splited_name'] = \
    #        df_splited_name['splited_name'].apply(lambda x: u'、'.join(eval(x)))

    return df_irregular_splited_name


def exactQuery(the_collection, splited_name):
    """根据一个关键字在指定集合中查找结果"""

    query_result = []
    for doc in db[the_collection].find({'keywords':splited_name}):
        query_result.append([doc['code'], doc['cate'], doc['keywords']])
    df_query_result = pd.DataFrame(query_result, columns=['code', 'cate', 'keywords'])

    return df_query_result


def exactMatching(the_collection, list_splited_name):
    """从分词列表中循环查询指定数据库集合, 得到最终的匹配结果"""

    # 如果分词列表中倒数第一关键词查询结果为空, 则从倒数第二个关键词开始, 以此类推
    df_query_result = exactQuery(the_collection, list_splited_name[-1])
    list_splited_name.pop()
    while(df_query_result.shape[0]==0 and len(list_splited_name)!=0):
        df_query_result = exactQuery(the_collection, list_splited_name[-1])
        list_splited_name.pop()
    #print "\n首次查询到的结果:\n", df_query_result
    #print "查询到结果后的后剩余关键字: ", repr(list_splited_name).decode('unicode-escape')

    # 查询的结果不为空且不为一时, 利用剩余的关键字进行筛选, 剩余关键都检查后结束循环
    while(df_query_result.shape[0] > 1 and len(list_splited_name) != 0):
        #print df_query_result
        #print "筛选剩余的关键字:", repr(list_splited_name).decode('unicode-escape')

        # 如果利用剩余的关键字筛选结果为空
    # 则保持上一结果集, 接着利用下一关键字筛选
        ss_selected_flag = pd.Series([list_splited_name[-1] in l
                for l in df_query_result['keywords']])
        ss_selected_flag.index = df_query_result.index
        if df_query_result[ss_selected_flag].shape[0] != 0:
        df_query_result = df_query_result[ss_selected_flag]
    list_splited_name.pop()
    #print "精确匹配的结果: ", df_query_result

    return df_query_result


def fuzzyQuery(the_collection, splited_name):
    """ """

    query_result = []
    for doc in db[the_collection].find({'keywords': {'$regex': splited_name}}):
        query_result.append([doc['code'], doc['cate'], doc['keywords']])
    df_query_result = pd.DataFrame(query_result, columns=['code', 'cate', 'keywords'])

    return df_query_result


def fuzzyMatching(the_collection, list_splited_name):
    """"""

    df_query_result = fuzzyQuery(the_collection, list_splited_name[-1])
    list_splited_name.pop()
    # 如果倒数第一关键词查询结果为空, 则从倒数第二个关键词开始, 以此类推
    while(df_query_result.shape[0] == 0 and len(list_splited_name)!= 0):
        df_query_result = fuzzyQuery(the_collection, list_splited_name[-1])
    list_splited_name.pop()
    #print df_query_result
    #print repr(list_splited_name).decode('unicode-escape')

    while(df_query_result.shape[0] > 1 and len(list_splited_name) != 0):
        #print df_query_result
    #print repr(list_splited_name).decode('unicode-escape')
    ss_selected_flag = pd.Series([list_splited_name[-1] in l
            for l in df_query_result['keywords']])
        ss_selected_flag.index = df_query_result.index
    if df_query_result[ss_selected_flag].shape[0] != 0:
        df_query_result = df_query_result[ss_selected_flag]
    list_splited_name.pop()
    # print "模糊匹配的结果: ", df_query_result

    return df_query_result


def getCodeAndCate(splited_name):
    """根据某个不规则名称的关键字列表, 设置循环匹配的规则,
        返回最优的查询结果"""

    list_splited_name = [x.decode('utf-8') for x in eval(splited_name)]
    # 删除列表的重复值并保持原来的顺序
    func = lambda x,y: x if y in x else x+[y]
    list_splited_name = reduce(func, [[], ] + list_splited_name)
    #print "最终的分词结果: ", repr(list_splited_name).decode('unicode_escape')

    df_query_result = exactMatching('detail_array', list_splited_name[:])
    #print "细分类精确匹配: ", df_query_result
    if df_query_result.shape[0] == 0:
        df_query_result = exactMatching('category_array', list_splited_name[:])
        #print "粗分类精确匹配: ", df_query_result

    # 对于上述未匹配到的再进行模糊匹配
    if df_query_result.shape[0] == 0:
        df_query_result = fuzzyMatching('detail_string', list_splited_name[:])
        #print "细分类模糊匹配: ", splited_name, df_query_result
    if df_query_result.shape[0] == 0:
        df_query_result = fuzzyMatching('category_string', list_splited_name[:])
        #print "粗分类模糊匹配: ", splited_name, df_query_result

#    print df_query_result

    # 将位于行索引中的商品编码和商品类别一起输出
    list_to_return = []
    for idx in df_query_result.index:
        list_to_return.append(df_query_result.loc[idx]['code'] + ' ' +\
            df_query_result.loc[idx]['cate'])
#    print repr(list_to_return).decode('unicode-escape')

    return list_to_return


if __name__ == "__main__":

    working_space = "/mnt/hgfs/windows_desktop/classification_and_coding/classification_and_coding/"

    start_time = datetime.now()

    #client = MongoClient("***", 27017)
    client = MongoClient('***', 
            username = '***',
            password = '***',
            authSource = '***',
            authMechanism = 'DEFAULT',)
    db = client.test

    # 读入给定样本的分词结果
    path_file = working_space + "data/word_segmenting/demo3_new_split.xlsx"
    df_irregular_splited_name = readIrregularAndSplitedName(path_file)

    # 对预批量进入的样本, 可以分批操作, 如5w成批(一批处理时间20+min)

#    df_irregular_splited_name = df_irregular_splited_name[50000:]
#    print df_irregular_splited_name

    df_result = df_irregular_splited_name
    # 根据分词结果查询数据数据库
    df_result['cate'] = df_result['splited_name'].apply(getCodeAndCate)

    # 计算返回类别的数目(即 列表元素的个数)
    df_result['count'] = df_result['cate'].apply(lambda x: len(x))

    # 方便在excel中正确存储中文列表cate
    df_result['cate'] = df_result['cate'].apply(lambda x: repr(x).decode('unicode-escape'))

#    print df_result

#    """
    # 存储最终结果
    path_to_write = working_space + "data/keywords_finding/"
    filename_to_write = "the_result_" + time.strftime('%Y%m%d', time.localtime()) + '.xlsx'
    df_result.to_excel(path_to_write + filename_to_write)
#    """

    # 计算最终用时
    # 1w 427s(4.12m)
    # 前5w 1711s(28.5m)
    # 后5w 2300s(38m)
    finish_time = datetime.now()
    print "总用时: ", (finish_time - start_time).total_seconds()




