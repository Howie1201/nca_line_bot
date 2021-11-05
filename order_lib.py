# -*- coding: utf-8 -*-
"""
Created on Thu Oct 28 15:50:24 2021

@author: jacky
"""

import json
import csv
import os

restaurant_folder = 'data/restaurant/'
data_path = 'data/data.json'
order_path = 'data/order.csv'
detail_path = 'static/detail.txt'
#detail_url = 'https://eatwhat-in-ncu.herokuapp.com/detail'

# TODO: add comment, optimize

# check if the input message should be handled
def isCommand(message, group_id):
    if not '/' in message:
        return False 
    if not group_id:
        return False
    else:
        data = getData()
        groups = data['group_id']
        if group_id not in groups.values():
            return False
    return True

# return data in data.json
def getData():
    with open(data_path, 'r', encoding = 'utf-8') as jsonFile: 
        data = json.load(jsonFile)
    return data 

# edit data in data.json
def setData(data):
    with open(data_path, 'w', encoding = 'utf-8') as jsonFile: 
        json.dump(data, jsonFile)

# check if the user is admin
def checkAuthority(user_id):
    data = getData()
    admins = data['admin']
    return True if user_id in admins.values() else False

# list the restaurants in restaurant folder
def listRestaurant():
    reply = ''
    for dirPath, dirNames, fileNames in os.walk(restaurant_folder):
        for fileName in fileNames:
            restaurant = fileName.split('.')[0]
            reply += ( restaurant + '\n' )
    return reply

# check if the value of data['restaurant'] is not empty   
def hasRestaurant():
    data = getData()
    return True if data['restaurant'] else False

# return today's restaurant
def getRestaurant():
    data = getData()
    return data['restaurant']

# set today's restaurant
def setRestaurant(restaurant):
    data = getData()
    data['restaurant'] = restaurant
    setData(data)

# check if a restaurant's menu is in database 
def hasMenu(restaurant):
    restaurant_path = restaurant_folder + restaurant + '.csv'
    return True if os.path.isfile(restaurant_path) else False

# get a restaurant's menu
def getMenu(restaurant):
    with open(restaurant_folder + restaurant + '.csv', newline = '', encoding = 'utf-8') as menuFile:
        menu = list(csv.reader(menuFile))
        return menu
    
# print a restaurant's menu
def printMenu(restaurant):
    reply = ''
    menu = getMenu(restaurant)
    for food in menu:
        reply += ( food[0] + '. ' + food[1] + ' ' + food[2] + '\n' )  
    return reply

# check if user's input is valid
def checkValidity(order):
    menu = getMenu(getRestaurant())
    if order.isnumeric():
        if int(order) > 0 and int(order) < len(menu):
            return True
    return False
    
# add order(s) into order.csv
def addOrder(user_id, orders):
    orders = orders.split('/') 
    with open(order_path, 'a+', encoding = 'utf-8') as orderFile:        
        for order in orders:
            if checkValidity(order):
                orderFile.write(user_id + ',' + order + '\n')          
            else:
                return '請依照格式輸入'
    return '收到'

# cancel and remove order(s) from order.csv
def cancelOrder(user_id, cancel_orders):
    orders = getOrder()
    os.remove(order_path)
    # if user does input parameters, cancel particular orders
    if cancel_orders:
        cancel_orders = cancel_orders.split('/')
        for cancel_order in cancel_orders:
            for order in orders:
                if order[0] != user_id or order[1] != cancel_order:
                    addOrder(order[0], order[1])
    # if user does not input parameters, cancel all the orders that match user_id 
    else:
        for order in orders:
            if order[0] != user_id:
                addOrder(order[0], order[1])
    return '取消訂單'
    
# return orders
def getOrder():
    with open(order_path, newline = '', encoding = 'utf-8') as orderFile:
        orders = list(csv.reader(orderFile))
    return orders

# count number of each items via dict
def countOrder(orders):
    foods = {}
    for order in orders:
        if order[1] in foods:
            foods[order[1]] += 1
        else:
            foods[order[1]] = 1
    return foods

# print each items' number, total number, and price
def printStatistic(foods, menu):
    reply = ''
    total = 0
    total_price = 0          
    for food in foods:
        food_name = menu[int(food)][1]
        food_price = menu[int(food)][2]
        reply += ( food_name + ' ' + str(foods[food]) + '份\n')
        total += foods[food]
        total_price += ( int(food_price) * foods[food] )    
    reply += ( '共' + str(total) + '份' + str(total_price) + '元' )
    return reply
    
# write orders into detail.txt which is loaded by detail.html and show to the users
def showDetailAsHtml(line_bot_api, orders, menu, domain_name):
    if os.path.isfile(detail_path):
        os.remove(detail_path)
    order_no = 1          
    for order in orders:
        try:
            user_name = line_bot_api.get_profile(order[0]).display_name
        except:
            user_name = order[0]
        print(user_name)
        food_name = menu[int(order[1])][1]
        food_price = menu[int(order[1])][2]
        with open(detail_path, 'a+', encoding = 'utf-8') as detailFile:    
            detailFile.write( str(order_no) + '. ' + user_name + ' / ' + food_name + ' / ' + food_price + '元\n' )
        order_no += 1
    return domain_name + 'detail'

# print orders via line bot
def printDetail(line_bot_api, orders, menu):
    order_no = 1
    reply = ''            
    for order in orders:
        try:
            user_name = line_bot_api.get_profile(order[0]).display_name
        except:
            user_name = order[0]
        food_name = menu[int(order[1])][1]
        food_price = menu[int(order[1])][2]
        reply += ( str(order_no) + '. ' + user_name + '/' + food_name + '/' + food_price + '元\n' )
        order_no += 1
    return reply

# remove unnecessary files 
def clear():
    if os.path.isfile(order_path):
        os.remove(order_path)
    if os.path.isfile(detail_path):
        os.remove(detail_path)
    

    
    
    
    
    
    
    