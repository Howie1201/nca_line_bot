# -*- coding: utf-8 -*-
"""
Created on Thu Jul 23 15:50:24 2020

@author: jacky

version: 2.4
"""

from __future__ import unicode_literals
import os
import json
import csv

from flask import Flask, request, abort
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


def checkAuthority(userId):
    return True


def setRestaurant(restaurant):
    with open('data/data.json', 'r', encoding = 'utf-8') as jsonFile: 
        data = json.load(jsonFile)
    data['restaurant'] = restaurant
    with open('data/data.json', 'w', encoding = 'utf-8') as jsonFile: 
        json.dump(data, jsonFile)
    return restaurant

def getMenu():
    with open('data/data.json', 'r', encoding = 'utf-8') as jsonFile:
        data = json.load(jsonFile)
    restaurant_path = 'data/restaurant/' + data['restaurant'] + '.csv'
    if os.path.isfile(restaurant_path):
        with open(restaurant_path, newline = '', encoding = 'utf-8') as menuFile:
            menu = list( csv.reader(menuFile) )
            return menu
    else:
        return []
    

def printMenu(restaurant):
    restaurant_path = 'data/restaurant/' + restaurant + '.csv'
    if os.path.isfile(restaurant_path):
        with  open(restaurant_path, newline = '', encoding = 'utf-8') as menuFile:
            menu = list( csv.reader(menuFile) )        
        reply = ''
        for food in menu:
            reply += ( food[0] + '. ' + food[1] + ' ' + food[2] + '\n' )
        return reply
    else:           
        return '查無此餐廳'

def addOrder(userId, orders):
    f = open('data/order.csv', 'a+', encoding = 'utf-8')
    profile = line_bot_api.get_profile(userId)         
    orders = orders.split('/')     
    for order in orders:
        f.write(profile.display_name + ',' + order + '\n')     
    f.close()          
    return '收到'
    

def countOrder():
    with open('data/order.csv', newline = '', encoding = 'utf-8') as orderFile:
        orders = list(csv.reader(orderFile))
    foods = {}
    for order in orders:
        if order[1] in foods:
            foods[order[1]] += 1
        else:
            foods[order[1]] = 1
    return foods

def printStatistic(foods, menu):
    reply = ''
    total = 0
    total_price = 0
    # if database has restaurant's menu 
    if menu:
        # print items, numbers, total numbers, total price, etc.               
        for food in foods:
            food_name = menu[int(food)][1] if food.isnumeric() else food
            food_price = menu[int(food)][2] if food.isnumeric() else 0
            reply += ( food_name + ' ' + str(foods[food]) + '份\n')
            total += foods[food]
            total_price += ( int(food_price) * foods[food] )    
        reply += ( '共' + str(total) + '份' + str(total_price) + '元' )
    else:             
        for food in foods:
            reply += ( food + ' ' + str(foods[food]) + '份\n')
            total += foods[food] 
        reply += ( '共' + str(total) + '份' )
    return reply
    
def printDetail(orders, menu):
    order_no = 1
    reply = ''
    if menu:               
        # print order detail
        for order in orders:
            food_name = menu[int(order[1])][1]
            food_price = menu[int(order[1])][2]
            reply += ( str(order_no) + '. ' + order[0] + '/' + food_name + '/' + food_price + '元\n' )
            order_no += 1      
    else:
        for order in orders:
            reply += ( str(order_no) + '. ' + order[0] + '/' + order[1] + '\n' )
            order_no += 1
    return reply


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
    
    # handle command
    if '/' not in message:
        return
    message = message.split().split('/', 1)
    command = message[0]
    parameters = message[1]  
    reply = ''
    
    if command == '說明':
        line_bot_api.reply_message(event.reply_token, TextSendMessage(description))
            
    elif command == '吃':
        checkAuthority(userId)
        # set restaurant            
        # if database has restaurant's menu, print it
        restaurant = setRestaurant(parameters)
        reply = printMenu(restaurant)
        
                                                        
    elif command == '點':
        reply = addOrder(userId, parameters)
                        
    elif command == '統計':                        
        foods = countOrder()
        menu = getMenu()
        printStatistic(foods, menu)
        
    elif command == '明細':          
        with open('data/order.csv', newline = '', encoding = 'utf-8') as orderFile:
            orders = list( csv.reader(orderFile) )           
        menu = getMenu()
        printDetail(orders, menu)
        
    elif command == 'clear':
        os.remove('data/order.csv')
    
    line_bot_api.reply_message(event.reply_token, TextSendMessage(reply))
    
'''
    match command:
        
        case '說明':
            line_bot_api.reply_message(event.reply_token, TextSendMessage(description))
            
        case '吃':
            checkAuthority(userId)
            # set restaurant            
            # if database has restaurant's menu, print it
            restaurant = setRestaurant(parameters)
            printMenu(restaurant)
                                                        
        case '點':
            addOrder(userId, parameters)
                            
        case '統計':                        
            foods = countOrder()
            menu = getMenu()
            printStatistic(menu)           
            
        case '明細':          
            with open('data/order.csv', newline = '', encoding = 'utf-8') as orderFile:
                orders = list( csv.reader(orderFile) )           
            menu = getMenu()
            printDetail(orders, menu)
'''
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
'''
        case 'clear':
            os.remove('data/order.csv')
            #os.remove('data/detail.png')
'''

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