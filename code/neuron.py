#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 22:02:54 2019

@author: wangjinpeng
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 31 21:03:20 2019

@author: wangjinpeng
"""

import requests
from fake_useragent import UserAgent
from lxml import etree
import csv
import random
import time
from requests.packages.urllib3.exceptions import InsecureRequestWarning
MAXSLEEPTIME = 3
MINSLEEPTIME = 1


# 禁用安全请求警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
#进入neuron官网的archive页面
def get_first_page():
    url = 'https://www.cell.com/neuron/archive'
    #请求头
    headers = {'User-Agent':UserAgent().chrome}
    #发起请求，获取响应
    response = requests.get(url,headers=headers,timeout=24,verify=False)
    #获取文本形式的响应
    text = response.text
#    print(text)
    #转换xpath识别的html格式
    html = etree.HTML(text)
    #xpath匹配每一卷每一个issue的文章
    alist = html.xpath('//*[@id="issueName"]/a/@href')
    #准备切片，将目的issue切出来
    print('准备开始切片')
    slice_alist = alist[8:14:1] # v100_2018
#    slice_alist = alist[14:26:1] # v99-98_2018
#    slice_alist = alist[26:33:1] # v97_pubtime_2018
#    slice_alist = alist[33:38:1]  # v96_issue12456_2017 差一个issue3
#    slice_alist = alist[38:44:1]  # v95_2017
#    slice_alist = alist[44:50:1] #v94_2017
#    slice_alist = alist[50:56:1] #v93_2017
    #issue有更新，所以索引号有变化
#    slice_alist = alist[56:62:1] #v92_2016
#    slice_alist = alist[62:68:1] #v91_2016
#    slice_alist = alist[68:74:1] #v90_2016
#    slice_alist = alist[74:80:1] #v89_2016

    #使用列表式拼全url
    full_list = ['https://www.cell.com' + x for x in slice_alist]
#    print(full_list)
    print('准备调用secondpage')
    get_second_page(full_list,headers)
    time.sleep(random.randint(MINSLEEPTIME,MAXSLEEPTIME))


def get_second_page(newlist,headers):
    #遍历从第一页里的issuelist
    for i in newlist:
        print('准备获取第一页的articles')
        #发起网页请求
        response = requests.get(i,headers=headers,timeout=24,verify=False)
        text = response.text
        html = etree.HTML(text)
        #提取取isuue部分所有的版块，包括articles版块
        text_list = html.xpath('//*[@id="frmSearch"]/div[1]/div/div/div[2]/section/h2/text()')
        try:
            
            articles_no = text_list.index('Articles') + 1
        except ValueError as e:
            print('该issue没有articles版块')
        else:    
            articles = html.xpath('//*[@id="frmSearch"]/div[1]/div/div/div[2]/section[%d]/ul/li\
                              /div[2]/div/div[2]/h3/a/@href' %articles_no)
        finally:
        #拼接文章的完整连接
            articles_list = ['https://www.cell.com' + x for x in articles]
            print('准备调用thirdpage')
            print(articles_list)
            get_third_page(articles_list,headers)
            time.sleep(random.randint(MINSLEEPTIME,MAXSLEEPTIME))
        

def get_third_page(final_list,headers):
    #遍历每一个文章的url
    for i in final_list:
        print('第三页现在开始抓取的url是:',i)
        response = requests.get(i,headers=headers,timeout=24,verify=False)
        text = response.text
        html = etree.HTML(text)
        #找出一篇article中所包含的部分，比如highlight，abstract，keywords等
        component_list = html.xpath('//*[@id="pb-page-content"]/div/div[1]/div/div/main/\
                                    article/div[2]/div[3]/div/div[2]/section/h2//text()')
        new_component_list = []
        for x in component_list:
            del_gap = x.strip()
            if del_gap:
                new_component_list.append(del_gap)
        print("文章中包含的内容是：",new_component_list)
        try:
            #取出keywords的索引
            keywords_index = new_component_list.index('Keywords') + 1
        except ValueError as e:
            print('该文章没有keywords')
        else:
            keywords = html.xpath('//*[@id="pb-page-content"]/div/div[1]/div/div/main/\
                                  article/div[2]/div[3]/div/div[2]/section[%d]/ul/li//text()' % keywords_index)
#        去除关键词之间的空格
            all_keyword = []
            for x in keywords:
                del_gap = x.strip()
                if del_gap:
                    all_keyword.append(x)
            print("关键词是：",all_keyword)
                            
        #得到以列表格式的标题
            title = html.xpath('//*[@id="articleHeader"]/div/div[3]/div[2]/h1/text()')
            
            #找到published_data
            published_data1 = html.xpath('//*[@id="articleHeader"]/div/div[3]/div[2]/div/span[1]/span/text()')
#            print('published_data1:',published_data1)
            published_data2 = html.xpath('//*[@id="articleHeader"]/div/div[3]/div[2]/div/span[2]/span/text()')
#            print('published_data2:',published_data2)
            
            if len(published_data1) == False:
                result = [title[0],all_keyword,published_data2[0]]
                print('result:',result)
                save_result(result)
                time.sleep(random.randint(MINSLEEPTIME,MAXSLEEPTIME))
            else:
                result = [title[0],all_keyword,published_data1[0]]
                print('result:',result)
                save_result(result)
                time.sleep(random.randint(MINSLEEPTIME,MAXSLEEPTIME))
                
#            try:
#                slice_published_data = published_data1[0] or published_data2[0]
#            except IndexError as e:
#                print('没有提取到该文章的发表日期')
#            finally:
#                if not published_data1:
#                    result = [title[0],all_keyword]
#                    print(result)
#                    save_result(result)
#                    time.sleep(random.randint(MINSLEEPTIME,MAXSLEEPTIME))
#                elif not published_data2:
#                    result = [title[0],all_keyword]
#                    print(result)
#                    save_result(result)
#                    time.sleep(random.randint(MINSLEEPTIME,MAXSLEEPTIME))
#                else: 
#                    result = [title[0],all_keyword,slice_published_data]
#                    print(result)
#                    save_result(result)
#                    time.sleep(random.randint(MINSLEEPTIME,MAXSLEEPTIME))
#                  
###
def save_result(result):
    #保存csv格式
    with open('neuron_data_v100-97_2018.csv','a+',newline='') as f:
        writer = csv.writer(f)
        writer.writerow(result)
        
            
def main():
    get_first_page()


if __name__ == '__main__':
    main()


