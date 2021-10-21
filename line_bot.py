# -*- coding: utf-8 -*-
"""
Created on Thu Jul 23 15:50:24 2020

@author: jacky
"""

from __future__ import unicode_literals
import os
import json
import csv

from flask import Flask, request, abort
from PIL import Image, ImageDraw, ImageFont

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

description = '指令輸入格式:\n(指令)/ (內容)\n\n指令:\n說明、吃、點、統計、明細、clear'

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
    
    userId = event.source.user_id
    message = event.message.text
    texts = message.split('/', 1)
    
    if texts[0] == '說明':
        line_bot_api.reply_message(event.reply_token, TextSendMessage(description))
        
    elif texts[0] == '吃':
        with open('data/data.json', 'r', encoding = 'utf-8') as jsonFile: 
            data = json.load(jsonFile)
        data['restaurant'] = texts[1]
        with open('data/data.json', 'w', encoding = 'utf-8') as jsonFile: 
            json.dump(data, jsonFile)
            
        with open('data/restaurant/' + texts[1] + '.csv', newline = '', encoding = 'utf-8') as csvFile: 
            menu = csv.reader(csvFile)
            for row in menu:
                line_bot_api.reply_message(event.reply_token, TextSendMessage(row[0] + '. ' + row[1] + ' ' + row[2] + '\n'))
        
    elif texts[0] == '點':
        profile = line_bot_api.get_profile(userId)
        with open('data/order.csv', 'a+', encoding = 'utf-8') as f:
            orders = texts[1].split(',')
            for order in orders:
                f.write(profile.display_name + ',' + order + '\n')
            line_bot_api.reply_message(event.reply_token, TextSendMessage('收到'))          
            
    elif texts[0] == '統計':  
        with open('data/order.csv', newline = '', encoding = 'utf-8') as csvFile: 
            orders = csv.reader(csvFile)
        with open('data/data.json', 'r', encoding = 'utf-8') as jsonFile: 
            data = json.load(jsonFile)
        with open('data/restaurant/' + data['restaurant'] + '.csv', newline = '', encoding = 'utf-8') as csvFile: 
            menu = csv.reader(csvFile)
            
        food_nums = {}
        for order in orders:
            food_nums[int(order[1])] += 1
            
        reply = ''
        total = 0
        total_price = 0
        for food_num in food_nums:
            reply += ( menu[food_num][1] + ' ' + str(food_nums[food_num]) + '份\n')
            total += food_nums[food_num]
            total_price += ( int(menu[food_num][2]) * food_nums[food_num] )
            
        line_bot_api.reply_message(event.reply_token, TextSendMessage(reply + '共' + str(total) + '份' + str(total_price) + '元'))
    
    elif texts[0] == '明細':
        with open('data/order.csv', newline = '', encoding = 'utf-8') as csvFile: 
            orders = csv.reader(csvFile)
        with open('data/data.json', 'r', encoding = 'utf-8') as jsonFile: 
            data = json.load(jsonFile)
        with open('data/restaurant/' + data['restaurant'] + '.csv', newline = '', encoding = 'utf-8') as csvFile: 
            menu = csv.reader(csvFile)
        
        order_no = 1
        reply = ''
        for order in orders:
            reply += ( str(order_no) + '. ' + order[0] + '/' + menu[int(order[1])][1] + '/' + menu[int(order[1])][2] + '元\n' )
        line_bot_api.reply_message(event.reply_token, TextSendMessage(reply))
        '''
        img = Image.new('RGB', (600, 800), color=(255, 255, 255))
        font = ImageFont.truetype('arial.ttf', size = 24)
        d = ImageDraw.Draw(img)
        d.text((40, 40), 'Hello', fill=(0, 0, 0), font = font)
        
        img.save('data/tmp.png')
        '''

    elif texts[0] == 'clear':
        os.remove('data/order.csv')
        os.remove('data/tmp.png')
        '''
        with open('data/data.json', 'r') as jsonFile:
            data = json.load(jsonFile)
        data['amount'] = 0
        data['order_no'] = 0
        with open('data/data.json', 'w') as jsonFile:
            json.dump(data, jsonFile)
        with open('data/order.txt', 'w') as f:
            f.write('')
        '''


if __name__ == '__main__':
    app.run()