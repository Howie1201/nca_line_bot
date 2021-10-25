# -*- coding: utf-8 -*-
import json
import csv
#from PIL import Image, ImageDraw, ImageFont
import io
import os

'''
bool1 = os.path.isfile('restaurant/a.csv')
bool2 = os.path.isfile('restaurant/皇上皇.csv')
print(str(bool1) + ' ' + str(bool2))
'''
'''
def a()

if a():
    print('ya')
else:
    print('no')
    
def a():
    return []


'''

'''
with open('data/restaurant.json', 'r', encoding = 'utf-8') as jsonFile: 
    data = json.load(jsonFile)

index = 1

for food in data['甲一']:
    print(str(index) + '. ' + food + ' ' + str(data['甲一'][food]))
    index += 1
    


with open('data/restaurant.json', 'w') as jsonFile:
    json.dump(data, jsonFile)
'''

'''
with open('data/restaurant/' + '甲一' + '.csv', 'r', encoding = 'utf-8') as csvFile: 
    rows = csv.reader(csvFile)
    for row in rows:
        print(row[0] + '. ' + row[1] + ' ' + row[2])
'''

'''
img = Image.new('RGB', (600, 800), color=(255, 255, 255))
font = ImageFont.truetype('arial.ttf', size = 24)
d = ImageDraw.Draw(img)
d.text((40, 40), 'Hello', fill=(0, 0, 0), font = font)

img.save('tmp.png')
'''


#img = Image.new('RGB', (200, 100), (255, 255, 255))

#s = io.BytesIO()
#img.save(s, 'png')
#in_memory_file = s.getvalue()
