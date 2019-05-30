#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  1 20:23:37 2019

@author: wangjinpeng
"""

import requests
from fake_useragent import UserAgent
from lxml import etree
import time
import random
import csv

MAXSLEEPTIME = 3
MINSLEEPTIME = 1

#def get_first_page_v39():
#def get_first_page_v38():
#def get_first_page_v37():
def get_first_page_v36():

#    url = 'http://www.jneurosci.org/content/by/volume/39'
#    url = 'http://www.jneurosci.org/content/by/volume/38'
#    url = 'http://www.jneurosci.org/content/by/volume/37'
    url = 'http://www.jneurosci.org/content/by/volume/36'
   
    headers = {'User-Agent':UserAgent().chrome}
    response = requests.get(url,headers=headers,timeout=24,verify=False)
    text = response.text
    html = etree.HTML(text)   
    alist = html.xpath('//*[@id="block-system-main"]/div/div/div/div[2]/div[1]\
                               /div/div/div[7]/div/div/ul/li/div/div/div/a/@href')
    full_list = ['http://www.jneurosci.org' + x for x in alist]
    print('full_list:',full_list)
    get_second_page(full_list,headers)
    time.sleep(random.randint(MINSLEEPTIME,MAXSLEEPTIME))

def get_second_page(newlist,headers):
    #遍历第一页的issue
    for i in newlist:
        print('准备获取第一页所包含的内容')
        response = requests.get(i,headers=headers,timeout=24,verify=False)
        text = response.text
        html = etree.HTML(text)
        text_list = html.xpath('//*[@id="block-system-main"]/div/div/div/div[2]/\
            div[1]/div/div/div[1]/div/div/div/div/h2/text()')
        try:
            article_no = text_list.index('Research Articles') + 1
        except ValueError as e:
            print('该issue没有research Articles')
        else:
            research_articles = html.xpath('//*[@id="block-system-main"]/div/div/div/div[2]/div[1]\
                       /div/div/div[1]/div/div/div/div[%d]/ul/li/ul/li/div/div/div/a/@href' %article_no)
        finally:
            research_articles_list = ['http://www.jneurosci.org' + x for x in research_articles]
            print('准备调用thirdpage网页')
            print('research_articles_list')
            get_third_page(research_articles_list,headers)
            time.sleep(random.randint(MINSLEEPTIME,MAXSLEEPTIME))
            
def get_third_page(final_list,headers):
    for i in final_list:
        print('开始获取第三页的url：',i)
        response = requests.get(i,headers=headers,timeout=24,verify=False)
        text = response.text
        html = etree.HTML(text)
        keywords = html.xpath('//*[@id="block-system-main"]/div/div/div/div[2]/\
                              div[2]/div/div/div[7]/div/div/ul/li//text()')
        all_keyword = []
        for x in keywords:
            del_gap = x.strip()
            if del_gap:
                all_keyword.append(del_gap)  #有错误，应该为all_keyword.append(del_gap)
        print('关键词是：', all_keyword)
        title = html.xpath('//*[@id="page-title"]/text()')
        full_title = ' '.join(title)
#        all_title = []
#        for y in title:
#            del_gap_y = y.strip()
#            if del_gap_y:
#                all_title.append(y)
        print('title:',full_title)
        #取出日期中的data-node-nid属性
        node_id = html.xpath('//*[@id="block-system-main"]/div/div/div/div[1]\
                             /div/div/div/div[3]/div/div/@data-node-nid')
        int_node_id = int(node_id[0])
        print('int_node_id:',int_node_id)
        try:
            published_data = html.xpath('//*[@id="node%-6d"]/div[1]/div[4]/span[2]/text()' % int_node_id)
        except IndexError as e:
            print('published_data为空')
        finally:
            if len(published_data) == False:
                result = [full_title,all_keyword]
                print('result:',result)
                save_result(result)
                time.sleep(random.randint(MINSLEEPTIME,MAXSLEEPTIME))
            else:
                result = [full_title,all_keyword,published_data[0]]  
                print('result:',result)
                save_result(result)
                time.sleep(random.randint(MINSLEEPTIME,MAXSLEEPTIME))

def save_result(result):
    #保存
    with open('jofneuro_v36_2016.csv','a+',newline='') as f:
        writer = csv.writer(f)
        writer.writerow(result)
               
def main():
#    get_first_page_v39()
#     get_first_page_v37()
     get_first_page_v36()
    

if __name__ == '__main__':
    main()