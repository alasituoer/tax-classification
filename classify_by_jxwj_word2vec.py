#coding:utf-8

import pandas as pd
import jieba
from jieba import posseg
import gensim
from pymongo import MongoClient
from collections import Counter


jieba.load_userdict('jxwj_word2vec/dict.txt')

def segmented(line):
    """对给定字符串分词, 返回分词列表"""

    list_segmented = [word for word, flag in posseg.lcut(line) 
            if flag not in ['m', 'eng', 'x',]]

    return list_segmented

def returnMostSimilar(list_word):
    """给定词组, 返回最相近的词组列表"""

    model = gensim.models.Word2Vec.load('jxwj_word2vec/model.model')

    list_return = []
    for word in list_word:
        list_return_oneword = []
        try:
            for x in model.most_similar(word):
                list_return_oneword.append(x[0])
        except:
            list_return_oneword = []
        list_return.append(list_return_oneword)

    return list_return


def exactMatching(list_word_most_similar):

#    print('分词的最相似词组 输入: ', list_word_most_similar)

    list_result = []
    for list_kws in list_word_most_similar:
        #print(list_kws)
        list_result_onekws = []
	# list_kws内不会有重复值(因其是通过most_similar得到的)
        for kws in list_kws:
#            print(kws)
            for doc in db['detail_array'].find({'keywords': kws}):
                list_result_onekws.append(doc['code'] + ' ' + doc['cate'])
#        print(list_result_onekws)
#        print('\n')
        list_result.append(list_result_onekws)

    list_final = []
    for l1 in list_result[::-1]:
        list_final.extend(Counter(l1).most_common(len(l1)))

    return list_final


def queryFromMongodb(path_file):

#    """
    df = pd.read_pickle(path_file)
    df = df[(df['count']<1) | (df['count']>4)]

    df['new_splited_name'] = df['irregular_name'].apply(lambda x: str(x)).apply(segmented)

#    print(returnMostSimilar(['沥青', '漆']))
#    print(returnMostSimilar(['条形', '帽']))
#    print(returnMostSimilar(['防汛', '盆']))
#    print([eval(df['splited_name'].iloc[0])])

    df['most_similar'] = df['splited_name'].apply(lambda x: eval(x)
            ).apply(returnMostSimilar)
    df['new_most_similar'] = df['new_splited_name'].apply(returnMostSimilar)

#    print(df)
#    df.to_pickle('df_sample_query_from_mongo.pickle')
#    """
    
#    df = pd.read_pickle('df_sample_query_from_mongo.pickle')
#    print(df)
#    print(df.iloc[15]['most_similar'])
#    list_word_most_similar = [['空气压缩机', '压缩机', '制冷机', '螺杆式', '鼓风机', '离心式', '发电机组', '阿特拉斯', '水冷式', '织机'], ['垫圈', '加垫', '垫板', '垫块', '螺帽', '垫', '压盖', '密封垫', '螺母', '橡胶垫']]
#    print(exactMatching(list_word_most_similar))

    df['cate_most_similar'] = df['most_similar'].apply(exactMatching)
    df['cate_new_most_similar'] = df['new_most_similar'].apply(exactMatching)

    df.to_excel('df_wujin_final.xlsx')




if __name__ == "__main__":

    working_space = "/mnt/hgfs/windows_desktop/classification_and_coding/classification_and_coding/"
    path_file = working_space + "data/keywords_finding/the_result_20180314_10w+.xlsx"

    # 将10万+样本中的五金部分单独存储为pickle格式文件
#    df_handware = pd.read_excel(path_file, sheet_name='五金')
#    df_handware = df_handware[['irregular_name', 'splited_name', 'cate', 'count']]
#    print(df_handware.head())
#    df_handware.to_pickle(path_file + "df_handware.pickle")

    # 将10万+样本中的非五金部分也存储为pickle格式文件
#    df_not_handware = pd.read_excel(path_file, sheet_name='非五金')
#    df_not_handware = df_not_handware[['irregular_name', 'splited_name', 'cate', 'count']]
#    print(df_not_handware.head())
#    df_not_handware.to_pickle(path_file + "_df_not_handware.pickle")

    client = MongoClient('***', 
            username = '***',
	    password = '***', 
	    authSource = '***',
	    authMechanism = 'DEFAULT')
    db = client.test

    path_file = working_space + "data/keywords_finding/df_handware.pickle"
    queryFromMongodb(path_file)




