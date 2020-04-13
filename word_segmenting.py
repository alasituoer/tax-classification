#coding:utf-8
import pandas as pd
import uniout
import jieba
import jieba.posseg as pseg
import numpy as np

working_space = "/mnt/hgfs/windows_desktop/classification_and_coding/data/word_segmenting/"
jieba.load_userdict(working_space + "user_dict.txt")
#filename_demo1 = "demo-1.xlsx"
#filename_demo2 = "demo-2.xlsx"
filename_demo = "demo10w.xlsx"

#df_demo1 = pd.read_excel(working_space + filename_demo1)
#df_demo2 = pd.read_excel(working_space + filename_demo2)
#print df_demo1.shape, '\n', df_demo1.head(), '\n'
#print df_demo2.shape, '\n', df_demo2.head(), '\n'

#df_demo = pd.concat([df_demo1, df_demo2], axis=0)[[u'货物或应税劳务名称']]
#print df_demo.shape, '\n', df_demo.head(), '\n'
df_demo = pd.read_excel(working_space + filename_demo)
df_demo = df_demo[[u'货物或应税劳务名称']].astype(np.str)
#print df_demo.head()

#df_demo = df_demo1[[u'货物或应税劳务名称']]
#df_demo = df_demo2[[u'货物或应税劳务名称']]
#print df_demo.shape

#f = lambda x: u'、'.join([word for word, flag in jieba.posseg.lcut(x)
#		    if flag in ['n', 'nz', 'nl', 'ng',]])

def f(x):
    list_return = [word for word, flag in jieba.posseg.lcut(x)
			    if flag in ['n', 'nz', 'nl', 'ng',]]
    if len(list_return)==0:
	return x
    else:
	return u'、'.join(list_return)
#print f("倍加洁牙刷")
#print f("vivox2手机")


df_demo[u'分词结果'] = df_demo[u'货物或应税劳务名称'].apply(f)
df_demo.columns = ['irregular_name', 'splited_name',]
df_demo.to_excel(working_space + u"demo10w_splited.xlsx", index=False)


