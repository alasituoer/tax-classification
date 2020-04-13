# -*- coding: utf-8 -*-
import json
import jsonpath
import requests
import scrapy
from tmallSpider.items import TmallspiderItem


class TmallcrawlSpider(scrapy.Spider):
    name = 'tmallCrawl'
    allowed_domains = ['tmall.com']
    start_urls = ["http://www.tmall.com/"]

    def parse(self, response):
        cate_url = {}
        for each in response.xpath("//ul[@class='normal-nav clearfix']/li/a"):
            cateName = each.xpath("text()").extract()
            cateUrl = each.xpath("@href").extract()
            cateUrl = cateUrl[0].split(".com")[0] + ".com"
            # print(cateName[0],"https:"+cateUrl[0])
            cate_url[cateName[0]] = "https:"+cateUrl
        # print(cate_url)
        cate_spider = {'女装': self.ClothesParse,
                       '内衣': self.ClothesParse,
                       '男装': self.ClothesParse,
                       '箱包': self.BagParse,
                       '珠宝饰品': self.ClothesParse,
                       '运动户外': None,
                       '女鞋': None,
                       '男鞋': None,
                       '美妆': None,
                       '个人护理': None,
                       '腕表': None,
                       '眼镜': None,
                       '手机': None,
                       '数码':None,
                       '电脑办公': None,
                       '母婴玩具': None,
                       '零食': None,
                       '茶酒': None,
                       '进口食品': None,
                       '生鲜水果': None,
                       '大家电': None,
                       '生活电器': None,
                       '家具建材': None,
                       '汽车': None,
                       '配件': None,
                       '用品': None,
                       '家纺': None,
                       '家饰': None,
                       '鲜花': None,
                       '医药保健': None,
                       '厨具': None,
                       '收纳': None,
                       '宠物': None,
                       '图书音像': None}
        # for i,j in cate_url.items():
        #     print(i,j)
        new_url ='''https://www.tmall.com/'''
        yield scrapy.Request(url=new_url, callback=self.LoadPage)

    def ClothesParse(self,response):
        '''
           '女装': self.ClothesParse,成功
           '内衣': self.ClothesParse,成功
           '男装': self.ClothesParse,成功
           '珠宝饰品': self.ClothesParse,成功，无细分类目
           '家居家纺': self.ClothesParse,成功，无细分类目
           '''
        print("coming!")

        # 获取侧展列表进行主体
        sideListBody = response.xpath("//div[@class='cate-panels']/div")
        # 找到当前列表标题对应的侧展列表
        sideCollections = {}
        for panel in sideListBody:
            sideTitle = panel.xpath("div/span/text()").extract()
            sideList = panel.xpath("div[@class='sub-col sub-col1 clearfix']")
            sideList2 = sideList.xpath("string(.)").extract()
            cateTitle = panel.xpath("div/h2/text()").extract()
            print(sideTitle)

            if len(sideTitle) > 0 and len(sideList2)>0:
                sideList = sideList2[0].replace("\n",",").replace(" ","").lstrip(",,,").rstrip(",,,").split(",,,,")
                sideIndex = [sideList.index(i) for i in cateTitle]
                sideIndex.append(len(sideList)-2)

                sideDict = {}
                for i in sideIndex:
                    if i == sideIndex[-1]:
                        break
                    endidx = len(sideList) + 2 if i == sideIndex[-2] else sideIndex[sideIndex.index(i)+1]
                    sideDict[sideList[i]] = sideList[i+1:endidx]
                sideCollections[sideTitle[0]]=sideDict
        # print(sideCollections)

        title = response.xpath("//head/title/text()").extract()
        body = response.xpath("//div[@class='tm-fushi-cate']/ul[@class='cate-nav']/li[@class='cate-item']")
        for each in body:
            item = TmallspiderItem()
            # 提取类目标题
            cateTitle = each.xpath("h2/text()").extract()
            # 列表标题
            segName =  None
            # 列表内容
            segList = each.xpath("ul/li/a/text()").extract()

            item['title'] = title[0]
            item['cateTitle'] = cateTitle[0]
            item['segName'] = segName
            item['segList'] = segList

            yield item


            # 判断是否有嵌套列表
            segDict = sideCollections.get(cateTitle[0])
            # 如果有
            if segDict:
                snames = segDict.keys()
            else:
                continue
            for i in snames:
                item_ = TmallspiderItem()
                item_['title'] = title[0]
                item_['cateTitle'] = cateTitle[0]
                item_['segName'] = i
                item_['segList'] = segDict.get(i)
                yield item_
        print("="*100)

    def BagParse(self,response):
        '''
           '箱包': self.BagParse,成功
           '''
        print("coming!")

        title = response.xpath("//head/title/text()").extract()
        body = response.xpath("//div[@class='tm-fushi-cate']/ul[@class='cate-nav']/li[@class='cate-item']")
        # 定义侧展列表栏位序号
        num = 1
        for each in body:
            item = TmallspiderItem()
            # 提取类目标题
            cateTitle = each.xpath("h2/text()").extract()
            # 列表标题
            segName =  None
            # 列表内容
            segList = each.xpath("ul/li/a/text()").extract()

            item['title'] = title[0]
            item['cateTitle'] = cateTitle[0]
            item['segName'] = segName
            item['segList'] = segList

            yield item


            # 获取侧展列表进行主体
            sideListBody = response.xpath("//div[@class='tm-fushi-cate']/div[@class='cate-panels']/div[%s]" %num)

            # 找到当前列表标题对应的侧展列表
            sideCollections = {}
            sideTitle = sideListBody.xpath("div[@class='sub-col sub-col1 clearfix']/h2/text()").extract()
            sideList = sideListBody.xpath("div[@class='sub-col sub-col1 clearfix']")
            sideList2 = sideList.xpath("string(.)").extract()

            num += 1
            sideList = sideList2[0].replace("\n",",").replace(" ","").lstrip(",,,").rstrip(",,,").split(",,,,")
            sideIndex = [sideList.index(i) for i in sideTitle]
            sideIndex.append(len(sideList)-2)

            sideDict = {}
            for i in sideIndex:
                if i == sideIndex[-1]:
                    break
                endidx = len(sideList) + 2 if i == sideIndex[-2] else sideIndex[sideIndex.index(i)+1]
                sideDict[sideList[i]] = sideList[i+1:endidx]
                sideCollections[cateTitle[0]]=sideDict


            sideSet = sideCollections.get(cateTitle[0])
            for i,j in sideSet.items():
                item_ = TmallspiderItem()
                item_['title'] = title[0]
                item_['cateTitle'] = cateTitle[0]
                item_['segName'] = i
                item_['segList'] = j
                yield item_
            print("=" * 100)

    def ShoesParse(self,response):
        '''
           '男鞋': self.ShoesParse,成功,无细分类目
           '女鞋':self.ShoesParse,,无细分类目
           '''
        body = response.xpath("//div[@class='fushi-first-sidebar w240']/div[@class='fushi-f-cat-cont biz-module']")
        for each in body:
            item = TmallspiderItem()
            item['title'] = response.xpath("//head/title/text()").extract()[0]
            item['cateTitle'] = each.xpath("h2/text()").extract()[0]
            item['segName'] = None
            item['segList'] = each.xpath("ul[@class='clearfix']/li/a/text()").extract()
            yield item

    def BabyParse(self,response):
        '''
           '母婴': self.BabyParse,,

           '''
        mainBody = response.xpath("//div/div[@class='mui-category-menu']")
        sideBody = mainBody.xpath("ul/li")
        title = response.xpath("//head/title/text()").extract()[0]
        for each in sideBody:
            data_tag = each.xpath("@data-tag").extract()[0]
            data_tag = data_tag[:-1] + '2'
            # print(data_tag)

            cateTitle = each.xpath("h4/text()").extract()[0]

            item = TmallspiderItem()
            item['title'] = title
            item['cateTitle'] = cateTitle
            item['segName'] = None
            item['segList'] = each.xpath("a/text()").extract()
            yield item




            # 获取侧展列表进行主体
            sideListBody = mainBody.xpath("div[@data-tag='%s']" %data_tag)

            # 找到当前列表标题对应的侧展列表

            sideTitle = sideListBody.xpath("h4/text()").extract()
            sideTitle = [i.replace(" ","") for i in sideTitle]
            sideStr = sideListBody.xpath("string(.)").extract()
            # print(sideTitle)
            # print(sideStr)

            sideList = sideStr[0].replace("\n", ",").replace(" ", "").lstrip(",,,").rstrip(",,,") .split(",,")
            sideList = [i.replace(',','') for i in sideList]
            sideIndex = [sideList.index(i) for i in sideTitle]
            sideIndex.append(len(sideList) - 2)
            # print(sideList)

            sideDict = {}
            sideCollections = {}
            for i in sideIndex:
                if i == sideIndex[-1]:
                    break
                endidx = len(sideList) + 2 if i == sideIndex[-2] else sideIndex[sideIndex.index(i) + 1]
                sideDict[sideList[i]] = sideList[i + 1:endidx]
                sideCollections[cateTitle] = sideDict
            # print(sideCollections)


            sideSet = sideCollections.get(cateTitle)
            for i, j in sideSet.items():
                item_ = TmallspiderItem()
                item_['title'] = title
                item_['cateTitle'] = cateTitle
                item_['segName'] = i
                item_['segList'] = j
                yield item_
            print("=" * 100)

    def BookParse(self,response):
        '''
           '图书音像': self.ClothesParse,成功
           '珠宝饰品': self.ClothesParse,成功，无细分类目
           '家居家纺': self.ClothesParse,成功，无细分类目
           '''


        title = response.xpath("//head/title/text()").extract()
        body = response.xpath("//div[@class='jia-left-nav']/ul/li")
        for each in body:
            item = TmallspiderItem()
            # 提取类目标题
            cateTitle = each.xpath("div/text()").extract()[0]
            cateTitle = cateTitle.replace(" ","").replace("\n","")
            # 列表标题
            segName =  None
            # 列表内容
            segList = each.xpath("a/text()").extract()

            item['title'] = title[0]
            item['cateTitle'] = cateTitle
            item['segName'] = segName
            item['segList'] = segList

            yield item

            sideBody = each.xpath("div[@class='nav-expand-content']/div")
            for side in sideBody:
                segName = side.xpath("div[@class='box-title']/text()").extract()[0]
                segName = segName.replace(" ","").replace("\n","")
                # print(segName)

                segList = side.xpath("div[@class='box-cell-container']/a/text()").extract()
                # print(segList)

                item_ = TmallspiderItem()
                item_['title'] = title[0]
                item_['cateTitle'] = cateTitle
                item_['segName'] = segName
                item_['segList'] = segList
                print("-" * 30)
                yield item_
            #
            print("="*100)

    def SportsParse(self,response):
        '''sports:'''

        title = response.xpath("//head/title/text()").extract()
        body = response.xpath("//div[@class='cate-panels']/div[@class='cate-panel']")
        for each in body:
            cateTitle = each.xpath("div/span/text()").extract()
            seg2 = each.xpath("div[@class='sub-col sub-col2 clearfix']")
            seg1 = each.xpath("div[@class='sub-col sub-col1 clearfix']")

            segStr1 = seg1.xpath("string(.)").extract()
            segStr1 = segStr1[0].replace("\n", ",").replace(" ", "").lstrip(",,,").rstrip(",,,").split(",,,,")

            segStr2 = seg2.xpath("string(.)").extract()
            segStr2 = segStr2[0].replace("\n", ",").replace(" ", "").lstrip(",,,").rstrip(",,,").split(",,,,")

            segName1 = seg1.xpath("h2/text()").extract()
            segName2 = seg2.xpath("h2/text()").extract()
            segName = segName1 + segName2

            segStr = segStr1 + segStr2

            # print(segName)
            # print(segStr)
            # print("="*50)

            sideIndex = [segStr.index(i) for i in segName]
            sideIndex.append(len(segStr)-2)

            sideCollections = {}
            sideDict = {}
            for i in sideIndex:
                if i == sideIndex[-1]:
                    break
                endidx = len(segStr) + 2 if i ==sideIndex[-2] else sideIndex[sideIndex.index(i) + 1]
                sideDict[segStr[i]] = segStr[i + 1:endidx]
                sideCollections[cateTitle[0]] = sideDict
            # print(sideCollections)

            sideSet = sideCollections.get(cateTitle[0])
            for j,k in sideSet.items():
                item = TmallspiderItem()
                item['title'] = title[0]
                item['cateTitle'] = cateTitle[0]
                item['segName'] = j
                item['segList'] = k

                yield item

    def WatchParse(self,response):
        '''
        watch
        :param response:
        :return:
        '''
        print('coming!')
        # print(response)
        title = response.xpath("//head/title/text()").extract()
        body = response.xpath("//div[@id='J_MuiCategoryMenu']/textarea[@data-type='end']/text()").extract()
        bodyDict = eval(body[0])
        for i in bodyDict:
            print(i['cat'],i['title'])
            item = TmallspiderItem()

            item['title'] = title[0]
            item['cateTitle'] = 'None'
            item['segName'] = i['cat']
            item['segList'] = [i['title']]

            yield item

    def YaoParse(self,response):
        title = response.xpath("//head/title/text()").extract()
        sideBody = response.xpath("//div[@id='J_MuiCategoryMenu']/ul/li/div[@class='leftCategory']")
        segBody = response.xpath("//div[@id='J_MuiCategoryMenu']/div/div")
        # print(sideBody)
        for i in range(0,5):
            side = sideBody[i]
            seg = segBody[i]
            catetitle = side.xpath("h3/a/text()").extract()
            sideList = side.xpath("a/text()").extract()

            item = TmallspiderItem()
            item['title'] = title[0]
            item['cateTitle'] = catetitle[0]
            item['segName'] = 'None'
            item['segList'] = sideList

            yield item

            # print(catetitle[0],sideList)
            print("="*100)

            seg_block = seg.xpath("div/dl")
            for i in seg_block:
                segName = i.xpath("dt/a/text()").extract()
                segList = i.xpath("dd/a/text()").extract()

                item_ = TmallspiderItem()
                item_['title'] = title[0]
                item_['cateTitle'] = catetitle[0]
                item_['segName'] = segName[0]
                item_['segList'] = segList

                yield item_

                # print(segName)
                # print(segList)
                print("-"*100)

    def FoodParse(self,response):
        title = response.xpath("//head/title/text()").extract()
        sideBody = response.xpath("//div[@id='J_MuiCategoryMenu']/ul/li")
        segBody = response.xpath("//div[@id='J_MuiCategoryMenu']/div")
        # print(sideBody)
        for i in range(0,5):
            side = sideBody[i]
            seg = segBody[i]
            catetitle = side.xpath("h4/a/text()").extract()
            sideList = side.xpath("a/text()").extract()

            item = TmallspiderItem()
            item['title'] = title[0]
            item['cateTitle'] = catetitle[0]
            item['segName'] = 'None'
            item['segList'] = sideList

            yield item

            # print(catetitle[0],sideList)
            # print("-"*100)

            segStr = seg.xpath("string(.)").extract()
            segStr = segStr[0].replace(" ", ",").replace("\t", "").replace("\n", "").lstrip(",").rstrip(",").split(",")#replace(',,,,,,,,,,',",").replace(',,,,,,,,,',",").replace(',,',",").
            segStr = [word for word in segStr if len(word)>0]
            segTitle = seg.xpath("h4/a/text()").extract()


            if len(segTitle)>0:
                sideCollections = {}
                sideIndex = [segStr.index(j) for j in segTitle]
                sideIndex.append(len(segStr) - 2)

                sideDict = {}
                for k in sideIndex:
                    if k == sideIndex[-1]:
                        break
                    endidx = len(segStr) + 2 if k == sideIndex[-2] else sideIndex[sideIndex.index(k) + 1]
                    sideDict[segStr[k]] = segStr[k + 1:endidx]

                    sideCollections[catetitle[0]] = sideDict
                # print(sideCollections)

                sideSet = sideCollections.get(catetitle[0])
                for m, n in sideSet.items():
                    item_ = TmallspiderItem()
                    item_['title'] = title[0]
                    item_['cateTitle'] = catetitle[0]
                    item_['segName'] = m
                    item_['segList'] = n
                    yield item_
                # print("=" * 100)
            else:
                item2 = TmallspiderItem()
                item2['title'] = title[0]
                item2['cateTitle'] = catetitle[0]
                item2['segName'] = None
                item2['segList'] = segStr
                yield item2

            # print(segTitle)
            # print(segStr)
            print("="*100)

    def SCParse(self,response):
        bigbody = response.xpath("//div[@class='J-fs-subnav fs-subnav']/textarea").extract()
        for sideBody in bigbody:
            sideBody = sideBody.replace(r'<textarea style="display:none">',"").replace(r'</textarea>',"")

            from lxml import etree
            html = etree.HTML(sideBody)
            for each in html.xpath("//body/dl"):
                segName = each.xpath("dt/a/text()")
                segList = each.xpath("dd/a/text()")

                item = TmallspiderItem()
                item['title'] = '天猫3C'
                item['cateTitle'] = None
                item['segName'] = segName[0]
                item['segList'] = segList

                yield item
                print("="*100)

    def LoadPage(self,responese):
        json_txt = responese.xpath("//div[@id='J_defaultData']/text()").extract()[0]
        jsonobj = json.loads(json_txt)

        # 获取各细分品类的appid
        appid_dict = []  #大类，细分类，细分类别appid
        appid_list = []  #细分类别appid，用于组合
        for num in range(1,17):
            appid = jsonpath.jsonpath(jsonobj, '$[page][100][hotWordType%s]'%num)[0]
            for eachDict in appid:
                del eachDict['isUse']
                eachDict['howWordType'] = 'hotWordType%s'%num
                appid_list.append(str(eachDict['appId']))
            appid_dict.extend(appid)
            # print(appid)
            # print("=" * 100)
        # print(appid_dict)


        # appid：细分类别名称
        appidDict = {}
        # appid:hotWordType
        appidWord = {}
        for apid in appid_dict:
            appidDict[str(apid['appId'])] = apid['title']
            appidWord[str(apid['appId'])] = apid['howWordType']
        # print(appidDict)
        # print(appidWord)
        #
        appidStr = ",".join(appid_list)
        json_url = "https://aldh5.tmall.com/recommend2.htm?notNeedBackup=true&appId=" + appidStr
        rqst = requests.get(json_url)
        html = rqst.text
        jsonobj = json.loads(html)
        for j,k in jsonobj.items():
            segList = [l['title'] for l in k['data']]
            item = TmallspiderItem()
            item['title'] = '天猫首页'
            item['cateTitle'] = appidWord[j]
            item['segName'] = appidDict[j]
            item['segList'] = segList
            yield item
            # print("category: " + appidDict[j])
            # print("hotWord:  " + appidWord[j])
            # print(segList)
            print("="*100)
