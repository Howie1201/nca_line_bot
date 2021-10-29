# -*- coding: utf-8 -*-
"""
Created on Thu Jul 23 15:50:24 2020

@author: jacky

version: 2.5
"""

from __future__ import unicode_literals
import os
import order_lib

from flask import Flask, request, abort, render_template
from PIL import Image, ImageDraw, ImageFont

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageSendMessage

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

@app.route("/detail")
def showDetail():
    return render_template('datail.html')
    

description = '指令輸入格式:\n(指令)/(內容1)/(內容2)...\n\n指令:\n說明、吃、點、統計、明細、clear'

# decorator 判斷 event 為 MessageEvent
# event.message 為 TextMessage 
# 所以此為處理 TextMessage 的 handler
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # TODO: optimization
    print(event)
    
    # get user id and message
    userId = event.source.user_id
    message = event.message.text
    
    # handle command and string processing
    if '/' not in message:
        return
    message = message.replace(' ','').replace('\n','').split('/',1)
    command = message[0]
    parameters = message[1]  
    reply = ''
    
    if command == '說明':
        reply = description
            
    elif command == '吃':
        admin = order_lib.checkAuthority(userId)
        if not admin:
            return 
        restaurant = parameters
        order_lib.setRestaurant(restaurant)
        reply = order_lib.printMenu(restaurant)               
                                                        
    elif command == '點':
        user_name = line_bot_api.get_profile(userId).display_name
        reply = order_lib.addOrder(user_name, parameters)
                      
    elif command == '取消':
        user_name = line_bot_api.get_profile(userId).display_name
        order_lib.cancelOrder(user_name, parameters)
        #print('cancel')
        
    elif command == '統計':        
        orders = order_lib.getOrder()  
        restaurant = order_lib.getRestaurant()
        menu = order_lib.getMenu(restaurant)        
        foods = order_lib.countOrder(orders)      
        reply = order_lib.printStatistic(foods, menu)
        
    elif command == '明細':  
        orders = order_lib.getOrder()     
        restaurant = order_lib.getRestaurant()         
        menu = order_lib.getMenu(restaurant)
        reply = order_lib.printDetail(orders, menu)
        printDetailAsHtml()
        
    elif command == 'clear': 
        reply = order_lib.clear()
    
    line_bot_api.reply_message(event.reply_token, TextSendMessage(reply))
    
'''
        TODO:
        
        # create and send order datail image
        img = Image.new('RGB', (600, 800), color=(255, 255, 255))
        font = ImageFont.truetype('data/arial.ttf', size = 24)
        iDraw = ImageDraw.Draw(img)
        iDraw.text((40, 40), 'Hello', fill=(0, 0, 0), font = font)
        
        img.save('data/detail.png')
        line_bot_api.reply_message(event.reply_token, ImageSendMessage('data/detail.png', 'data/detail.png'))
'''


if __name__ == '__main__':
    app.run()