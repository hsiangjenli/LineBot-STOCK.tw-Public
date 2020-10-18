# -*- coding: utf-8 -*-
"""
Created on Sat Oct 17 00:07:43 2020
@author: User
"""

import requests
import json
import pandas as pd


###header
headers = {'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko)\Chrome/70.0.3538.110 Mobile Safari/537.36'}

###鉅亨網 股票基本資料
def basic_info(stock_code):
    stock_code = stock_code
    url = 'https://marketinfo.api.cnyes.com/mi/api/v1/TWS:{}:STOCK/info'.format(stock_code.split('.')[0])
    res = requests.get(url,headers=headers)
    data = res.json()
    df = pd.DataFrame(data['data'].keys())
    df['data'] = pd.DataFrame(data['data'].values())
    replace_en = [['symbolId'], ['companyName'], ['companyAddress'],
                  ['telephoneNumber'], ['industryType'], ['description'],
                  ['president'],['listingDateS'],['startAtS'],['agency'],
                  ['agencyPhone'],['agencyAddress'],['url'], 
                  ['commonShares'],['netAsset'],['foreignStockOwnRatio'], 
                  ['generalManager'],['spokesman'],['pbr'], 
                  ['per'],['eps']]
    replace_ch = ['股票代碼', '公司名稱', '地址', '電話號碼', '產業別', '主營業務', '董事長','上市日期','成立日期','股票過戶機構',
                  '過戶電話','過戶機構地址','網站','實收資本','每股淨值','外資持股','總經理','發言人','股價淨值比','本益比','每股盈餘']
    df[0] = df[0].replace(replace_en, replace_ch)
    df = df.drop([2,6,11,12,18,20,21,22,23,25,29,32,33,34,35,36,37]) 
    index = [e for e in df[0]]
    data = [e for e in df['data']]
    text = ''
    for e in range(0, len(index)):
        text = text+index[e]+'：'+str(data[e])+'\n'
        e = e+1
    return text