# -*- coding: utf-8 -*-
import json
import csv
#from PIL import Image, ImageDraw, ImageFont
import io
import os
import re

text = 'aaaa/'

'''
match (text):
    case "a":
        print('a')
        break
    case "ab":
        print('ab')
        break
    case "abc":
        print('abc')
        break
'''

text2 = text.split('/')
print(text2)
if(text2[1]):
    print('hi')
else:
    print('no')