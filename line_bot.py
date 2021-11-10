# -*- coding: utf-8 -*-
"""
Created on Thu Jul 23 15:50:24 2020

@author: jacky

version: 3.5
"""

from __future__ import unicode_literals
from flask import Flask, request, abort, render_template
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

import order_lib


app = Flask(__name__)

line_bot_api = LineBotApi('KbUSP5ShwG5gziWRdy3niYUieAZaYlDc2YMW1HB3Ao05YRm+DKUar29lK0lfqjeMqzLRm1MLALf/R4jIV/k+98YxIR40SryCI8qsokVBe31heMMafyPQSI89odk42Ts1dD9b35gyPMCkOhHEGp+M/wdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('b33a01e1e548c7b39a732d62245e1d36')
app_name = 'eatwhat-in-ncu'
admins = {"洪仲杰" : "Uefa7580b75912cf5cbd1be6dba8dafbe",
		  "陳宜祥" : "U75851bf4cd33d189464170b50df30ee8",
		  "蕭崇聖" : "U45eac4b2d3598d5bb9ee33cee0518d45"}
groups = {"午餐群組" : "Cf4a08527ed49eab9d2cf53a8b0309cf0",
		  "測試群組" : "Ce6071d5887fd879bc620143fce3c8382"}
restaurants = ['大盛','小煮角','六星','日日佳','甲一','皇上皇','華圓','寶多福','小林','月枱']


domain_name = 'https://' + app_name + '.herokuapp.com/'
description = '指令輸入格式:\n\
[指令]/[內容1]/[內容2]...\n\
\n\
指令:\n\
說明、吃、點、取消、統計、截止、clear\n\
詳細說明請見https://github.com/jackyh1999/line_bot'


@app.route("/")
def home():
    return 'Hi'

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
    print('show detail')
    return render_template('detail.html')
    

# check if the input message should be handled
def isCommand(message, group_id):
    if not '/' in message:
        return False 
    if group_id not in groups.values():
        return False
    return True

# check if the user is admin
def isAdmin(user_id):
    if user_id not in admins.values():
        return False
    return True

''''''''''''''''''
'''主要程式在這'''
''''''''''''''''''

# decorator 判斷 event 為 MessageEvent
# event.message 為 TextMessage 
# 所以此為處理 TextMessage 的 handler
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):

    print(event)
    
    # get user id and message  
    message = event.message.text 
    message_type = event.source.type
    user_id = event.source.user_id     
    group_id = event.source.group_id if message_type == 'group' else ''
      
    # handle command and process string    
    if not isCommand(message, group_id):
        return 
    message = message.replace(' ','').replace('\n','').split('/',1)
    print(message)
    
    # command's format: [command, parameters]
    command = message[0]
    parameters = message[1]  
    reply = ''
    
    # 使用說明
    if command == '說明':
        reply = description
            
    # 列出可提供菜單的餐廳
    elif command == '餐廳':
        for restaurant in restaurants:
            reply += ( restaurant + '\n' )
    
    # 決定要吃的餐廳
    # 需要admin權限
    elif command == '吃':
        if not isAdmin(user_id):
            return                     
        restaurant = parameters
        if restaurant in restaurants:
            order_lib.setRestaurant(restaurant)
            reply = order_lib.printMenu(restaurant)
        else:
            reply = '查無此餐廳'
        
    # 清除訂餐資料
    # 需要admin權限
    elif command == '清除': 
        if not isAdmin(user_id):
            return           
        order_lib.clear()
        reply = '清除資料'
            
    # 已經決定好餐廳才能使用的指令
    if order_lib.getRestaurant():           
        
        # 點餐             
        if command == '點':            
            reply = order_lib.addOrder(user_id, parameters)
                          
        # 取消點餐
        elif command == '取消':
            reply = order_lib.cancelOrder(user_id, parameters)
            
        # 統計餐點並顯示明細表(網頁)
        elif command == '統計':      
            orders = order_lib.getOrder()  
            restaurant = order_lib.getRestaurant()
            menu = order_lib.getMenu(restaurant)        
            foods = order_lib.countOrder(orders)      
            reply = order_lib.printStatistic(foods, menu)
            reply += ('\n' + order_lib.showDetailAsHtml(line_bot_api, orders, menu, domain_name))
           
        # 回覆明細表
        elif command == '明細':
            orders = order_lib.getOrder()  
            restaurant = order_lib.getRestaurant()
            menu = order_lib.getMenu(restaurant)  
            reply = order_lib.printDetail(line_bot_api, orders, menu)
            
        # 關閉點餐
        # 需要admin權限
        elif command == '截止': 
            if not isAdmin(user_id):
                return            
            order_lib.setRestaurant('')   
            
    '''
    # This part of code requires verified line official account  
    
    if command == '成員':
        admin = order_lib.checkAuthority(user_id)
        if not admin:
            return
        member_ids = line_bot_api.get_group_member_ids('Cf4a08527ed49eab9d2cf53a8b0309cf0')
        for member_id in member_ids:
            member_info = member_id + ' ' + line_bot_api.get_profile(member_id).display_name + '\n'
            print(member_info)
            with open('static/detail.txt', 'w+', encoding = 'utf-8') as f:
                f.write(member_info)
    '''
    
    # 回覆訊息
    if reply:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(reply))


if __name__ == '__main__':
    app.run()