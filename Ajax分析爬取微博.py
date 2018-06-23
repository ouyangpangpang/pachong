#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 29 21:14:17 2018

@author: oyc
"""

from urllib.parse import urlencode
import requests

from pyquery import PyQuery as pq

base_url='https://m.weibo.cn/api/container/getIndex?'

headers={
        'Host':'m.weibo.cn',
        'Referer':'https://m.weibo.cn/u/2830678474',
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20',
        'X-Requested-With':'XMLHttpRequest'
    
    }


def get_page(page):
    params={
            'type':'uid',
            'value':'2830678474',
            'containerid':'1076032830678474',
            'page':page
            
        }
    url=base_url+urlencode(params)#urlencode将参数转化成URL的get请求参数 如type=uid&value=2830678474&containerid=1076032830678474&page=2
    try:
        response=requests.get(url,headers=headers)
        if response.status_code==200:
            return response.json()
    except requests.ConnectionError as e:
        print('Error',e.args)
        
def parse_page(json):
    if json:
        items=json.get('data').get('cards')
        for item in items:
            i=item.get('mblog')
            weibo={}    
            weibo['id']=i.get('id')
            weibo['text']=pq(i.get('text')).text()#使用pyquery将正文中的HTML标签去掉
            weibo['attitudes']=i.get('attitudes_count')
            weibo['comments']=i.get('comments_count')
            weibo['reposts']=i.get('reposts_count')
            # yield weibo #生成器
            return weibo
        
if __name__=='__main__':
    for page in range(1,11):
        json=get_page(page)
        results=parse_page(json)
        print(results)
        #for result in results:
            #print(result)