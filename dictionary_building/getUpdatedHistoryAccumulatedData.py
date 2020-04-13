#coding:utf-8
from pymongo import MongoClient

if __name__ == "__main__":
    client = MongoClient("***", 27017)
    db = client.test

    # 在此从最原始分类编码文件中人工核对整理
    # 504条记录 = 346(说明不为空)+ 158(说明为空, cate中包含'、'或者'及') 多个类别的关键字


    # 最新的表与最原始的表做差, 得到历史累计更新(添加)的类别及其关键字
    for doc_old in db.docs_first_commit.find()[100:200]:
        for doc_new in db.docs_copy.find({'code': doc_old['code']}):
#            print doc_old['code'], doc_old['cate']
#            print "old: ", repr(doc_old['keywords']).decode('unicode-escape')
#            print "new: ", repr(doc_new['keywords']).decode('unicode-escape')
            dict_to_write = {'code': doc_new['code'], 'cate': doc_new['cate'],
                    'keywords': [x for x in doc_new['keywords'] \
                            if x not in doc_old['keywords']]}
            if len(dict_to_write['keywords']) > 0:
                print repr(dict_to_write).decode('unicode-escape')



