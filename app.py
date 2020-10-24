# -*- coding: utf-8 -*-
"""
Created on Thu Oct  1 10:42:26 2020

@author: User
"""

#載入LineBot所需要的套件
from flask import Flask, request, abort
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import *

#import副程式
import candlestickchart
import Stock_Info as s

#import regex
import regex as re

#imgur Client id, savefig
CLIENT_ID = "0a5b5c23df1a717"
savefig = 'test_plot.png'

app = Flask(__name__)

### Channel Access Token
line_bot_api = LineBotApi('Channel Access Token')
### Channel Secret
handler = WebhookHandler('Channel Secret')
### Your user ID
line_bot_api.push_message('Your user ID', TextSendMessage(text='你可以開始了'))


@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

###傳送訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = str(event.message.text).upper().strip() # 使用者輸入的內容
    profile = line_bot_api.get_profile(event.source.user_id)
    user_name = profile.display_name #使用者名稱
    user_id = profile.user_id # 發訊者ID
    if re.match('C', msg):
        imgur_url = candlestickchart.plot_candlestick(msg[1:15], 90, CLIENT_ID, savefig)
        line_bot_api.push_message(user_id, [TextSendMessage(text='正在畫圖，請稍後....'),ImageSendMessage(original_content_url=imgur_url, preview_image_url=imgur_url)])
    elif re.match('M', msg):
        imgur_url = candlestickchart.plot_candlestick_macd(msg[4:20], 90, CLIENT_ID, savefig)
        line_bot_api.push_message(user_id, [TextSendMessage(text='正在畫圖，請稍後....'),ImageSendMessage(original_content_url=imgur_url, preview_image_url=imgur_url)])
    elif re.match('I', msg):
        text = s.basic_info(msg[4:20])
        line_bot_api.push_message(user_id, TextSendMessage(text=text))
        
#主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)