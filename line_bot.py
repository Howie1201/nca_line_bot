# -*- coding: utf-8 -*-
"""
Created on Thu Jul 23 15:50:24 2020

@author: jacky
"""

from __future__ import unicode_literals
import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError

from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)

line_bot_api = LineBotApi('KbUSP5ShwG5gziWRdy3niYUieAZaYlDc2YMW1HB3Ao05YRm+DKUar29lK0lfqjeMqzLRm1MLALf/R4jIV/k+98YxIR40SryCI8qsokVBe31heMMafyPQSI89odk42Ts1dD9b35gyPMCkOhHEGp+M/wdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('b33a01e1e548c7b39a732d62245e1d36')

# Webhook callback endpoint
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

description = '指令輸入格式:\n(指令)/ (內容)\n\n指令:\n說明、點餐、點餐清單'
order_list = ''

# decorator 判斷 event 為 MessageEvent
# event.message 為 TextMessage 
# 所以此為處理 TextMessage 的 handler
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # 決定要回傳什麼 Component 到 Channel
    '''
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))
    '''
    print(event)
    
    #userId = event.source.userId
    message = event.message.text
    texts = message.split(' ', 1)
    
    if(texts[0] == '說明/'):
        line_bot_api.reply_message(event.reply_token, TextSendMessage(description))
    if(texts[0] == '點餐/'):
        profile = line_bot_api.get_profile('<user_id>')
        order_list.append(profile.display_name + ' ' + texts[1] + '\n')
    if(texts[0] == '點餐清單/'):
        line_bot_api.reply_message(event.reply_token, TextSendMessage(order_list))
            

if __name__ == '__main__':
    app.run()