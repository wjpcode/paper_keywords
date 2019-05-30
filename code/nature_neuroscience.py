#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  7 10:03:34 2019

@author: wangjinpeng
"""
from selenium import webdriver
import requests
from fake_useragent import UserAgent
import time
import csv
import random
from lxml import etree
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import os

MAXSLEEPTIME = 5
MINSLEEPTIME = 3
TIME_OUT = 24
#from uagent import get_ua
# 禁用安全请求警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
#进入volumes页面
def get_first_page():
#    url = 'https://www.nature.com/neuro/volumes/22'
#    url = 'https://www.nature.com/neuro/volumes/21'
#    url = 'https://www.nature.com/neuro/volumes/20'
    url = 'https://www.nature.com/neuro/volumes/19'
    head = {'User-Agent':UserAgent().chrome}
    response = requests.get(url,headers=head,timeout=TIME_OUT,verify=False)
#    headers = {'UserAgent':UserAgent().chrome}
#    response = requests.get(url,headers=headers,timeout=TIME_OUT,verify=False)
    text = response.text
    html = etree.HTML(text)
    alist = html.xpath('//*[@id="content"]/div[3]/div/section/ul/li/div/a/@href')
    full_alist = ['https://www.nature.com' + x for x in alist]
    print('full_alist:',full_alist)
    get_second_page(full_alist,head)
    time.sleep(random.randint(MINSLEEPTIME,MAXSLEEPTIME))
    
def get_second_page(newlist,head):
    #遍历每个issue
    for x in newlist:
        print('获取第一页所有单个issue的url')
        print(x)
        response = requests.get(x,headers=head,timeout=TIME_OUT,verify=False)
        text = response.text
        html = etree.HTML(text)
        #提取每个issue部分所有的版块，包括article，brief communications,……
        text_list = html.xpath('//*[@id="content"]/div/div/main/div/section/div/h2/@id')
        try:
            article_no = text_list.index('Articles') + 1
        except ValueError as e:
            print('该文章没有articles')
        else:
            articles = html.xpath('//*[@id="content"]/div/div/main/div[4]\
                                       /section[%d]/div/div/ul/li/article/div/h3/a//@href' % article_no)
        finally:
            article_list = ['https://www.nature.com' + y for y in articles]
            print('article_list',article_list)
            get_third_page(article_list,head)
            time.sleep(random.randint(MINSLEEPTIME,MAXSLEEPTIME))

def get_third_page(final_list,head):
    #遍历每篇文章的url
    for x in final_list:
        print('开始打印第三页的文章的url',x)
        web = webdriver.Chrome()
        time.sleep(5)
        web.get(x)
        # 模拟JavaScript动作鼠标下滑到最底端。
        js="var q=document.documentElement.scrollTop=10000"
        web.execute_script(js)
        #使用xpath去匹配。只能匹配到节点。不能将里边的内容匹配出来
        title = web.find_element_by_xpath('//*[@id="content"]/div/div/article/div[1]/header/div/h1')
        print('title:',title.text)
        published_data = web.find_element_by_xpath('//*[@id="content"]/div/div/article/div[1]/header/div/p/a/time')
        print('published_data:',published_data.text)
        #匹配多个li节点。
        subjects = web.find_elements_by_css_selector('#article-info-content > div.ma0.text14.sans-serif > div > ul > li')
        #将匹配到的内容添加到列表中
        l = []
        for s in subjects:
            l.append(s.text)
        print('subjects:',l)
        
        result = [title.text,l,published_data.text]
        save_result(result)
        web.close()
        time.sleep(random.randint(MINSLEEPTIME,MAXSLEEPTIME))
        
def save_result(result):
    # nat_neur_v22_2019_final.csv,nat_neur_v21_2018.csv,nat_neur_v20_2017.csv
    with open('nat_neur_v19_2016.csv','a+',newline='',encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(result)
        
              
def main():
    get_first_page()
    
if __name__ == '__main__':
    main()
    