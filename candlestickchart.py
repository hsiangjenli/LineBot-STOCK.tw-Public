# -*- coding: utf-8 -*-
"""
Created on Fri Oct  2 11:16:47 2020

@author: User
"""

import imgur
import pandas_datareader.data as web
import datetime
import matplotlib.pyplot as plt 
import mplfinance as mpf
import numpy as np

CLIENT_ID = "Imgur Client ID"
savefig = 'savefig_path.png'

def plot_candlestick(stock_code, span, CLIENT_ID, savefig):
    start_date = (datetime.datetime.now() - datetime.timedelta(span)).strftime("%Y-%m-%d")
    df = web.DataReader(stock_code, 'yahoo', start_date)
    mc = mpf.make_marketcolors(up='#5ac390',down='#fd6a6c',volume='in',edge='None',)
    s  = mpf.make_mpf_style(base_mpl_style='fivethirtyeight',gridstyle='None',marketcolors=mc)
    fig = mpf.figure(style=s,figsize=(20,10))
    ax1 = fig.add_axes([0.05,0.3,0.95,0.5])
    ax2 = fig.add_axes([0.05,0.1,0.95,0.2])
    mav=(3,6,9)
    mpf.plot(df,
             type='candle',
             style=s,
             volume=ax2,
             mav=(3,6,9),
             panel_ratios=(4,1),
             xrotation=0,
             ax = ax1,
             update_width_config = dict(candle_width = 0.95),
             scale_width_adjustment = dict(lines=2))
    ax1.legend(['mav '+str(mav[0]),'mav '+str(mav[1]),'mav '+str(mav[2])],
               loc='best', 
               bbox_to_anchor=(0.2, 1.1),
               fontsize = 20,
               frameon = True,
               edgecolor = 'w',
               facecolor = 'w')
    ax1.set_title(
        label = 'TWSE\nStock Code:{}'.format(stock_code),
        fontdict={'fontsize':30,
                  'fontweight':'bold',
                  'color':'k'},
        loc='center')
    ax1.set_ylabel('Price',fontdict={'weight': 'bold', 'size': 20})
    ax2.set_ylabel('Volume',fontdict={'weight': 'bold', 'size': 20})
    ax1.yaxis.set_label_position("left")
    ax1.yaxis.tick_left()
    yticks = np.arange(min(df['Volume']), max(df['Volume']), round( (max(df['Volume']) - min(df['Volume']))/5 ))
    ax2.set_yticks(yticks)
    plt.savefig(savefig, dpi=300)
    url = imgur.upload_to_imgur(CLIENT_ID, savefig)
    return url
