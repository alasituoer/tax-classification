#coding:utf-8

cmd:
# 进入文件预下载目录
>cd C:\Users\Administrator\Desktop\classification_and_coding\data\dictionary_building\upload_to_39
# 从本地数据库中下载指定集合
>mongoexport -d test -c docs_copy -o docs_copy.json
# 将该集合上传到指定服务器的指定数据库中
# 参数-u指定的用户需属于待上传数据库
# 只是拥有该数据库的某些权限但不属于该数据库的用户,不行
>mongoimport -h ***:27017 -u test -p `username` -d test -c docs_copy docs_copy.json
# 操作下一个集合
>mongoexport -d test -c strdoc -o strdoc.json
>mongoimport -h ***:27017 -u test -p `username` -d test -c strdoc strdoc.json

